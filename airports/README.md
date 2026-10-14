# Russian airport cancellation and delay tracker

See [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) for the purpose, architecture, calculations, dashboard, and production operation on walker-server.

This program polls AeroDataBox's RapidAPI airport FIDS endpoint and stores flight observations in `flights.sqlite3`. The included `airports.json` covers the principal passenger airports in Russia and is intentionally editable: add or remove airports without changing the Python code.

## Setup

1. Create a RapidAPI subscription/key for AeroDataBox.
2. In this directory, export the key:

```bash
export RAPIDAPI_KEY='your-key-here'
python3 tracker.py init
```

No third-party Python packages are required; this uses Python 3.9+ standard-library modules.

## Collect

The API allows a maximum 12-hour time window. The collector requests the previous N hours, automatically chunks the window, and uses each airport's local timezone.

```bash
python3 tracker.py collect --hours 12
python3 tracker.py collect --hours 24 --airport SVO --airport LED
```

Run it from cron/systemd every 10–30 minutes for ongoing tracking. The database contains `airports`, `fetch_runs`, and `flight_observations`; raw API payloads are retained in `flight_observations.raw_json`.

## Command-line reports

```bash
python3 tracker.py report --cancelled
python3 tracker.py report --delayed 30 --airport SVO
python3 tracker.py report --since 2026-10-02T00:00 --limit 200
```

`delay_minutes` is calculated from the scheduled and revised movement times when both are available. AeroDataBox notes that live updates depend on airport data coverage, so a missing delay does not prove that a flight was on time.

## Daily cron collection and notebook

Create the local environment file and add your RapidAPI key:

```bash
cp .env.example .env
nano .env
```

The installed daily cron job runs at 02:17 every day:

```text
17 2 * * * /home/werowe/Documents/hypatia_lab/airports/run_daily.sh
```

Output is appended to `airport_tracker.log` in this directory. The collectors update `flights.sqlite3`; rerun the notebooks below to refresh their charts.

## Daily notebook reports

Launch Jupyter from this directory so the notebooks can find `flights.sqlite3`,
`airports.json`, and the reporting modules:

```bash
python3 -m pip install -r requirements-notebook.txt
jupyter notebook
```

Use **Kernel → Restart & Run All** after each collection. Both reports read the
local database; they do not fetch new flight or closure data themselves.

| Notebook | Charts |
| --- | --- |
| [airport_analysis.ipynb](airport_analysis.ipynb) | Daily cancellations, with a separate colored line for each airport. |
| [airport_closure_hours.ipynb](airport_closure_hours.ipynb) | Total daily closure hours across the four airports, followed by a separate chart with one colored line per airport. |

The reports cover **SVO (Moscow Sheremetyevo), DME (Moscow Domodedovo),
VKO (Moscow Vnukovo), and LED (St Petersburg Pulkovo)**. Kazan (KZN) and
Sochi (AER) are excluded from the notebook charts and closure totals. The
collection configuration in `airports.json` still retains all six airports.
`REPORT_AIRPORTS` in each notebook controls the report selection.

Both reports use the same airport colors and responsive line-chart layout.
Hover over a point for the exact count or hours. Gaps mean unavailable data;
dashed segments and faded points mark provisional intervals or incomplete
collection. A zero represents no recorded event within the available data,
not proof of complete reporting.

All chart dates use **Moscow time**. The current Moscow day is excluded
automatically so incomplete daily totals do not create a misleading drop to
zero. Each report shows up to the latest **14 past days with available history**;
change `DAYS` in its setup cell to adjust the window. The reports show their
source timestamps so the freshness of collected data is visible.

Cancellations count cancelled arrivals plus departures, using the latest
observation per scheduled airport flight movement and excluding explicit
codeshares. They are disruption counts, not total airport traffic.

Closure hours include only Airports.ru **`restricted` (closed)** periods.
`partial` operating restrictions are excluded. Overlapping periods are merged
per airport and intervals crossing midnight are split by Moscow date. The
total sums hours across airports: two airports closed for three hours each
contribute **six airport-hours**. The notebook checks that the individual
airport hours sum to each daily total. Ongoing periods are counted only through
the last successful import.


API reference: https://github.com/lucasbstn/aerodatabox/blob/main/doc/FlightAPIApi.md

## Airports.ru restrictions and comparison dashboard

`collect_restrictions.py` imports the source's 90-day CSV rather than its default
30-day window. This included all available history (starting August 31, 2026)
at installation on October 8, 2026. Future imports retain older records permanently.
The CSV contains `restricted` and `partial` periods; partial periods mean operating
with restrictions and must not be interpreted as complete airport closures.

```bash
python3 collect_restrictions.py
python3 restriction_report.py --scope all
python3 restriction_report.py --scope tracked --kind restricted
python3 restriction_report.py --html dashboard.html
python3 -m unittest -v test_restrictions.py test_flight_report.py
```

The standalone `dashboard.html` is an additional, broader comparison report;
the notebooks above provide the simpler daily view. Open the dashboard in a browser.
Its selector switches between all Airports.ru airports
and airports in `airports.json`, and between restriction kinds. The four aligned
charts show airport-hours, cancelled airport flight movements, restriction starts,
and distinct airports affected. The date table exposes both sources' coverage.
AeroDataBox always covers only the configured flight airports, even when restrictions
are shown for the wider source; use the tracked scope for the closest comparison.

Hours are calculated from timestamps in Moscow time, splitting at midnight.
Overlaps are merged per airport, so the total does not double count overlapping kinds;
per-kind hours in CSV reports need not sum to the union. Source duration minutes are
retained, but not used for daily calculations because they can differ by rounding.
Ongoing periods end at the last successful import's cutoff. The cutoff day and days
containing ongoing intervals are provisional; the first source day is marked as a
history boundary. Completed intervals describe source records, not a guarantee of
complete source coverage. Faded chart bars flag these caveats; hover for detail.
This observational comparison does not establish that drone activity caused an event.

Cancelled movements use the latest observation per airport, direction, flight number,
and scheduled timestamp, assigned to scheduled Moscow date. Explicit codeshares are
excluded. A flight arriving at one tracked airport and departing another can contribute
two airport movements, so this is not a count of unique network flights. Historical
scheduled times are recovered from retained raw payloads without rewriting flight
records. Collection now extracts these times from the actual departure/arrival payload
fields. The previous-24-hour collection window remains unchanged. Requested-window
coverage is reported separately; successful API requests do not guarantee complete
flight reporting. Missing observations are displayed as unavailable.

`run_daily.sh` attempts both collectors even if either fails, regenerates the standalone
dashboard, logs each exit status, and returns failure if any stage fails. The existing
02:17 cron entry is unchanged. Restriction collection uses curl and SQLite with no
RapidAPI calls or third-party Python modules. The flight collector now returns a
nonzero status if any API window fails instead of hiding errors from the runner.

## Mac / GitHub copy

Use Python 3.9+ and curl. No environment file or API key is included in the Mac copy.
The database snapshot and generated dashboard may be present for local analysis, but
`.gitignore` excludes databases, downloaded CSVs, logs, dashboards, notebook checkpoints,
and environment files. Notebook outputs are cleared in the source copy.

For local daily collection, create `.env` from `.env.example` and use:

```bash
PYTHON_BIN=python3 ./run_daily.sh
```

The server-specific default Python path remains in place for its existing cron job.

## Independent cancellation coverage

`airport_analysis.ipynb` uses `flight_report.py` to calculate AeroDataBox
cancellations and successful request coverage separately for each airport. Its
dates and coverage labels do not depend on Airports.ru imports or closure status.
Solid lines indicate full requested windows for that airport; dashed segments
touch a day with incomplete coverage, and gaps indicate no dated observations.
A recorded zero remains distinct from unavailable data. The current Moscow day
is excluded. `airport_closure_hours.ipynb` continues to report Airports.ru closure
intervals using the restriction import cutoff. Neither notebook makes API calls.

Validate with `python3 -m unittest -v test_restrictions.py test_flight_report.py`.

## Server repository location

The production airport directory is now
`/home/werowe/Documents/hypatia_lab/airports`, inside the server's GitHub clone.
Its existing `.env`, live database, logs, downloaded data, dashboard, and backups
remain local and are excluded from Git. The old `/home/werowe/Documents/airports`
path links to the new directory for compatibility. Cron runs the new path daily
at 02:17; source updates can be installed with `git pull --ff-only` from the server's
`/home/werowe/Documents/hypatia_lab` directory.
