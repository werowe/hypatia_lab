#!/usr/bin/env python3
"""Import Airports.ru restriction history, using only the Python standard library."""
import argparse
import csv
import io
import logging
import os
import re
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
MSK = ZoneInfo('Europe/Moscow')
URL = 'https://airports.ru/en/history/?format=csv&period=90'
SCHEMA = '''
CREATE TABLE IF NOT EXISTS airport_restrictions (
 id INTEGER PRIMARY KEY, airport_iata TEXT NOT NULL, airport_name TEXT,
 city TEXT, kind TEXT NOT NULL, start_msk TEXT NOT NULL, end_msk TEXT,
 duration_minutes INTEGER, ongoing INTEGER NOT NULL DEFAULT 0,
 imported_at TEXT NOT NULL, UNIQUE(airport_iata, kind, start_msk)
);
CREATE TABLE IF NOT EXISTS restriction_imports (
 id INTEGER PRIMARY KEY, imported_at TEXT NOT NULL, source TEXT NOT NULL,
 record_count INTEGER NOT NULL
);
'''
COLUMNS = {'airport', 'iata', 'city', 'kind', 'start_msk', 'end_msk', 'minutes', 'ongoing'}


def timestamp(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', value):
        raise ValueError('Expected Moscow timestamp YYYY-MM-DD HH:MM')
    return datetime.strptime(value, '%Y-%m-%d %H:%M').replace(tzinfo=MSK)


def parse_csv(text):
    reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff')), delimiter=';')
    if not COLUMNS.issubset(reader.fieldnames or []):
        raise ValueError('Missing required CSV columns')
    records = []
    for line, row in enumerate(reader, 2):
        try:
            if None in row or any(row.get(c) is None for c in COLUMNS):
                raise ValueError('Malformed CSV row')
            row = {k: v.strip() for k, v in row.items()}
            iata = row['iata'].upper()
            if not re.fullmatch(r'[A-Z0-9]{3}', iata) or not row['kind']:
                raise ValueError('Missing airport IATA or kind')
            start = timestamp(row['start_msk'])
            end = timestamp(row['end_msk']) if row['end_msk'] else None
            if row['ongoing'] not in ('0', '1'):
                raise ValueError('Invalid ongoing flag')
            ongoing = int(row['ongoing'])
            if (ongoing and end) or (not ongoing and not end) or (end and end < start):
                raise ValueError('Inconsistent restriction interval')
            minutes = int(row['minutes']) if row['minutes'] else None
            if minutes is not None and minutes < 0:
                raise ValueError('Negative duration')
            # Source minutes may be rounded; daily hours use timestamps instead.
            records.append((iata, row['airport'], row['city'], row['kind'],
                            row['start_msk'], row['end_msk'] or None, minutes, ongoing))
        except (ValueError, TypeError) as exc:
            raise ValueError(f'CSV line {line}: {exc}') from exc
    if not records:
        raise ValueError('Empty history download; refusing to mark a successful import')
    return records


def download(url=URL):
    # curl is already available on the deployment host and works with this source.
    result = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                             '--max-time', '90', '--retry', '2', url],
                            capture_output=True, check=True)
    return result.stdout.decode('utf-8-sig')


def import_csv(con, text, source=URL, cutoff=None):
    records = parse_csv(text)  # Validate entire download before any database write.
    imported = (cutoff or datetime.now(timezone.utc)).isoformat(timespec='seconds')
    con.executescript(SCHEMA)
    with con:
        con.executemany('''INSERT INTO airport_restrictions
          (airport_iata,airport_name,city,kind,start_msk,end_msk,duration_minutes,ongoing,imported_at)
          VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(airport_iata,kind,start_msk) DO UPDATE SET
          airport_name=excluded.airport_name,city=excluded.city,
          end_msk=excluded.end_msk,duration_minutes=excluded.duration_minutes,
          ongoing=excluded.ongoing,imported_at=excluded.imported_at
          WHERE NOT (airport_restrictions.ongoing=0 AND excluded.ongoing=1)''',
          [r + (imported,) for r in records])
        con.execute('INSERT INTO restriction_imports(imported_at,source,record_count) VALUES(?,?,?)',
                    (imported, source, len(records)))
    return len(records)


def collect(db, url=URL, csv_file=None):
    try:
        text = Path(csv_file).read_text(encoding='utf-8-sig') if csv_file else download(url)
        with sqlite3.connect(db) as con:
            count = import_csv(con, text, str(csv_file) if csv_file else url)
        logging.info('Imported %s restriction records into %s', count, db)
        return 0
    except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as exc:
        logging.error('Restriction collection failed (%s); existing records preserved', type(exc).__name__)
        return 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db', default=os.getenv('DATABASE_FILE', str(ROOT / 'flights.sqlite3')))
    p.add_argument('--url', default=URL)
    p.add_argument('--csv-file', help='Import a saved CSV instead of downloading')
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    raise SystemExit(collect(args.db, args.url, args.csv_file))


if __name__ == '__main__':
    main()
