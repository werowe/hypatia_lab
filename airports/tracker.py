#!/usr/bin/env python3
"""Track Russian airport flight status in SQLite using AeroDataBox via RapidAPI."""
import argparse, hashlib, json, os, sqlite3, sys, time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
DB = Path(os.getenv("DATABASE_FILE", ROOT / "flights.sqlite3"))
AIRPORTS_FILE = Path(os.getenv("AIRPORTS_FILE", ROOT / "airports.json"))
HOST = os.getenv("AERODATABOX_HOST", "aerodatabox.p.rapidapi.com")
BASE_URL = f"https://{HOST}"

SCHEMA = """
CREATE TABLE IF NOT EXISTS airports (
  iata TEXT PRIMARY KEY, icao TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
  timezone TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS fetch_runs (
  id INTEGER PRIMARY KEY, started_at TEXT NOT NULL, finished_at TEXT,
  airport_iata TEXT NOT NULL, window_from TEXT NOT NULL, window_to TEXT NOT NULL,
  status TEXT NOT NULL, http_status INTEGER, flight_count INTEGER,
  error TEXT
);
CREATE TABLE IF NOT EXISTS flight_observations (
  id INTEGER PRIMARY KEY, observed_at TEXT NOT NULL, airport_iata TEXT NOT NULL,
  airport_icao TEXT NOT NULL, direction TEXT NOT NULL, flight_key TEXT NOT NULL,
  flight_number TEXT, callsign TEXT, airline_name TEXT, airline_iata TEXT,
  airline_icao TEXT, origin_iata TEXT, origin_icao TEXT, destination_iata TEXT,
  destination_icao TEXT, scheduled_local TEXT, scheduled_utc TEXT,
  revised_local TEXT, revised_utc TEXT, actual_local TEXT, actual_utc TEXT,
  status TEXT, delay_minutes INTEGER, is_cancelled INTEGER NOT NULL DEFAULT 0,
  is_diverted INTEGER NOT NULL DEFAULT 0, raw_json TEXT NOT NULL,
  UNIQUE(airport_iata, direction, flight_key, scheduled_local, observed_at)
);
CREATE INDEX IF NOT EXISTS idx_obs_status ON flight_observations(status, is_cancelled);
CREATE INDEX IF NOT EXISTS idx_obs_airport_time ON flight_observations(airport_iata, scheduled_local);
"""

def iso_now(): return datetime.now().astimezone().isoformat(timespec="seconds")

def db_connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con

def initialize():
    con = db_connect()
    airports = load_airports()
    con.execute("UPDATE airports SET active = 0")
    con.executemany(
        "INSERT OR REPLACE INTO airports(iata,icao,name,timezone,active) VALUES(?,?,?,?,1)",
        [(a["iata"], a["icao"], a["name"], a["timezone"]) for a in airports],
    )
    con.commit()
    con.close()

def load_airports():
    return json.loads(AIRPORTS_FILE.read_text(encoding="utf-8"))

def get_path(obj, *keys):
    for key in keys:
        if isinstance(obj, dict) and key in obj: obj = obj[key]
        else: return None
    return obj

def first(obj, *paths):
    for path in paths:
        value = get_path(obj, *path.split("."))
        if value not in (None, ""): return value
    return None

def movement_time(movement, kind):
    value = first(movement, f"{kind}.local", f"{kind}.utc") if movement else None
    return value

def minutes_between(scheduled, revised):
    if not scheduled or not revised: return None
    try:
        a = datetime.fromisoformat(scheduled.replace("Z", "+00:00"))
        b = datetime.fromisoformat(revised.replace("Z", "+00:00"))
        return max(0, round((b - a).total_seconds() / 60))
    except (ValueError, TypeError): return None

def normalize(flight, direction, airport):
    movement = flight.get("movement") or flight.get("departure" if direction == "Departure" else "arrival") or {}
    if direction == "Departure":
        side, other = movement, movement.get("airport") or {}
        origin = movement.get("airport") or {}
        destination = first(flight, "arrival.airport", "arrival.airport") or {}
    else:
        side = movement
        origin = first(flight, "departure.airport") or {}
        destination = movement.get("airport") or {}
    scheduled_local = first(side, "scheduledTime.local")
    scheduled_utc = first(side, "scheduledTime.utc")
    revised_local = first(side, "revisedTime.local")
    revised_utc = first(side, "revisedTime.utc")
    actual_local = first(side, "actualTime.local")
    actual_utc = first(side, "actualTime.utc")
    number = first(flight, "number.iata", "number.icao", "number") or ""
    call = first(flight, "callSign", "callsign") or ""
    flight_key = first(flight, "id", "flightId") or f"{number}|{call}|{scheduled_utc or scheduled_local or ''}"
    status = first(flight, "status", "movement.status") or "Unknown"
    status_text = str(status)
    cancel = int("cancel" in status_text.lower())
    divert = int("divert" in status_text.lower())
    if first(side, "status"):
        cancel = cancel or int("cancel" in str(first(side, "status")).lower())
    airline = first(flight, "airline") or {}
    return dict(observed_at=iso_now(), airport_iata=airport["iata"], airport_icao=airport["icao"],
      direction=direction, flight_key=str(flight_key), flight_number=str(number) if number else None,
      callsign=call, airline_name=first(airline, "name"), airline_iata=first(airline, "iata"),
      airline_icao=first(airline, "icao"), origin_iata=first(origin, "iata"), origin_icao=first(origin, "icao"),
      destination_iata=first(destination, "iata"), destination_icao=first(destination, "icao"),
      scheduled_local=scheduled_local, scheduled_utc=scheduled_utc, revised_local=revised_local,
      revised_utc=revised_utc, actual_local=actual_local, actual_utc=actual_utc, status=status_text,
      delay_minutes=minutes_between(scheduled_utc or scheduled_local, revised_utc or revised_local),
      is_cancelled=int(cancel), is_diverted=int(divert), raw_json=json.dumps(flight, ensure_ascii=False))

def api_fetch(airport, start, end, api_key):
    query = urlencode({"direction":"Both", "withLeg":"true", "withCancelled":"true", "withCodeshared":"true", "withCargo":"false", "withPrivate":"false", "withLocation":"false"})
    path = f"/flights/airports/icao/{airport['icao']}/{quote(start, safe='')}" \
           f"/{quote(end, safe='')}?{query}"
    req = Request(BASE_URL + path, headers={"X-RapidAPI-Host": HOST, "X-RapidAPI-Key": api_key, "Accept":"application/json"})
    with urlopen(req, timeout=60) as response:
        return response.status, json.loads(response.read().decode("utf-8"))

def record_run(con, airport, start, end, status, http_status, count, error=None):
    con.execute("INSERT INTO fetch_runs(started_at,finished_at,airport_iata,window_from,window_to,status,http_status,flight_count,error) VALUES(?,?,?,?,?,?,?,?,?)",
      (iso_now(), iso_now(), airport["iata"], start, end, status, http_status, count, error))

def collect(hours=12, airports=None):
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key: raise SystemExit("RAPIDAPI_KEY is not set. Copy .env.example and export your RapidAPI key.")
    selected = load_airports()
    if airports: selected = [a for a in selected if a["iata"] in {x.upper() for x in airports}]
    con = db_connect()
    con.execute("UPDATE airports SET active = 0")
    con.executemany("INSERT OR REPLACE INTO airports(iata,icao,name,timezone,active) VALUES(?,?,?,?,1)", [(a["iata"],a["icao"],a["name"],a["timezone"]) for a in selected])
    failures = 0
    now = datetime.now().astimezone()
    for airport in selected:
        local_now = now.astimezone(ZoneInfo(airport["timezone"]))
        end = local_now
        cursor = local_now - timedelta(hours=hours)
        while cursor < end:
            chunk_end = min(cursor + timedelta(hours=12), end)
            start_s, end_s = cursor.isoformat(timespec="minutes"), chunk_end.isoformat(timespec="minutes")
            print(f"{airport['iata']} {start_s}..{end_s}", flush=True)
            try:
                http_status, payload = api_fetch(airport, start_s, end_s, api_key)
                count = 0
                for direction, key in (("Departure", "departures"), ("Arrival", "arrivals")):
                    for flight in payload.get(key, []) or []:
                        row = normalize(flight, direction, airport)
                        cols = list(row); vals = [row[c] for c in cols]
                        marks = ",".join("?" for _ in cols)
                        con.execute(f"INSERT OR IGNORE INTO flight_observations({','.join(cols)}) VALUES({marks})", vals)
                        count += 1
                record_run(con, airport, start_s, end_s, "ok", http_status, count); con.commit()
            except (HTTPError, URLError, TimeoutError, ValueError) as exc:
                failures += 1
                print(f"  ERROR: {exc}", file=sys.stderr)
                record_run(con, airport, start_s, end_s, "error", getattr(exc, "code", None), 0, str(exc)); con.commit()
            cursor = chunk_end
    con.close()
    if failures:
        raise SystemExit(1)

def report(args):
    con = db_connect()
    where, values = [], []
    if args.airport: where.append("airport_iata = ?"); values.append(args.airport.upper())
    if args.cancelled: where.append("is_cancelled = 1")
    if args.delayed: where.append("delay_minutes >= ?"); values.append(args.delayed)
    if args.since: where.append("scheduled_local >= ?"); values.append(args.since)
    clause = " WHERE " + " AND ".join(where) if where else ""
    rows = con.execute(f"SELECT * FROM flight_observations{clause} ORDER BY scheduled_local LIMIT ?", values + [args.limit]).fetchall()
    for r in rows: print(f"{r['scheduled_local'] or '-':25} {r['airport_iata']:4} {r['direction']:9} {r['flight_number'] or r['callsign'] or '-':10} {r['status']:18} delay={r['delay_minutes'] or 0}m")
    print(f"{len(rows)} observation(s)")
    con.close()

def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("collect"); c.add_argument("--hours", type=int, default=12); c.add_argument("--airport", action="append", help="IATA code; repeatable"); c.set_defaults(func=lambda a: collect(a.hours, a.airport))
    r = sub.add_parser("report"); r.add_argument("--airport"); r.add_argument("--cancelled", action="store_true"); r.add_argument("--delayed", type=int, metavar="MINUTES"); r.add_argument("--since"); r.add_argument("--limit", type=int, default=100); r.set_defaults(func=report)
    i = sub.add_parser("init"); i.set_defaults(func=lambda a: initialize())
    args = p.parse_args(); args.func(args)

if __name__ == "__main__": main()
