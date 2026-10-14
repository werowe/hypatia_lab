#!/usr/bin/env python3
"""AeroDataBox cancellations and request coverage, independent of closure imports."""
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

MSK = ZoneInfo('Europe/Moscow')


def instant(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(MSK)


def merged_seconds(intervals):
    total = 0
    end = None
    for a, b in sorted(intervals):
        if end is None or a > end:
            total += (b - a).total_seconds()
            end = b
        elif b > end:
            total += (b - end).total_seconds()
            end = b
    return total


def flight_daily(observations, airports):
    """Latest observation of each airport/direction/number/scheduled movement.

    Historical records have missing normalized times: recover from retained payloads.
    Counts are airport flight movements (arrivals/departures), not network-unique aircraft legs.
    """
    latest = {}
    missing = 0
    for r in observations:
        if r['airport_iata'] not in airports:
            continue
        raw = json.loads(r['raw_json'])
        if raw.get('codeshareStatus') == 'IsCodeshared':
            continue
        side = raw.get('movement') or raw.get('departure' if r['direction'] == 'Departure' else 'arrival') or {}
        scheduled = side.get('scheduledTime') or {}
        value = r['scheduled_utc'] or scheduled.get('utc') or r['scheduled_local'] or scheduled.get('local')
        try:
            dt = instant(value)
        except (ValueError, TypeError, AttributeError):
            missing += 1
            continue
        number = r['flight_number'] or raw.get('number') or r['flight_key']
        if isinstance(number, dict):
            number = number.get('iata') or number.get('icao') or r['flight_key']
        identity = (r['airport_iata'], r['direction'], str(number).replace(' ', '').upper(), dt.isoformat())
        if identity not in latest or (instant(r['observed_at']), r['id']) > latest[identity][0]:
            latest[identity] = ((instant(r['observed_at']), r['id']), dt.date().isoformat(), int(r['is_cancelled']))
    counts = defaultdict(lambda: defaultdict(int))
    for key, (_, day, cancelled) in latest.items():
        counts[day][key[0]] += cancelled
    return {day: dict(values) for day, values in counts.items()}, missing


def cancellation_report_data(con, config, as_of=None):
    """Return per-airport daily counts and successful requested-window coverage.

    Only flight observations and fetch_runs are read. Missing observations remain
    None even after a successful request; an observed day without cancellations
    is zero. Overlapping successful requests never inflate coverage.
    """
    con.row_factory = sqlite3.Row
    selected = {a['iata'] for a in config}
    as_of = (as_of or datetime.now(MSK)).astimezone(MSK)
    tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    observations = [r for r in con.execute('SELECT * FROM flight_observations')
                    if r['airport_iata'] in selected] if 'flight_observations' in tables else []
    counts, missing = flight_daily(observations, selected)
    runs = [r for r in con.execute('SELECT * FROM fetch_runs')
            if r['airport_iata'] in selected] if 'fetch_runs' in tables else []
    intervals = defaultdict(list)
    dates = [datetime.fromisoformat(d).date() for d in counts]
    updated = [instant(r['observed_at']) for r in observations]
    for run in runs:
        start, end = instant(run['window_from']), instant(run['window_to'])
        if end <= start:
            continue
        dates.extend([start.date(), (end - timedelta(microseconds=1)).date()])
        if run['status'] == 'ok':
            intervals[run['airport_iata']].append((start, end))
            updated.append(instant(run['finished_at'] or run['started_at']))
    last_collected = max(updated).isoformat() if updated else None
    if not dates:
        return [], last_collected, missing
    day, last = min(dates), min(max(dates), as_of.date())
    rows = []
    while day <= last:
        date = day.isoformat()
        start = datetime.combine(day, time(), MSK)
        end = start + timedelta(days=1)
        by_airport = {}
        for code in sorted(selected):
            seconds = merged_seconds([(max(start, a), min(end, b))
                                      for a, b in intervals[code] if a < end and b > start])
            coverage = ('full requested windows' if seconds >= 86400 else
                        'partial requested windows' if seconds else 'no successful fetch window')
            if day == as_of.date():
                coverage = 'provisional / ' + coverage
            by_airport[code] = dict(cancelled_movements=counts.get(date, {}).get(code),
                                    coverage_seconds=seconds, flight_coverage=coverage)
        rows.append(dict(date=date, airports=by_airport))
        day += timedelta(days=1)
    return rows, last_collected, missing
