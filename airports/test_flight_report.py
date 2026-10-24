import json
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import collect_cancellations as collector
import flight_report as report
import restriction_report

NOW = datetime(2026, 10, 23, 12, tzinfo=report.MSK)


def history(code='SVO', now=NOW, cancelled=3, flights=100):
    rows = ['<h1>Airport (' + code + '): flight delays today</h1><table><tr>' +
            ''.join('<th>' + s + '</th>' for s in collector.HEADERS) + '</tr>']
    for i in range(7, 0, -1):
        day = now.date() - timedelta(days=i)
        cells = [day.strftime('%d.%m %a'), '10', '20', str(cancelled), str(flights)]
        rows.append('<tr>' + ''.join('<td><span>' + c + '</span></td>' for c in cells) + '</tr>')
    return ''.join(rows) + '</table>'


class DatabaseCase(unittest.TestCase):
    def setUp(self):
        self.con = sqlite3.connect(':memory:')

    def tearDown(self):
        self.con.close()

    def insert(self, code='SVO', **kwargs):
        return collector.import_history(self.con, history(code=code, **kwargs), code,
                                        'https://airports.ru/test/', kwargs.get('now', NOW))


class CollectorTests(DatabaseCase):
    def test_history_extracts_seven_completed_dates_and_counts(self):
        rows = collector.parse_history(history(), 'SVO', NOW)
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[-1], ('2026-10-22', 10, 20, 3, 100))

    def test_year_rollover_and_leap_day(self):
        for now, expected in [(datetime(2027, 1, 2, tzinfo=report.MSK), '2026-12-26'),
                              (datetime(2028, 3, 1, tzinfo=report.MSK), '2028-02-23')]:
            rows = collector.parse_history(history(now=now), 'SVO', now)
            self.assertEqual(rows[0][0], expected)
            self.assertEqual(rows[-1][0], (now.date() - timedelta(days=1)).isoformat())

    def test_invalid_or_stale_pages_are_rejected_without_writes(self):
        self.insert()
        bad_pages = [history('DME'), history().replace('Cancelled', 'Missing'),
                     history().replace('22.10', '01.10'),
                     history().replace('<span>3</span>', '<span>-1</span>'),
                     history().replace('<span>3</span>', '<span>unknown</span>'),
                     history().replace('22.10', '21.10'), '<html>Unavailable</html>']
        for page in bad_pages:
            with self.assertRaises(ValueError):
                collector.import_history(self.con, page, 'SVO', 'test', NOW)
        self.assertEqual(self.con.execute('SELECT count(*),sum(cancelled) FROM daily_cancellations').fetchone(), (7, 21))

    def test_corrections_upsert_and_older_history_is_retained(self):
        self.insert()
        self.insert(now=NOW + timedelta(days=1), cancelled=4)
        self.assertEqual(self.con.execute('SELECT count(*) FROM daily_cancellations').fetchone()[0], 8)
        self.assertEqual(self.con.execute("SELECT cancelled FROM daily_cancellations WHERE date_msk='2026-10-22'").fetchone()[0], 4)
        self.insert()
        self.assertEqual(self.con.execute("SELECT cancelled FROM daily_cancellations WHERE date_msk='2026-10-22'").fetchone()[0], 4)

    def test_download_failure_is_recorded_other_airports_still_collected(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / 'flights.sqlite3'
            with patch.object(collector, 'download', side_effect=[TimeoutError('unreachable'), history('DME')]):
                self.assertEqual(collector.collect(db, [{'iata':'SVO'}, {'iata':'DME'}], NOW), 1)
            with sqlite3.connect(db) as con:
                self.assertEqual(con.execute('SELECT airport_iata,status FROM cancellation_fetches ORDER BY id').fetchall(), [('SVO','error'), ('DME','ok')])
                self.assertEqual(con.execute('SELECT count(*) FROM daily_cancellations').fetchone()[0], 7)


class CancellationReportTests(DatabaseCase):
    def data(self):
        return report.cancellation_report_data(self.con, [{'iata':'SVO'}, {'iata':'DME'}], NOW)

    def test_published_zero_is_distinct_from_missing_airport(self):
        self.insert(cancelled=0)
        rows, updated, _ = self.data()
        self.assertEqual(rows[-1]['airports']['SVO']['cancelled_movements'], 0)
        self.assertIsNone(rows[-1]['airports']['DME']['cancelled_movements'])
        self.assertEqual(updated, NOW.isoformat(timespec='seconds'))

    def test_no_flight_data_does_not_turn_into_zero_cancellations(self):
        self.insert(cancelled=0, flights=0)
        self.assertIsNone(self.data()[0][-1]['airports']['SVO']['cancelled_movements'])

    def test_reports_ignore_legacy_data_and_need_no_closure_tables(self):
        self.con.executescript('CREATE TABLE flight_observations(dummy INTEGER); INSERT INTO flight_observations VALUES(999);')
        self.assertEqual(self.data(), ([], None, 0))
        self.insert()
        self.assertEqual(self.data()[0][-1]['airports']['SVO']['cancelled_movements'], 3)

    def test_aggregate_total_requires_all_airports(self):
        import collect_restrictions as restrictions
        restrictions.import_csv(self.con, 'airport;iata;city;kind;start_msk;end_msk;minutes;ongoing\nAirport;SVO;Moscow;restricted;2026-10-22 01:00;2026-10-22 02:00;60;0\n', cutoff=NOW)
        self.insert()
        config = [{'iata':'SVO'}, {'iata':'DME'}]
        rows, _, _ = restriction_report.report_data(self.con, config)
        day = next(r for r in rows if r['date']=='2026-10-22')
        self.assertIsNone(day['cancelled_movements'])
        self.assertEqual(day['flight_coverage'], 'available for 1/2 airports')
        self.insert(code='DME', cancelled=0)
        rows, _, _ = restriction_report.report_data(self.con, config)
        day = next(r for r in rows if r['date']=='2026-10-22')
        self.assertEqual(day['cancelled_movements'], 3)
        self.assertEqual(day['flight_coverage'], 'source daily totals')

    def test_notebook_renders_six_airports_without_closures_or_paid_data(self):
        now = datetime.now(report.MSK)
        config = json.loads((Path(__file__).parent / 'airports.json').read_text())
        for airport in config:
            self.insert(code=airport['iata'], now=now)
        notebook = json.loads((Path(__file__).parent / 'airport_analysis.ipynb').read_text())
        rendered = []
        module = ModuleType('IPython.display')
        module.HTML = lambda value: value
        module.display = rendered.append
        old_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            with sqlite3.connect(str(Path(tmp) / 'flights.sqlite3')) as target:
                self.con.commit()
                self.con.backup(target)
            (Path(tmp) / 'airports.json').write_text(json.dumps(config))
            try:
                os.chdir(tmp)
                # Simulate an open Jupyter kernel retaining the old report function.
                with patch.dict(sys.modules, {'IPython': ModuleType('IPython'), 'IPython.display': module}), \
                     patch.object(report, 'cancellation_report_data', side_effect=AssertionError('stale report function')):
                    namespace = {}
                    for cell in notebook['cells']:
                        if cell['cell_type']=='code':
                            exec(compile(''.join(cell['source']), 'airport_analysis.ipynb', 'exec'), namespace)
            finally:
                os.chdir(old_cwd)
        html = ''.join(rendered)
        for airport in config:
            self.assertIn(airport['iata'] + ': 3 cancellations', html)
        self.assertIn('Airports.ru cancellations last collected', html)
        self.assertNotIn('AeroDataBox', html)


if __name__ == '__main__':
    unittest.main()
