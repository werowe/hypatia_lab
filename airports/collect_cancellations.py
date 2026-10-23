#!/usr/bin/env python3
"""Collect Airports.ru's completed-day cancellation totals without an API key."""
import argparse
import json
import logging
import os
import re
import sqlite3
import subprocess
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path

from collect_restrictions import MSK, ROOT

SLUGS = dict(SVO='sheremetyevo', DME='domodedovo', VKO='vnukovo',
             LED='saint-petersburg', KZN='kazan', AER='sochi')
HEADERS = ['Date', 'Delayed departures', 'Delayed arrivals', 'Cancelled', 'Flights with data']
SCHEMA = '''
CREATE TABLE IF NOT EXISTS daily_cancellations (
 airport_iata TEXT NOT NULL, date_msk TEXT NOT NULL,
 delayed_departures INTEGER NOT NULL CHECK(delayed_departures >= 0),
 delayed_arrivals INTEGER NOT NULL CHECK(delayed_arrivals >= 0),
 cancelled INTEGER NOT NULL CHECK(cancelled >= 0),
 flights_with_data INTEGER NOT NULL CHECK(flights_with_data >= 0),
 source_url TEXT NOT NULL, collected_at TEXT NOT NULL,
 PRIMARY KEY(airport_iata, date_msk)
);
CREATE TABLE IF NOT EXISTS cancellation_fetches (
 id INTEGER PRIMARY KEY, airport_iata TEXT NOT NULL, collected_at TEXT NOT NULL,
 status TEXT NOT NULL, record_count INTEGER NOT NULL, error TEXT
);
'''


class HistoryParser(HTMLParser):
    """Extract visible table cells and the airport heading, ignoring page scripts."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None
        self.headings = []
        self.heading = None
        self.ignored = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.ignored += 1
        if tag == 'h1':
            self.heading = []
        if tag == 'table':
            if self.table is not None:
                raise ValueError('Unexpected nested table')
            self.table = []
        elif tag == 'tr' and self.table is not None:
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.ignored:
            return
        if self.heading is not None:
            self.heading.append(data)
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.ignored = max(0, self.ignored - 1)
        elif tag == 'h1' and self.heading is not None:
            self.headings.append(' '.join(''.join(self.heading).split()))
            self.heading = None
        elif tag in ('td', 'th') and self.cell is not None:
            self.row.append(' '.join(''.join(self.cell).split()))
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == 'table' and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def parse_history(html, airport, collected_at):
    parser = HistoryParser()
    parser.feed(html)
    if not any(f'({airport})' in heading for heading in parser.headings):
        raise ValueError(f'Expected airport heading ({airport})')
    tables = [t for t in parser.tables if t and t[0] == HEADERS]
    if len(tables) != 1:
        raise ValueError('Expected one daily cancellation history table')
    today = collected_at.astimezone(MSK).date()
    expected = {today - timedelta(days=i) for i in range(1, 8)}
    rows = {}
    for cells in tables[0][1:]:
        if len(cells) != len(HEADERS):
            raise ValueError('Unexpected daily history columns')
        match = re.fullmatch(r'(\d{2})\.(\d{2})\s+\S+', cells[0])
        if not match:
            raise ValueError('Expected history date DD.MM weekday')
        candidates = [d for d in expected if (d.day, d.month) == tuple(map(int, match.groups()))]
        if len(candidates) != 1:
            raise ValueError(f'Stale or unexpected history date: {cells[0]}')
        day = candidates[0]
        if day in rows:
            raise ValueError('Duplicate history date')
        values = []
        for value in cells[1:]:
            if not re.fullmatch(r'(?:\d+|\d{1,3}(?: \d{3})+)', value):
                raise ValueError('Expected nonnegative integer history count')
            values.append(int(value.replace(' ', '')))
        rows[day] = (day.isoformat(), *values)
    if set(rows) != expected:
        raise ValueError('Expected all seven completed Moscow dates through yesterday')
    return [rows[d] for d in sorted(rows)]


def download(url):
    result = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                             '--max-time', '30', '--retry', '1', url],
                            capture_output=True, check=True)
    return result.stdout.decode('utf-8-sig')


def import_history(con, html, airport, url, collected_at):
    rows = parse_history(html, airport, collected_at)
    stamp = collected_at.astimezone(MSK).isoformat(timespec='seconds')
    con.executescript(SCHEMA)
    with con:
        con.executemany('''INSERT INTO daily_cancellations
          (airport_iata,date_msk,delayed_departures,delayed_arrivals,cancelled,
           flights_with_data,source_url,collected_at) VALUES(?,?,?,?,?,?,?,?)
          ON CONFLICT(airport_iata,date_msk) DO UPDATE SET
          delayed_departures=excluded.delayed_departures,
          delayed_arrivals=excluded.delayed_arrivals,cancelled=excluded.cancelled,
          flights_with_data=excluded.flights_with_data,
          source_url=excluded.source_url,collected_at=excluded.collected_at
          WHERE excluded.collected_at >= daily_cancellations.collected_at''',
          [(airport, *r, url, stamp) for r in rows])
        con.execute('''INSERT INTO cancellation_fetches
          (airport_iata,collected_at,status,record_count) VALUES(?,?,?,?)''',
          (airport, stamp, 'ok', len(rows)))
    return len(rows)


def collect(db, config, collected_at=None):
    collected_at = collected_at or datetime.now(MSK)
    failures = 0
    with sqlite3.connect(db) as con:
        con.executescript(SCHEMA)
        for airport in config:
            code = airport['iata']
            try:
                slug = airport.get('airports_ru_slug') or SLUGS.get(code)
                if not slug or not re.fullmatch(r'[a-z0-9-]+', slug):
                    raise ValueError(f'No valid Airports.ru slug for {code}')
                url = f'https://airports.ru/en/delays/{slug}/'
                count = import_history(con, download(url), code, url, collected_at)
                logging.info('%s: imported %s daily cancellation totals', code, count)
            except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as exc:
                failures += 1
                logging.error('%s: cancellation collection failed: %s', code, exc)
                with con:
                    con.execute('''INSERT INTO cancellation_fetches
                      (airport_iata,collected_at,status,record_count,error) VALUES(?,?,?,?,?)''',
                      (code, collected_at.isoformat(timespec='seconds'), 'error', 0, str(exc)))
    return int(bool(failures))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=os.getenv('DATABASE_FILE', ROOT / 'flights.sqlite3'))
    parser.add_argument('--airports', type=Path, default=os.getenv('AIRPORTS_FILE', ROOT / 'airports.json'))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    raise SystemExit(collect(args.db, json.loads(args.airports.read_text())))


if __name__ == '__main__':
    main()
