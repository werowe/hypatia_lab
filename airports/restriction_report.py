#!/usr/bin/env python3
"""Daily Moscow-time restriction and deduplicated flight-movement reports."""
import argparse
import csv
import io
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, time, timedelta
from html import escape
from pathlib import Path
from collect_restrictions import MSK, ROOT, timestamp


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


def daily_restrictions(records, cutoff, airports=None, kind=None):
    """Union overlapping periods per airport, so an airport never exceeds 24h/day."""
    buckets = defaultdict(lambda: {'intervals': defaultdict(list), 'by_kind': defaultdict(list),
                                  'starts': 0, 'airports': set(), 'provisional': False})
    for r in records:
        if airports is not None and r['airport_iata'] not in airports:
            continue
        if kind and r['kind'] != kind:
            continue
        start = timestamp(r['start_msk'])
        if start > cutoff:
            continue
        end = min(timestamp(r['end_msk']) if r['end_msk'] else cutoff, cutoff)
        buckets[start.date()]['starts'] += 1
        cursor = start
        while cursor < end:
            midnight = datetime.combine(cursor.date() + timedelta(days=1), time(), MSK)
            stop = min(end, midnight)
            b = buckets[cursor.date()]
            b['intervals'][r['airport_iata']].append((cursor, stop))
            b['by_kind'][(r['airport_iata'], r['kind'])].append((cursor, stop))
            b['airports'].add(r['airport_iata'])
            b['provisional'] |= bool(r['ongoing'])
            cursor = stop
    output = {}
    for day, b in buckets.items():
        hours_by_kind = defaultdict(float)
        for (_, k), intervals in b['by_kind'].items():
            hours_by_kind[k] += merged_seconds(intervals) / 3600
        output[day.isoformat()] = dict(
            date=day.isoformat(), restriction_hours=sum(merged_seconds(x) for x in b['intervals'].values()) / 3600,
            restricted_hours=hours_by_kind['restricted'], partial_hours=hours_by_kind['partial'],
            restrictions_started=b['starts'], affected_airports=len(b['airports']),
            restriction_status='provisional' if b['provisional'] or day == cutoff.date() else 'completed intervals')
    return output


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


def report_data(con, config, scope='all', kind=None, cutoff=None):
    con.row_factory = sqlite3.Row
    selected = {a['iata'] for a in config}
    records = con.execute('SELECT * FROM airport_restrictions').fetchall()
    imported = con.execute('SELECT max(imported_at) FROM restriction_imports').fetchone()[0]
    if not imported:
        raise ValueError('Run collect_restrictions.py before reporting')
    # Never extrapolate ongoing restrictions beyond the last successful source fetch.
    cutoff = min(cutoff, instant(imported)) if cutoff else instant(imported)
    restrictions = daily_restrictions(records, cutoff, selected if scope == 'tracked' else None, kind)
    tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    observations = con.execute('SELECT * FROM flight_observations') if 'flight_observations' in tables else []
    flights, missing = flight_daily(observations, selected)
    intervals = defaultdict(list)
    runs = con.execute("SELECT airport_iata, window_from, window_to FROM fetch_runs WHERE status='ok'") if 'fetch_runs' in tables else []
    for run in runs:
        intervals[run['airport_iata']].append((instant(run['window_from']), instant(run['window_to'])))
    source_first = min((timestamp(r['start_msk']).date() for r in records), default=cutoff.date())
    first = min([source_first] + [datetime.fromisoformat(d).date() for d in flights])
    day = first
    rows = []
    while day <= cutoff.date():
        d = day.isoformat()
        row = restrictions.get(d, dict(date=d, restriction_hours=0., restricted_hours=0., partial_hours=0.,
                                      restrictions_started=0, affected_airports=0,
                                      restriction_status='completed intervals'))
        if day < source_first:
            row['restriction_status'] = 'outside source history'
        elif day == source_first:
            row['restriction_status'] = 'source boundary / ' + row['restriction_status']
        if day == cutoff.date():
            row['restriction_status'] = 'provisional'
        a = datetime.combine(day, time(), MSK)
        b = a + timedelta(days=1)
        coverage = [merged_seconds([(max(a, x), min(b, y)) for x, y in intervals[i] if x < b and y > a])
                    for i in selected]
        row['cancelled_movements'] = sum(flights.get(d, {}).values()) if d in flights else None
        row['flight_coverage'] = ('full requested windows' if coverage and min(coverage) >= 86400
                                  else 'partial requested windows' if any(coverage) else 'no successful fetch window')
        if day == cutoff.date():
            row['flight_coverage'] = 'provisional / ' + row['flight_coverage']
        row['cancellations_by_airport'] = flights.get(d, {})
        rows.append(row)
        day += timedelta(days=1)
    return rows, cutoff, missing


def svg_chart(rows, column, title, color):
    width, height = 960, 235
    top, bottom, left, right = 45, 192, 65, 930
    values = [r[column] for r in rows if r[column] is not None]
    maximum = max(values + [1])
    parts = [f"<svg viewBox='0 0 {width} {height}' role='img' aria-label='{escape(title)}'>",
             f"<text x='16' y='24' font-size='18'>{escape(title)}</text>"]
    for v in (0, maximum / 2, maximum):
        y = bottom - (bottom - top) * v / maximum
        parts.append(f"<path d='M{left},{y} H{right}' stroke='#ddd'/><text x='10' y='{y+4}'>{v:.1f}</text>")
    step = (right - left) / max(len(rows), 1)
    for j, row in enumerate(rows):
        value = row[column]
        x = left + j * step
        if value is not None:
            h = (bottom - top) * value / maximum
            opacity = '.45' if (column == 'cancelled_movements' and row['flight_coverage'] != 'full requested windows') or (column != 'cancelled_movements' and row['restriction_status'] != 'completed intervals') else '1'
            label = f"{row['date']}: {value:.2f}; {row['restriction_status']}; {row['flight_coverage']}"
            parts.append(f"<rect x='{x+1}' y='{bottom-h}' width='{max(step-2,1)}' height='{max(h,1)}' fill='{color}' opacity='{opacity}'><title>{escape(label)}</title></rect>")
        else:
            parts.append(f"<text x='{x}' y='{bottom-3}' fill='#777'>×</text>")
        if j % max(len(rows) // 8, 1) == 0:
            parts.append(f"<text x='{x}' y='{bottom+20}' font-size='11'>{row['date'][5:]}</text>")
    return ''.join(parts) + '</svg>'


def dashboard(con, config):
    views = []
    for scope in ('all', 'tracked'):
        kinds = [None] + [r[0] for r in con.execute('SELECT DISTINCT kind FROM airport_restrictions ORDER BY kind')]
        for kind in kinds:
            rows, cutoff, missing = report_data(con, config, scope, kind)
            label = ('All Airports.ru airports' if scope == 'all' else 'Only airports.json airports') + ' / ' + (kind or 'all kinds (union)')
            charts = ''.join(svg_chart(rows, c, t, color) for c, t, color in [
                ('restriction_hours', 'Airports.ru · daily airport restriction-hours', '#2563eb'),
                ('cancelled_movements', 'AeroDataBox · daily cancelled airport flight movements', '#dc2626'),
                ('restrictions_started', 'Airports.ru · restrictions initiated per day', '#7c3aed'),
                ('affected_airports', 'Airports.ru · distinct airports affected per day', '#0d9488')])
            table = '<table><tr><th>Moscow date</th><th>Airport-hours</th><th>Starts</th><th>Airports</th><th>Restriction totals</th><th>Cancelled movements</th><th>Flight coverage</th></tr>'
            for r in rows:
                table += '<tr>' + ''.join(f'<td>{escape(str(v))}</td>' for v in
                    (r['date'], f"{r['restriction_hours']:.2f}", r['restrictions_started'], r['affected_airports'],
                     r['restriction_status'], r['cancelled_movements'] if r['cancelled_movements'] is not None else 'unavailable', r['flight_coverage'])) + '</tr>'
            views.append((label, f'<p>Reporting cutoff: {escape(cutoff.isoformat())}. Flight observations without usable scheduled times: {missing}.</p>' + charts + table + '</table>'))
    options = ''.join(f"<option value='{i}'>{escape(label)}</option>" for i, (label, _) in enumerate(views))
    sections = ''.join(f"<section id='view-{i}' {'hidden' if i else ''}>{body}</section>" for i, (_, body) in enumerate(views))
    return '''<!doctype html><html><head><meta charset="utf-8"><title>Russian aviation disruption tracker</title>
<style>body{font:15px system-ui;margin:24px;max-width:1100px;color:#172033}svg{width:100%;font:12px system-ui}table{border-collapse:collapse;font-size:12px}td,th{padding:6px;border-bottom:1px solid #ddd;text-align:left}select{padding:10px}section[hidden]{display:none}</style></head><body>
<h1>Russian aviation disruption tracker</h1>
<p>All dates use Moscow time. Airport-hours sum time across airports, not hours of nationwide closure.
“partial” means operating with restrictions, not a complete closure. Overlaps are merged per airport.
Restrictions and cancellations are different measures, shown on aligned dates with independent scales.</p>
<p>Faded bars mark provisional restriction totals or incomplete flight windows; × means no dated flight observations.
Completed intervals remain subject to source revisions. The first history date may be incomplete.
An ongoing restriction is capped at the last successful import; refresh collection to update it.</p>
<p>Cancellations use the latest observation per scheduled airport flight movement, excluding explicit codeshares.
Arrivals and departures are separate movements; these are not unique network flights. Successful fetch windows
measure collection coverage, not the completeness of AeroDataBox reporting. This comparison does not establish the cause of restrictions.</p>
<label>Restriction airport scope and type: <select onchange="document.querySelectorAll('section').forEach((s,i)=>s.hidden=i!=this.value)">''' + options + '</select></label>' + sections + '</body></html>'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db', type=Path, default=ROOT / 'flights.sqlite3')
    p.add_argument('--airports', type=Path, default=ROOT / 'airports.json')
    p.add_argument('--scope', choices=['all', 'tracked'], default='all')
    p.add_argument('--kind')
    p.add_argument('--cutoff', help='ISO timestamp with offset; capped at last successful import')
    p.add_argument('--html', type=Path, help='Write a standalone dashboard with scope/type selectors')
    args = p.parse_args()
    with sqlite3.connect(f'file:{args.db}?mode=ro', uri=True) as con:
        config = json.loads(args.airports.read_text())
        if args.html:
            args.html.write_text(dashboard(con, config), encoding='utf-8')
        else:
            rows, cutoff, missing = report_data(con, config, args.scope, args.kind, instant(args.cutoff) if args.cutoff else None)
            print(f'# cutoff={cutoff.isoformat()} missing flight timestamps={missing}')
            writer = csv.DictWriter(__import__('sys').stdout, fieldnames=[k for k in rows[0] if k != 'cancellations_by_airport'])
            writer.writeheader()
            for row in rows:
                writer.writerow({k: round(v, 3) if isinstance(v, float) else v for k,v in row.items() if k != 'cancellations_by_airport'})


if __name__ == '__main__':
    main()
