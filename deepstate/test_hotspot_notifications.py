"""Geometric and delivery regressions; never sends real Telegram messages."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, box
from shapely.ops import unary_union

import check_hotspot as notifier
import hotspot_selector as selector

ORIGIN = gpd.GeoSeries([Point(35, 49)], crs=4326).to_crs(selector.AREA_CRS).iloc[0]
X, Y = ORIGIN.x, ORIGIN.y
PARTS = {
    "A": box(X, Y, X + 2000, Y + 2000),
    "B": box(X + 200000, Y, X + 201000, Y + 1000),
    "S": box(X + 2000, Y, X + 2005, Y + 1000),  # 0.005 km²
    "T": box(X + 2000, Y, X + 2015, Y + 1000),  # 0.015 km², includes S
}
LIBERATED_OLD = box(X - 30000, Y, X - 29000, Y + 1000)
GRAY = box(X + 3000, Y, X + 3500, Y + 500)
NEW_OCCUPIED = box(X + 5000, Y, X + 6000, Y + 1000)
OCCUPIED = unary_union([
    box(X, Y, X + 2100, Y + 2100), PARTS["B"], GRAY,
    box(X + 300000, Y, X + 301000, Y + 1000),
])


def history(extra):
    """Four stable baseline days followed by explicit daily map changes."""
    snapshots = [(f"2026-11-{day:02d}", (), False, False) for day in range(1, 5)] + extra
    rows = []
    for day, names, gray, new_occupied in snapshots:
        liberated = unary_union([LIBERATED_OLD] + [PARTS[name] for name in names])
        occupied = OCCUPIED.difference(liberated)
        if gray:
            occupied = occupied.difference(GRAY)
        if new_occupied:
            occupied = occupied.union(NEW_OCCUPIED)
        layers = [("liberated", liberated), ("geoJSON.status.occupied", occupied)]
        if gray:
            layers.append(("geoJSON.status.unknown", GRAY))
        for status, geom in layers:
            rows.append({"epoch_time": int(pd.Timestamp(day).timestamp()),
                         "properties": {"name": status}, "geometry": geom})
    return gpd.GeoDataFrame(rows, geometry="geometry", crs=selector.AREA_CRS).to_crs(4326)


FIRST = [("2026-11-05", ("A",), True, True)]


class NotificationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.root_patch = patch.object(notifier, "ROOT", self.root)
        self.root_patch.start()
        self.telegram = patch.object(notifier, "send_telegram").start()

    def tearDown(self):
        patch.stopall()
        self.temporary.cleanup()

    def run_check(self, frame, dry_run=False):
        with patch.object(notifier, "load_history", return_value=frame):
            return notifier.check(dry_run=dry_run)

    def state(self):
        return json.loads((self.root / ".hotspot_notification_state.json").read_text())

    def test_message_contains_requested_fields_and_area(self):
        self.run_check(history(FIRST))
        message = self.telegram.call_args.args[0]
        for value in ("2026-11-01", "2026-11-05", "occupied to liberated",
                      "gain 4.000 km²", "newly mapped occupied 1.000 km²",
                      "occupied→gray 0.250 km²", "TL ", "BR ", "https://deepstatemap.live"):
            self.assertIn(value, message)
        self.assertLess(len(message), 1000)
        self.assertEqual(len(self.state()["alerts"]), 1)
        self.assertEqual((self.root / ".hotspot_notification_state.json").stat().st_mode & 0o777, 0o600)

    def test_same_geometry_does_not_repeat_when_dates_or_baseline_change(self):
        snapshots = FIRST.copy()
        self.run_check(history(snapshots))
        for day in range(6, 10):
            snapshots.append((f"2026-11-{day:02d}", ("A",), True, True))
            self.run_check(history(snapshots))
        self.assertEqual(self.telegram.call_count, 1)
        self.assertEqual(len(self.state()["alerts"]), 1)

    def test_new_smaller_hotspot_is_found_outside_old_largest(self):
        self.run_check(history(FIRST))
        self.run_check(history(FIRST + [("2026-11-06", ("A", "B"), True, True)]))
        self.assertEqual(self.telegram.call_count, 2)
        details = self.state()["alerts"][-1]["details"]
        self.assertAlmostEqual(details["new_gain_km2_in_window"], 1.0, places=5)
        self.assertAlmostEqual(details["gain_km2_in_window"], 1.0, places=5)

    def test_previous_secondary_hotspot_does_not_alert_next_day(self):
        self.run_check(history([("2026-11-05", ("A", "B"), False, False)]))
        self.run_check(history([("2026-11-05", ("A", "B"), False, False),
                                ("2026-11-06", ("A", "B"), False, False)]))
        self.assertEqual(self.telegram.call_count, 1)

    def test_small_unreported_additions_accumulate_until_threshold(self):
        self.run_check(history(FIRST))
        small = FIRST + [("2026-11-06", ("A", "S"), True, True)]
        self.run_check(history(small))
        self.assertEqual(self.telegram.call_count, 1)
        self.run_check(history(small + [("2026-11-07", ("A", "T"), True, True)]))
        self.assertEqual(self.telegram.call_count, 2)
        details = self.state()["alerts"][-1]["details"]
        self.assertAlmostEqual(details["new_gain_km2_in_window"], 0.015, places=5)
        self.assertAlmostEqual(details["gain_km2_in_window"], 4.015, places=5)

    def test_lost_land_can_be_reported_if_regained(self):
        self.run_check(history(FIRST))
        lost = FIRST + [("2026-11-06", (), False, False)]
        self.run_check(history(lost))
        self.assertEqual(self.telegram.call_count, 1)
        self.run_check(history(lost + [("2026-11-10", ("A",), True, True)]))
        self.assertEqual(self.telegram.call_count, 2)

    def test_no_gain_is_silent_and_unexpected_failure_is_not_hidden(self):
        self.run_check(history([("2026-11-05", (), False, False)]))
        self.telegram.assert_not_called()
        self.assertEqual(self.state()["alerts"], [])
        with patch.object(notifier, "prepare_hotspot_comparison", side_effect=ValueError("Missing layers")):
            with self.assertRaisesRegex(ValueError, "Missing layers"):
                self.run_check(history(FIRST))

    def test_failed_delivery_is_retried_without_recording_an_alert(self):
        self.telegram.side_effect = RuntimeError("Delivery failed")
        with self.assertRaisesRegex(RuntimeError, "Delivery failed"):
            self.run_check(history(FIRST))
        self.assertFalse((self.root / ".hotspot_notification_state.json").exists())
        self.telegram.side_effect = None
        self.run_check(history(FIRST))
        self.run_check(history(FIRST))
        self.assertEqual(self.telegram.call_count, 2)
        self.assertEqual(len(self.state()["alerts"]), 1)

    def test_dry_run_does_not_send_or_persist(self):
        self.run_check(history(FIRST), dry_run=True)
        self.run_check(history([("2026-11-05", (), False, False)]), dry_run=True)
        self.telegram.assert_not_called()
        self.assertFalse((self.root / ".hotspot_notification_state.json").exists())

    def test_legacy_snapshot_state_migrates_without_resending_old_gain(self):
        first = history(FIRST)
        (self.root / ".hotspot_notification_state.json").write_text(json.dumps({
            "latest_epoch": int(first["epoch_time"].max()), "baseline_date": "2026-11-01",
        }))
        self.run_check(history(FIRST + [("2026-11-06", ("A",), True, True)]))
        self.telegram.assert_not_called()
        self.assertEqual(self.state()["version"], 2)
        self.run_check(history(FIRST + [("2026-11-07", ("A", "B"), True, True)]))
        self.assertEqual(self.telegram.call_count, 1)

    def test_invalid_state_is_not_silently_discarded(self):
        for invalid in ('{"unexpected": true}', '{}', '[]'):
            with self.subTest(state=invalid):
                (self.root / ".hotspot_notification_state.json").write_text(invalid)
                with self.assertRaisesRegex(RuntimeError, "Unrecognized notification state"):
                    self.run_check(history(FIRST))
        self.telegram.assert_not_called()

    def test_restarting_process_still_suppresses_previous_gain(self):
        self.run_check(history(FIRST))
        state, seen = notifier.load_notification_state(history(FIRST))
        self.assertEqual(len(state["alerts"]), 1)
        self.assertGreater(seen.area, 3_999_999)
        self.run_check(history(FIRST))
        self.assertEqual(self.telegram.call_count, 1)


class SelectorCompatibilityTests(unittest.TestCase):
    def test_original_notebook_fields_keep_their_values(self):
        original = Path('/home/werowe/Documents/hypatia_lab/deepstate/hotspot_selector.py')
        if not original.exists():
            self.skipTest('Original server selector is unavailable locally')
        spec = importlib.util.spec_from_file_location('original_hotspot_selector', original)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        frame = history(FIRST)
        expected_area, expected = old.select_weekly_ukrainian_hotspot(frame)
        actual_area, actual = selector.select_weekly_ukrainian_hotspot(frame)
        self.assertEqual(expected_area, actual_area)
        for key, value in expected.items():
            if isinstance(value, float):
                self.assertAlmostEqual(actual[key], value, places=8)
            else:
                self.assertEqual(actual[key], value)


class TelegramResponseTests(unittest.TestCase):
    def test_retry_of_already_delivered_edit_can_record_state(self):
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test-token",
                                    "TELEGRAM_CHAT_ID": "@test",
                                    "TELEGRAM_MESSAGE_ID": "7"}, clear=True):
            with patch.object(notifier.requests, "post") as post:
                post.return_value.ok = False
                post.return_value.json.return_value = {
                    "ok": False, "error_code": 400,
                    "description": "Bad Request: message is not modified: content is exactly the same",
                }
                notifier.send_telegram("Previously delivered alert")

    def test_actual_rejection_does_not_count_as_delivery(self):
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test-token",
                                    "TELEGRAM_CHAT_ID": "@test",
                                    "TELEGRAM_MESSAGE_ID": "7"}, clear=True):
            with patch.object(notifier.requests, "post") as post:
                post.return_value.ok = False
                post.return_value.status_code = 403
                post.return_value.json.return_value = {"ok": False, "error_code": 403}
                with self.assertRaisesRegex(RuntimeError, "Telegram rejected"):
                    notifier.send_telegram("Undelivered alert")


if __name__ == '__main__':
    unittest.main(verbosity=2)
