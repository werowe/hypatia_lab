# Russian Airport Restrictions Tracker: purpose and operation

## What it does

This project compares Russian airport restrictions with reported flight cancellations.
It helps show days when restrictions affect many airports or last for many hours,
even when relatively few flights are recorded as cancelled. The two sources measure
different things. The comparison does not establish what caused a restriction.

The production installation runs continuously on `werowe@walker-server` in
`/home/werowe/Documents/airports`. The copy in
`/Users/walkerrowe/Documents/hypatia_lab/airports` is for source control and local
analysis. Its database is a manually copied snapshot; it does not synchronize itself
with the server. GitHub contains the code, configuration example, notebook, tests,
and documentation, while the live database and credentials stay outside Git.

## Data sources and collection

**AeroDataBox through RapidAPI** supplies flight observations for the airports in
`airports.json`. The current configuration includes SVO, DME, VKO, LED, KZN, and AER.
`tracker.py` collects arrivals and departures for the previous 24 hours when invoked
by the daily runner. It divides the period into at most 12-hour API requests using
each airport's configured timezone. This preserves the existing API usage pattern.
The API key comes from the server's private `.env` file.

The collector stores status, scheduled/revised/actual times, cancellation and diversion
flags, calculated delay, and the raw response for each flight observation. Repeated
observations are retained to preserve the collection history. Each requested window
also has a success or failure record in `fetch_runs`.

**[Airports.ru restriction history](https://airports.ru/en/history/)** supplies a
semicolon-delimited CSV through
[the 90-day download](https://airports.ru/en/history/?format=csv&period=90).
`collect_restrictions.py` uses curl to fetch it and Python's standard-library
`csv.DictReader` to parse it. It makes no RapidAPI requests. The source timestamps
use Moscow time (`Europe/Moscow`, UTC+3).

The restriction collector validates all required columns, timestamps, durations,
and ongoing flags before writing any rows. Its stable key is airport IATA code,
restriction kind, and start time. Re-importing a period updates that record instead
of adding a duplicate. An ongoing record can acquire an end time when the source
publishes it; a stale ongoing record cannot reopen a completed period. Records absent
from a later download are retained. Failed downloads or invalid CSVs do not erase
previously imported history.

The initial October 8, 2026 import contained 540 records, including September history
and an earliest start of August 31. The download is a rolling 90-day window; older
records survive in SQLite after they leave that window, provided they were imported
while available. The observed kinds are `restricted` and `partial`. A partial period
means operation with restrictions and must not be interpreted as a complete closure.

## Database and files

The two sources share `flights.sqlite3` but use separate tables:

| Table | Purpose |
| --- | --- |
| `airports` | Airport configuration recorded by the flight collector |
| `fetch_runs` | Flight request windows, outcomes, and errors |
| `flight_observations` | Historical flight observations and raw API payloads |
| `airport_restrictions` | Restriction intervals, duration, kind, and ongoing status |
| `restriction_imports` | Successful restriction imports and their reporting cutoffs |

| File | Role |
| --- | --- |
| `tracker.py` | Collect flight observations and print observation reports |
| `collect_restrictions.py` | Download, validate, and upsert restriction history |
| `restriction_report.py` | Calculate daily metrics and generate the HTML dashboard |
| `airport_analysis.ipynb` | Jupyter analysis with cancellation tables and dashboard |
| `run_daily.sh` | Run collection and dashboard generation, with logging |
| `airports.json` | Airports monitored through AeroDataBox |
| `.env.example` | Template for the private server environment file |
| `requirements-notebook.txt` | Optional pandas and Jupyter dependencies |
| `test_restrictions.py` | Automated correctness and failure-handling tests |
| `.gitignore` | Exclude credentials, databases, logs, generated dashboards, and caches |

## How daily metrics work

All comparison dates use Moscow time. Restrictions crossing midnight are split:
a period from 22:00 to 04:00 contributes two airport-hours to the first date and four
to the next. Hours come from timestamps rather than the CSV's rounded `minutes` field.
Overlapping intervals are merged per airport, so one airport cannot contribute more
than 24 hours to one day. The union across kinds can be smaller than the sum of
separate restricted and partial totals.

An airport-hour sums time across airports. For example, three airports restricted
for two hours contribute six airport-hours. This is not six hours during which the
entire Russian aviation system was closed.

The daily restriction metrics are:

- Airport restriction-hours during the date.
- Number of restriction records whose start falls on the date.
- Number of distinct airports with restriction time during the date.

Ongoing periods are capped at the last successful import time, rather than extended
silently to the time the report is opened. Dates containing ongoing intervals and the
cutoff date are provisional. The first history date is marked as a source boundary.
“Completed intervals” means the stored periods have ends; it does not guarantee
that the external source recorded every event.

Daily cancellations use the latest observation for each combination of airport,
arrival/departure direction, flight number, and scheduled timestamp. Explicit
codeshare records are excluded. Historical scheduled times missing from normalized
columns are recovered from the retained raw payloads without rewriting those rows.
Future collection extracts them from the actual departure or arrival payload fields.

These are cancelled **airport flight movements**. A flight departing one tracked
airport and arriving at another can contribute two movements, so the total is not
a count of unique network flights. Flights are assigned to their scheduled Moscow
date rather than the date the tracker ran.

Successful request windows are merged to indicate flight collection coverage for
each date. Partial windows, missing dated observations, and the current cutoff date
are labeled. A successful API request does not guarantee exhaustive flight reporting.

## Dashboard and reports

`dashboard.html` is a standalone browser report with four aligned daily charts:
restriction-hours, cancelled movements, restriction starts, and affected airports.
They share calendar dates and use separate vertical scales. Faded bars identify
provisional totals or incomplete flight windows; a cross marks missing dated flight
observations. Hover text and the daily table expose the coverage labels.

The selector switches restriction scope between all Airports.ru airports and only
those in `airports.json`, and can filter by restriction kind. Flight counts always
refer to configured AeroDataBox airports. Use the tracked restriction scope for the
closest comparison between sources.

From the project directory:

```bash
python3 restriction_report.py --scope all
python3 restriction_report.py --scope tracked --kind restricted
python3 restriction_report.py --html dashboard.html
```

The first two commands print daily CSV summaries. `--cutoff` accepts an ISO timestamp
with an offset and is capped at the last successful import. Open `dashboard.html`
in a browser, or start Jupyter in the project directory and open
`airport_analysis.ipynb`. The notebook also regenerates the HTML file.
A database containing only restriction imports can generate a report with flight
coverage shown as unavailable.

Example from the initial import: September 9, 2026 contributed 158.8 airport-hours,
31 restriction starts, and 26 affected airports. Flight observations were not available
for that September date, so its cancellation value is unavailable rather than zero.

## Production automation on walker-server

The existing crontab entry remains:

```cron
17 2 * * * /home/werowe/Documents/airports/run_daily.sh
```

Cron interprets 02:17 in the server's timezone. The runner uses
`/home/werowe/venvs/main/bin/python3`, loads the private `.env`, then runs:

1. `tracker.py collect --hours 24`
2. `collect_restrictions.py`
3. `restriction_report.py --html dashboard.html`

It attempts both collectors even if one fails, logs each exit status to
`airport_tracker.log`, and returns nonzero if either collector or dashboard generation
fails. The flight collector reports failure when any API window fails. Dashboard
regeneration after a failed restriction fetch uses the prior successful import cutoff.
The scheduled process runs on the server independently of the Mac being on.

Before the extension was installed, the server code and database were backed up under
`backups/pre-restrictions-20261008-173939`. The extension preserved the existing
23,440 flight observations. This backup and runtime data are excluded from Git.

## Setup and validation

Collectors and HTML reports require Python 3.9+ and curl, with no third-party Python
packages. Jupyter analysis additionally uses the packages in
`requirements-notebook.txt`.

For a fresh installation, from the project directory:

```bash
cp .env.example .env
# Edit .env locally to supply the RapidAPI key.
# run_daily.sh loads .env; direct tracker.py commands require exported variables.
python3 tracker.py init
python3 collect_restrictions.py
python3 restriction_report.py --html dashboard.html
python3 -m unittest -v test_restrictions.py
```

On the existing server, manual collection uses `./run_daily.sh`. On another machine,
set `PYTHON_BIN=python3` when invoking it. A local run will collect into that machine's
database; it does not update the production server automatically.

The 14 automated tests cover CSV delimiters and BOMs, duplicate imports, historical
retention, ongoing completion, stale records, midnight splitting, airport-hour
calculations, overlaps, type/scope filtering, invalid timestamps, download failure,
flight deduplication, payload normalization, coverage/cutoff handling, a restriction-only
dashboard, and attempting both collectors after failure. They use synthetic data and
make no paid API calls. They passed on both server and Mac; the notebook also executed
successfully against the server database.
