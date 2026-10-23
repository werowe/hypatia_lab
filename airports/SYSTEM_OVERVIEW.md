# Airport reports: sources, calculations and operation

Production runs in `/home/werowe/Documents/hypatia_lab/airports` on walker-server.
The Mac source copy is `/Users/walkerrowe/Documents/hypatia_lab/airports`.
The six configured airports are SVO, DME, VKO, LED, KZN and AER. Both collectors
use Airports.ru public downloads/pages and require no paid API or API key.

## Daily process

The existing 02:17 server-time cron entry invokes `run_daily.sh`:

1. `collect_cancellations.py` downloads each airport's English delays page.
2. `collect_restrictions.py` downloads the 90-day restriction-history CSV.
3. `restriction_report.py` regenerates `dashboard.html`.

All stages are attempted. Exit statuses and errors are appended to
`airport_tracker.log`; any failed stage makes the runner return 1. The Mac and SSH
tunnel do not need to be running for collection. Notebooks are refreshed separately
with Kernel → Restart & Run All.

## Cancellation totals

The source is `https://airports.ru/en/delays/<airport>/`, with slugs configured in
`collect_cancellations.py`. A custom `airports_ru_slug` can be set in an airport's
configuration. Each source page has a seven-day completed-date history with:

- Date, without a year.
- Delayed departures and delayed arrivals.
- Cancelled flights.
- Flights with data.

The collector resolves each date against the seven completed Moscow dates before
the collection time. This handles New Year and leap days without guessing a year
from the process's local timezone. It requires the correct airport in the heading,
one history table with the expected headers, seven unique completed dates through
yesterday, and nonnegative integer counts. Stale or malformed pages fail explicitly.
Only a validated airport page is written, in one SQLite transaction.

Every run refreshes all seven days. The `(airport_iata,date_msk)` key prevents
duplicates, while newer imports update source corrections. Older stored days survive
when they leave the source window; older snapshots cannot replace newer rows.
Failures for one airport do not prevent collecting the others.

`flight_report.cancellation_report_data` reads only these source totals. It returns
independent airport-day counts, source URLs, collection timestamps and source flight
counts. Missing days, missing airports, and rows with zero flights with data are
unavailable. Explicit cancellation zeros with flight data remain zero. Reporting
availability is not a guarantee of exhaustive source coverage. Source totals are
not claimed to be deduplicated network flights or codeshare-filtered movements.
The combined total is shown only when every configured airport has usable data.

## Closure hours and events

`collect_restrictions.py` downloads
`https://airports.ru/en/history/?format=csv&period=90`. The semicolon-delimited CSV
contains airport identity, restriction kind, Moscow start/end times, minutes and
ongoing state. A validated import upserts by airport, kind and start time. A stale
ongoing row cannot reopen a completed interval, and older imported history remains
stored beyond the rolling source window.

`restriction_report.daily_restrictions` merges overlapping intervals per airport
and splits them across Moscow midnights. Duration comes from timestamps, not the
source's rounded minutes. `restricted` contributes to hours closed; `partial` means
operating with restrictions and is excluded from notebook closure totals.
Ongoing periods end at the last successful restriction import. Current-date totals
and days with ongoing intervals are provisional. Event counts are restriction
starts on that date; affected airports are distinct airports with restriction time.

Hours are summed across airports. Two airports closed for three hours contribute
six airport-hours. These data alone do not establish the cause of restrictions.

## Storage

| Table | Purpose |
| --- | --- |
| `daily_cancellations` | Per-airport/day source counts, URL and collection timestamp |
| `cancellation_fetches` | Successful and failed airport page fetch/import attempts |
| `airport_restrictions` | Restriction intervals and ongoing state |
| `restriction_imports` | Successful CSV imports and reporting cutoffs |

A pre-migration database may retain `airports`, `fetch_runs` and
`flight_observations` from AeroDataBox. New reports do not read those tables. They
are not mixed with the new cancellation totals. No API credentials are needed.

## User-facing reports

- `airport_analysis.ipynb`: one cancellation line for each of the six airports.
- `airport_closure_hours.ipynb`: total hours closed and per-airport closure hours.
- `dashboard.html`: aligned restriction-hours, cancellations, starts and affected
  airports, with scope and restriction-kind selectors.

The notebooks exclude the current Moscow day. They show up to 14 collected days;
cancellations start with seven source days and accumulate thereafter. Missing
cancellation data stays unavailable. Closure report dates depend on closure history,
not cancellation availability. Saved notebook outputs are refreshed by running the
notebook. The daily process refreshes the HTML dashboard automatically.

## Validation and limits

Run `python3 -m unittest -v test_restrictions.py test_flight_report.py`. Tests cover
HTML table validation, year rollover, leap days, corrections and retention, failure
isolation, missing versus zero counts, partial six-airport totals, notebook rendering,
closure intervals, overlaps, provisional cutoffs and daily-run failure handling.
They make no network or paid API calls.

Public-page HTML is not a documented API. Layout changes will fail collection
rather than silently write guessed counts. The source offers seven cancellation
history days, so a longer collection outage can leave an unrecoverable gap. Retained
history is not automatically revised after leaving that window. Source records and
coverage may differ from the retired AeroDataBox feed.
