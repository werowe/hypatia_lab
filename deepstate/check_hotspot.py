#!/usr/bin/env python3
"""Run only the historical-data load and hotspot selector, then notify Telegram.

Copyright (c) 2026 Walker Rowe. SPDX-License-Identifier: MIT.
Data source: DeepStateMap.Live (https://deepstatemap.live/en).
"""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import logging
import os
from pathlib import Path
import tempfile
from urllib.parse import quote_plus

import certifi
import geopandas as gpd
import pandas as pd
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from shapely.geometry import shape
from shapely.geometry import GeometryCollection
from shapely import wkb
from shapely.ops import unary_union

from hotspot_selector import (
    AREA_CRS, NoNewGainError, prepare_hotspot_comparison,
    select_weekly_ukrainian_hotspot,
)

ROOT = Path(__file__).resolve().parent
NO_GAIN = "No Ukrainian gain above MIN_GAIN_KM2 was found"
LOG = logging.getLogger("deepstate.hotspot")


def load_history():
    missing = [k for k in ("MONGODB_USER", "MONGODB_PWD", "CLUSTER") if not os.getenv(k)]
    if missing:
        raise RuntimeError("Missing MongoDB settings: " + ", ".join(missing))
    uri = "mongodb+srv://{}:{}@{}".format(
        quote_plus(os.environ["MONGODB_USER"]),
        quote_plus(os.environ["MONGODB_PWD"]), os.environ["CLUSTER"],
    )
    with MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=30000) as client:
        data = list(client.geodb.geodata.find(
            {}, {"_id": 0, "geometry": 1, "epoch_time": 1, "properties": 1},
        ))
    if not data:
        raise RuntimeError("MongoDB contains no historical records")
    df = pd.DataFrame(data)
    df["geometry"] = df["geometry"].apply(lambda x: shape(x) if x else None)
    LOG.info("Loaded %s records from MongoDB", len(df))
    return gpd.GeoDataFrame(df, geometry="geometry")


def telegram_settings():
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHANNEL_ID")
    if not token or not chat:
        raise RuntimeError("Configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
    return token, chat


def send_telegram(message):
    token, chat = telegram_settings()
    message_id = os.getenv("TELEGRAM_MESSAGE_ID")
    method = "editMessageText" if message_id else "sendMessage"
    payload = {"chat_id": chat, "text": message}
    if message_id:
        payload["message_id"] = message_id
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/{method}",
            data=payload, timeout=(10, 30),
        )
    except requests.RequestException:
        # Requests exceptions can contain the token-bearing URL.
        raise RuntimeError("Telegram network request failed; notification not recorded") from None
    try:
        result = response.json()
    except ValueError:
        raise RuntimeError(f"Telegram returned invalid JSON (HTTP {response.status_code})") from None
    if not response.ok or not result.get("ok"):
        # Repeating an edit after a state-write failure is harmless.
        if (message_id and result.get("error_code") == 400
                and result.get("description", "").startswith("Bad Request: message is not modified")):
            return
        raise RuntimeError(f"Telegram rejected notification (HTTP {response.status_code}, "
                           f"error {result.get('error_code', 'unknown')})")


def format_message(area, hotspot):
    lat = (area["top_left"][0] + area["bottom_right"][0]) / 2
    lon = (area["top_left"][1] + area["bottom_right"][1]) / 2
    return (
        "DeepState: new Ukrainian gain\n"
        f"{hotspot['baseline_date'].date()} → {hotspot['latest_date'].date()}"
        f" | {hotspot['method']}\n"
        f"15 km hotspot: gain {hotspot['gain_km2_in_window']:.3f} km²"
        f" ({hotspot['new_gain_km2_in_window']:.3f} newly detected); "
        f"newly mapped occupied {hotspot['newly_occupied_km2_in_window']:.3f} km²; "
        f"occupied→gray {hotspot['occupied_to_gray_km2_in_window']:.3f} km²\n"
        f"Bounds (lat, lon): TL {area['top_left'][0]:.4f}, {area['top_left'][1]:.4f}"
        f" | BR {area['bottom_right'][0]:.4f}, {area['bottom_right'][1]:.4f}\n"
        f"https://deepstatemap.live/en#12/{lat:.6f}/{lon:.6f}"
    )


def load_notification_state(history):
    """Read acknowledged gain footprints; migrate the old snapshot-only key."""
    path = ROOT / ".hotspot_notification_state.json"
    if not path.exists():
        return {"version": 2, "area_crs": AREA_CRS, "alerts": []}, GeometryCollection()
    state = json.loads(path.read_text())
    if not isinstance(state, dict):
        raise RuntimeError("Unrecognized notification state; refusing to discard its history")
    if state.get("version") == 2:
        if state.get("area_crs") != AREA_CRS:
            raise RuntimeError("Notification-state CRS does not match the selector")
        seen = wkb.loads(state["seen_gain_wkb"], hex=True)
        if not seen.is_valid:
            raise RuntimeError("Notification state contains invalid gain geometry")
        if not isinstance(state.get("alerts"), list):
            raise RuntimeError("Notification state is missing its alert ledger")
        return state, seen
    if "latest_epoch" in state:
        epoch = int(state["latest_epoch"])
        historical = history[history["epoch_time"] <= epoch]
        comparison = prepare_hotspot_comparison(historical)
        LOG.info("Migrating existing notification at epoch %s to geometry tracking", epoch)
        return {
            "version": 2, "area_crs": AREA_CRS, "alerts": [],
            "migrated_snapshot_key": state,
        }, comparison["gain"]
    raise RuntimeError("Unrecognized notification state; refusing to discard its history")


def save_notification_state(state, seen, comparison, history):
    """Atomically persist the ledger and its projected geometry, mode 0600."""
    state["seen_gain_wkb"] = seen.wkb_hex
    state["last_checked_epoch"] = int(history["epoch_time"].max())
    state["last_comparison"] = {
        "baseline_date": str(comparison["baseline_date"].date()),
        "latest_date": str(comparison["latest_date"].date()),
    }
    path = ROOT / ".hotspot_notification_state.json"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=ROOT, prefix=".hotspot_", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(state, stream, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def check(dry_run=False):
    history = load_history()
    comparison = prepare_hotspot_comparison(history)
    state, seen = load_notification_state(history)
    # Land leaving the liberated layer can be reported again if later regained.
    # A no-gain check must also persist this pruning.
    seen = seen.intersection(comparison["liberated_latest"])
    try:
        area, hotspot = select_weekly_ukrainian_hotspot(
            history, exclude_gain=seen, _comparison=comparison,
        )
    except ValueError as exc:
        if str(exc) != NO_GAIN and not isinstance(exc, NoNewGainError):
            raise
        LOG.info("%s; no Telegram notification", exc)
        if not dry_run:
            save_notification_state(state, seen, comparison, history)
        return 0
    message = format_message(area, hotspot)
    LOG.info("%s", message)
    if dry_run:
        LOG.info("Dry run: no Telegram message or notification-state update")
        return 0
    send_telegram(message)
    # Acknowledge the whole comparison after its first successful alert, so
    # other unchanged hotspots do not trickle out on subsequent days.
    seen = unary_union([seen, comparison["gain"]])
    state["alerts"].append({
        "notified_at_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_epoch": int(history["epoch_time"].max()),
        "selected_area": area,
        "details": {
            key: str(value.date()) if isinstance(value, pd.Timestamp) else value
            for key, value in hotspot.items()
        },
        "message": message,
    })
    save_notification_state(state, seen, comparison, history)
    LOG.info("Telegram notification delivered")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv(ROOT / ".env")
    load_dotenv(ROOT / "telegram.env")
    os.umask(0o077)
    with (ROOT / ".hotspot_check.lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            LOG.info("Another hotspot check is running; skipping")
            return 0
        try:
            return check(args.dry_run)
        except Exception as exc:
            LOG.error("Hotspot check failed (%s): %s", type(exc).__name__, exc)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
