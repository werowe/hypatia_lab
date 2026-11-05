# Daily Ukrainian hotspot alerts

The existing 05:00 cron entry on walker-server runs `deepstate_download.sh`.
After `download_deepstate.py` exits successfully, the wrapper runs
`check_hotspot.py` with `/home/werowe/venvs/main/bin/python`. The notebook,
downloader and cron schedule are unchanged.

## Calculation and Telegram message

`hotspot_selector.py` contains the calculation ported from
`time_series_whole_country.ipynb`. Default selection preserves the notebook's
comparison and its original result fields. Settings remain a four-day
lookback, 15 km window, 5 km stride, and 0.01 km² minimum gain.

The monitor additionally excludes previously reported gain geometry when
searching for a window. This lets it find a smaller new hotspot even if an
older, larger gain is still inside the four-day comparison. A notification
requires at least 0.01 km² of unreported gain in the selected window.

Successful notifications edit message 7 in the configured Telegram channel.
Each brief message includes:

- Baseline and latest source dates, and the comparison method.
- Total gain in the selected window and the portion newly detected.
- Newly mapped occupied area and occupied-to-gray area in that window.
- The selected area's top-left and bottom-right coordinates (latitude,
  longitude), plus a DeepState map link to its center.

The opposite-direction indicators describe source-map changes; they are not
independently verified battlefield observations or a computed net gain.
Changes to the notebook calculation should also be applied to the standalone
selector, keeping the alert-specific exclusion behavior.

## First-detection tracking

The previous snapshot-date key was replaced by persistent geometry tracking
in `.hotspot_notification_state.json` (version 2, EPSG:3035, mode 0600).

- A gain already reported does not alert again merely because the source
  timestamp, comparison dates, method or selected window changes.
- After a confirmed Telegram delivery, the entire gain footprint observed in
  that comparison is acknowledged. The message describes its largest fresh
  compact hotspot; unchanged secondary hotspots do not generate later alerts.
- Unreported additions below the threshold stay unacknowledged. They can
  accumulate into a qualifying change while present in the rolling comparison.
- Acknowledged land leaving the latest liberated layer is removed from the
  cache, including during a no-gain run. If it is later regained and qualifies
  under the notebook's comparison, it can be reported again.
- An audit ledger stores the notification time, source epoch, selected bounds,
  comparison details and delivered message. It records alerts only after
  Telegram confirms success. Failed sends can be retried.
- State writes are atomic. The existing lock prevents concurrent checks.
  Dry runs neither send messages nor change the tracking state.

An old snapshot-only state file is migrated using the gain geometry from its
saved historical epoch. Unrecognized state is not silently discarded;
unreadable/corrupt state or missing history required for migration causes an
error. Back up the state with the code: deleting it loses duplicate protection
and can cause existing gains to be reported again.

No gain above the threshold, or no qualifying unreported gain, is a normal
silent result. It does not mean every frontline position is unchanged. Other
calculation, database or delivery errors exit nonzero and are recorded in
`deepstate_download.log`.

## Configuration and operation

Private `telegram.env` (mode 0600) defines `TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID`, and `TELEGRAM_MESSAGE_ID=7`. The program also accepts
`BOT_TOKEN` and `CHANNEL_ID` from the environment. Removing the message ID
selects new-message delivery instead of editing. Never put the bot token in
source files. Credentials, runtime state, lock, backups, staging and bytecode
are excluded through this repository's `.git/info/exclude`.

Preview the calculation using current tracking, without sending or saving:

```bash
cd /home/werowe/Documents/hypatia_lab/deepstate
/home/werowe/venvs/main/bin/python check_hotspot.py --dry-run
```

Run normally with conditional notification and persistent tracking:

```bash
cd /home/werowe/Documents/hypatia_lab/deepstate
/home/werowe/venvs/main/bin/python check_hotspot.py
```

Run regression checks with synthetic map changes and mocked Telegram delivery:

```bash
cd /home/werowe/Documents/hypatia_lab/deepstate
/home/werowe/venvs/main/bin/python -m unittest -v test_hotspot_notifications
```

The tests cover metrics and bounds, unchanged gains across advancing dates,
new smaller hotspots, sub-threshold additions, loss and regain, delivery
failure/retry, state migration, dry runs and persisted duplicate protection.
No real test notifications are sent. Previous deployed files are backed up
under `.hotspot_backups/`.
