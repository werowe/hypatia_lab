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

## Reports

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
17 2 * * * /home/werowe/Documents/airports/run_daily.sh
```

Output is appended to `airport_tracker.log` in this directory. Open `airport_analysis.ipynb` with Jupyter for tables and dependency-light inline SVG charts. The notebook reads directly from `flights.sqlite3` and will show an empty-state message until collection has succeeded.

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
python3 -m unittest -v test_restrictions.py
```

Open `dashboard.html` in a browser or launch `airport_analysis.ipynb` from this
project directory. The dashboard selector switches between all Airports.ru airports
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
