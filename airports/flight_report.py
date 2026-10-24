#!/usr/bin/env python3
"""Airports.ru daily cancellation totals, independent of closure imports."""
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
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


def cancellation_report_data(con, config, as_of=None):
    """Read source daily totals without mixing in legacy flight observations.

    Missing airport-days remain None. A published zero with flight data is zero.
    These are source-reported totals; no claim of complete flight coverage is made.
    """
    con.row_factory = sqlite3.Row
    selected = {a['iata'] for a in config}
    as_of = (as_of or datetime.now(MSK)).astimezone(MSK)
    tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if 'daily_cancellations' not in tables:
        return [], None, 0
    records = [r for r in con.execute('SELECT * FROM daily_cancellations')
               if r['airport_iata'] in selected and r['date_msk'] < as_of.date().isoformat()]
    if not records:
        return [], None, 0
    latest = max(instant(r['collected_at']) for r in records).isoformat()
    by_day = defaultdict(dict)
    for record in records:
        available = record['flights_with_data'] > 0
        by_day[record['date_msk']][record['airport_iata']] = dict(
            cancelled_movements=record['cancelled'] if available else None,
            flight_coverage='source daily total' if available else 'no source flight data',
            flights_with_data=record['flights_with_data'], source_url=record['source_url'],
            collected_at=record['collected_at'])
    first, last = min(by_day), max(by_day)
    day = datetime.fromisoformat(first).date()
    rows = []
    while day.isoformat() <= last:
        date = day.isoformat()
        airports = {code: by_day[date].get(code, dict(
            cancelled_movements=None, flight_coverage='no cancellation history',
            flights_with_data=None, source_url=None, collected_at=None))
            for code in sorted(selected)}
        rows.append(dict(date=date, airports=airports))
        day += timedelta(days=1)
    return rows, latest, 0
