import json
import sqlite3
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import flight_report as report
import tracker


class CancellationCoverageTests(unittest.TestCase):
    def setUp(self):
        self.con = sqlite3.connect(':memory:')
        self.con.executescript(tracker.SCHEMA)
        self.config = [{'iata': 'SVO'}, {'iata': 'DME'}]
        self.as_of = datetime(2026, 10, 14, 7, tzinfo=report.MSK)

    def tearDown(self):
        self.con.close()

    def run_window(self, code, start, end, status='ok'):
        self.con.execute('INSERT INTO fetch_runs(airport_iata,started_at,finished_at,window_from,window_to,status) '
                         'VALUES(?,?,?,?,?,?)', (code, end, end, start, end, status))

    def observation(self, code, cancelled=0):
        airport = dict(iata=code, icao='TEST', name='Test', timezone='Europe/Moscow')
        flight = dict(number=code + '1', status='Canceled' if cancelled else 'Arrived',
                      arrival={'scheduledTime': {'utc': '2026-10-12T22:00:00Z'}})
        row = tracker.normalize(flight, 'Arrival', airport)
        row['observed_at'] = '2026-10-14T02:17:00+03:00'
        self.con.execute('INSERT INTO flight_observations(' + ','.join(row) + ') VALUES(' +
                         ','.join('?' for _ in row) + ')', list(row.values()))

    def data(self):
        return report.cancellation_report_data(self.con, self.config, as_of=self.as_of)

    def test_coverage_is_per_airport_and_needs_no_closure_tables(self):
        self.run_window('SVO', '2026-10-13T00:00+03:00', '2026-10-14T00:00+03:00')
        self.run_window('DME', '2026-10-13T12:00+03:00', '2026-10-14T00:00+03:00')
        self.observation('SVO', 1)
        self.observation('DME')
        row = self.data()[0][0]['airports']
        self.assertEqual(row['SVO']['flight_coverage'], 'full requested windows')
        self.assertEqual(row['DME']['flight_coverage'], 'partial requested windows')
        self.assertEqual(row['SVO']['cancelled_movements'], 1)
        self.assertEqual(row['DME']['cancelled_movements'], 0)

    def test_stale_or_ongoing_closures_do_not_change_flight_report(self):
        self.observation('SVO', 1)
        before = self.data()
        self.con.executescript('CREATE TABLE restriction_imports(imported_at TEXT); '
                              "INSERT INTO restriction_imports VALUES('2026-09-01T00:00:00Z'); "
                              'CREATE TABLE airport_restrictions(ongoing INTEGER); '
                              'INSERT INTO airport_restrictions VALUES(1);')
        self.assertEqual(self.data(), before)
        self.assertEqual(before[0][0]['date'], '2026-10-13')

    def test_zero_and_missing_observations_are_distinct(self):
        self.observation('SVO')
        self.run_window('DME', '2026-10-13T00:00+03:00', '2026-10-14T00:00+03:00')
        row = self.data()[0][0]['airports']
        self.assertEqual(row['SVO']['cancelled_movements'], 0)
        self.assertIsNone(row['DME']['cancelled_movements'])

    def test_overlaps_do_not_inflate_coverage_and_errors_do_not_count(self):
        for _ in range(2):
            self.run_window('SVO', '2026-10-13T00:00+03:00', '2026-10-13T12:00+03:00')
        self.run_window('SVO', '2026-10-13T12:00+03:00', '2026-10-14T00:00+03:00', 'error')
        row = self.data()[0][0]['airports']['SVO']
        self.assertEqual(row['coverage_seconds'], 43200)
        self.assertEqual(row['flight_coverage'], 'partial requested windows')

    def test_missing_days_and_midnight_boundaries(self):
        self.run_window('SVO', '2026-10-10T21:00Z', '2026-10-11T21:00Z')
        self.run_window('SVO', '2026-10-12T21:00Z', '2026-10-13T21:00Z')
        rows = self.data()[0]
        self.assertEqual([r['date'] for r in rows], ['2026-10-11', '2026-10-12', '2026-10-13'])
        self.assertEqual(rows[0]['airports']['SVO']['coverage_seconds'], 86400)
        self.assertEqual(rows[1]['airports']['SVO']['coverage_seconds'], 0)

    def test_current_day_is_provisional_using_flight_clock(self):
        self.run_window('SVO', '2026-10-14T00:00+03:00', '2026-10-14T02:17+03:00')
        row = self.data()[0][0]
        self.assertEqual(row['date'], '2026-10-14')
        self.assertEqual(row['airports']['SVO']['flight_coverage'],
                         'provisional / partial requested windows')

    def test_empty_database(self):
        self.assertEqual(self.data(), ([], None, 0))

    def test_notebook_renders_independent_airport_lines_without_closures(self):
        today = datetime.now(report.MSK).date()
        first = today - timedelta(days=2)
        for code in ('SVO', 'DME'):
            for offset in (0, 1):
                day = first + timedelta(days=offset)
                start = datetime.combine(day, datetime.min.time(), report.MSK)
                end = start + timedelta(days=1)
                self.run_window(code, (start if code == 'SVO' else start + timedelta(hours=12)).isoformat(), end.isoformat())
                row = tracker.normalize({'number': code + str(offset), 'status': 'Canceled',
                                         'arrival': {'scheduledTime': {'local': (start + timedelta(hours=13)).isoformat()}}},
                                        'Arrival', dict(iata=code, icao='TEST', name=code, timezone='Europe/Moscow'))
                self.con.execute('INSERT INTO flight_observations(' + ','.join(row) + ') VALUES(' +
                                 ','.join('?' for _ in row) + ')', list(row.values()))
        nb = json.loads((Path(__file__).parent / 'airport_analysis.ipynb').read_text())
        rendered = []
        display_module = ModuleType('IPython.display')
        display_module.HTML = lambda value: value
        display_module.display = rendered.append
        old_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            with sqlite3.connect(str(Path(tmp) / 'flights.sqlite3')) as target:
                self.con.commit()
                self.con.backup(target)
            (Path(tmp) / 'airports.json').write_text(json.dumps([dict(iata=code, name=code) for code in ('SVO', 'DME')]))
            try:
                os.chdir(tmp)
                namespace = {}
                with patch.dict(sys.modules, {'IPython': ModuleType('IPython'), 'IPython.display': display_module}):
                    for cell in nb['cells']:
                        if cell['cell_type'] == 'code':
                            exec(compile(''.join(cell['source']), 'airport_analysis.ipynb', 'exec'), namespace)
            finally:
                os.chdir(old_cwd)
        html = ''.join(rendered)
        self.assertIn('stroke="#2563eb" stroke-width="2.5"/>', html)
        self.assertNotIn('stroke="#2563eb" stroke-width="2.5" stroke-dasharray', html)
        self.assertIn('stroke="#ea580c" stroke-width="2.5" stroke-dasharray="6 4"', html)
        self.assertNotIn('Closures last imported', html)


if __name__ == '__main__':
    unittest.main()
