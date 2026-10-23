# Russian airport closures and cancellations

Daily reports for **SVO, DME, VKO, LED, KZN and AER**, using two free public
Airports.ru sources. No API subscription or key is needed.

- [Restriction history](https://airports.ru/en/history/?format=csv&period=90)
  supplies closure/restriction intervals and start/end times.
- [Flight delays and cancellations](https://airports.ru/en/delays/)
  supplies a seven-day table of daily cancellation totals on each airport's page.

See [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) for storage and calculation details.

## Production daily run

On walker-server:

```bash
cd /home/werowe/Documents/hypatia_lab/airports
./run_daily.sh
```

The existing cron job runs at **02:17 server time** every day:

```cron
17 2 * * * /home/werowe/Documents/hypatia_lab/airports/run_daily.sh
```

The job fetches six airport pages plus the restrictions CSV, updates
`flights.sqlite3`, and regenerates `dashboard.html`. Output goes to
`airport_tracker.log`. Both collectors run even if one fails, and any failed stage
makes the job return nonzero. Nothing calls RapidAPI or AeroDataBox.

`PYTHON_BIN` defaults to `/home/werowe/venvs/main/bin/python3`. On a different
machine, use `PYTHON_BIN=python3 ./run_daily.sh`. Collectors need Python 3.9+ and
curl; no third-party Python packages are required. The optional `.env` supports
`DATABASE_FILE` and `AIRPORTS_FILE` overrides. An old `RAPIDAPI_KEY` is ignored.

## Reports

Open Jupyter in this directory and use **Kernel → Restart & Run All**:

| Report | Contents |
| --- | --- |
| `airport_analysis.ipynb` | Daily reported cancellations, one line for each of the six airports |
| `airport_closure_hours.ipynb` | Total hours closed across six airports, followed by one line per airport |
| `dashboard.html` | Restriction-hours, cancellations, restriction starts and affected airports |

The notebooks show up to the latest 14 days collected, excluding the current
Moscow day. Initial cancellation history contains only the seven days offered
by the source; more days accumulate with daily collection. Notebook outputs refresh
when you run the notebook, independently of the daily HTML dashboard.

Closure hours include only `restricted` periods. `partial` means operating with
restrictions and is excluded from full closure hours. Overlaps are merged per
airport; midnight crossings are split by Moscow date. Two airports closed for
three hours each contribute **six airport-hours**. Ongoing closures stop at the
last successful import. The dashboard selector can also include partial restrictions;
choose `restricted` for full closure totals.

Cancellation counts are the source's published daily totals. They are not
recomputed from individual flights and do not claim to exclude codeshares or count
unique network flights. A missing airport-day is unavailable, not zero; a published
zero with flight data is zero. The combined six-airport total is unavailable if
any airport lacks a usable total for that date.

## Collection and validation commands

```bash
python3 collect_cancellations.py
python3 collect_restrictions.py
python3 restriction_report.py --scope tracked --kind restricted
python3 restriction_report.py --html dashboard.html
python3 -m unittest -v test_restrictions.py test_flight_report.py
```

The cancellation collector refreshes all seven completed Moscow dates on every
run, updating source corrections without duplicates and retaining older collected
days. It validates the airport heading, exact table headers, dates and integer
counts before writing that airport's data. A failed, stale or changed page is logged
and does not erase earlier data; the remaining airports are still attempted.
There is no documented cancellation API used here: this parses the public HTML
history table, so site layout changes can require a parser update.

`tracker.py` is a compatibility entry point to the same free collector. Older
`tracker.py collect --hours 24` commands now refresh seven completed days; `--hours`
is ignored. The former per-flight `report` and `init` commands have been retired.

## Migration from AeroDataBox

The new `daily_cancellations` table is separate from any existing AeroDataBox
`flight_observations` and `fetch_runs` tables. Reports read only Airports.ru daily
totals. Legacy records are ignored; no manual database reset is required. All
closure history remains usable. After the first successful free collection,
restart and rerun both notebooks to replace saved outputs and reload report code.

Source files live in the Mac and walker-server copies of `werowe/hypatia_lab`.
Databases, logs, `.env`, generated dashboards and backups are excluded from Git;
these runtime files do not automatically synchronize between machines. Use the
server notebooks for current production data.
