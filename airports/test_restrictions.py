import json
import sqlite3
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
import collect_restrictions as c
import restriction_report as report

HEADER = 'airport;iata;city;kind;start_msk;end_msk;minutes;ongoing\n'
CLOSED = 'Airport;SVO;Moscow;restricted;2026-09-01 22:00;2026-09-02 04:00;360;0\n'
OPEN = 'Airport;SVO;Moscow;restricted;2026-09-01 22:00;;120;1\n'
CUTOFF = datetime(2026,9,3,tzinfo=c.MSK)

class RestrictionsTests(unittest.TestCase):
    def setUp(self):
        self.con = sqlite3.connect(':memory:')
        self.con.row_factory = sqlite3.Row
    def tearDown(self):
        self.con.close()
    def records(self):
        return self.con.execute('SELECT * FROM airport_restrictions').fetchall()
    def test_semicolon_bom_and_unicode(self):
        rows = c.parse_csv('\ufeff' + HEADER + CLOSED.replace('Moscow','Москва'))
        self.assertEqual(rows[0][2], 'Москва')
    def test_duplicate_import_and_history_preserved(self):
        c.import_csv(self.con, HEADER+CLOSED)
        c.import_csv(self.con, HEADER+CLOSED)
        c.import_csv(self.con, HEADER+CLOSED.replace('SVO','DME'))
        self.assertEqual(len(self.records()), 2)
    def test_ongoing_closes_and_stale_open_cannot_reopen(self):
        c.import_csv(self.con, HEADER+OPEN)
        c.import_csv(self.con, HEADER+CLOSED)
        c.import_csv(self.con, HEADER+OPEN)
        r = self.records()[0]
        self.assertEqual((r['ongoing'],r['end_msk']), (0,'2026-09-02 04:00'))
    def test_midnight_and_airport_hours(self):
        c.import_csv(self.con, HEADER+CLOSED+CLOSED.replace('SVO','DME'))
        days = report.daily_restrictions(self.records(), CUTOFF)
        self.assertEqual(days['2026-09-01']['restriction_hours'], 4)
        self.assertEqual(days['2026-09-02']['restriction_hours'], 8)
        self.assertEqual(days['2026-09-01']['restrictions_started'], 2)
        self.assertEqual(days['2026-09-02']['restrictions_started'], 0)
        self.assertEqual(days['2026-09-02']['affected_airports'], 2)
    def test_ongoing_cutoff_and_filter(self):
        c.import_csv(self.con,HEADER+OPEN)
        d=report.daily_restrictions(self.records(), datetime(2026,9,2,1,tzinfo=c.MSK))
        self.assertEqual(d['2026-09-02']['restriction_hours'],1)
        self.assertEqual(d['2026-09-01']['restriction_status'],'provisional')
        self.assertEqual(report.daily_restrictions(self.records(),CUTOFF,{'DME'}),{})
    def test_overlap_and_kind(self):
        c.import_csv(self.con,HEADER+CLOSED+CLOSED.replace('restricted','partial'))
        d=report.daily_restrictions(self.records(),CUTOFF)
        self.assertEqual(d['2026-09-01']['restriction_hours'],2)
        self.assertEqual(d['2026-09-01']['partial_hours'],2)
        self.assertEqual(report.daily_restrictions(self.records(),CUTOFF,kind='partial')['2026-09-02']['restriction_hours'],4)
    def test_invalid_timestamps_and_atomic_validation(self):
        c.import_csv(self.con,HEADER+CLOSED)
        for row in [CLOSED.replace('2026-09-01 22:00',''), CLOSED.replace('2026-09-01','2026-02-30'),
                    CLOSED.replace('2026-09-02 04:00',''), CLOSED.replace('2026-09-02','2026-08-31')]:
            with self.assertRaises(ValueError):
                c.import_csv(self.con,HEADER+CLOSED.replace('SVO','DME')+row)
        self.assertEqual(len(self.records()),1)
    def test_missing_columns_and_empty(self):
        for text in ['airport;iata\na;SVO\n',HEADER]:
            with self.assertRaises(ValueError): c.parse_csv(text)
    def test_failed_download_preserves_database(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/'test.sqlite3'
            with sqlite3.connect(db) as con: c.import_csv(con,HEADER+CLOSED)
            with patch.object(c,'download',side_effect=subprocess.CalledProcessError(22,['curl'])):
                self.assertEqual(c.collect(db),1)
            with sqlite3.connect(db) as con:
                self.assertEqual(con.execute('SELECT count(*) FROM airport_restrictions').fetchone()[0],1)
    def test_restriction_only_database_dashboard(self):
        c.import_csv(self.con,HEADER+CLOSED,cutoff=CUTOFF)
        html = report.dashboard(self.con,[{'iata':'SVO'}])
        self.assertIn('no cancellation history',html)
        self.assertIn('Only airports.json airports',html)

    def test_daily_runner_attempts_both_collectors_on_failure(self):
        import shutil
        for failed in ('collect_cancellations.py', 'collect_restrictions.py'):
            with tempfile.TemporaryDirectory() as d:
                root = Path(d)
                shutil.copy(Path(c.__file__).parent / 'run_daily.sh', root / 'run_daily.sh')
                stub = root / 'python-stub'
                stub.write_text('#!/bin/sh\necho "$1" >> "' + str(root / 'calls') + '"\ncase "$1" in *' + failed + ') exit 1;; esac\nexit 0\n')
                stub.chmod(0o755)
                import os
                result = subprocess.run(['bash', str(root / 'run_daily.sh')], env=dict(os.environ, PYTHON_BIN=str(stub)), capture_output=True)
                self.assertEqual(result.returncode, 1)
                calls = (root / 'calls').read_text()
                self.assertIn('collect_cancellations.py', calls)
                self.assertIn('collect_restrictions.py', calls)
                self.assertIn('restriction_report.py', calls)

    def test_stale_closure_cutoff(self):
        c.import_csv(self.con,HEADER+CLOSED,cutoff=CUTOFF)
        rows,cutoff,_=report.report_data(self.con,[{'iata':'SVO'}],cutoff=datetime(2026,10,1,tzinfo=c.MSK))
        self.assertEqual(cutoff,CUTOFF)
        self.assertEqual(rows[0]['flight_coverage'],'no cancellation history')

if __name__=='__main__': unittest.main()
