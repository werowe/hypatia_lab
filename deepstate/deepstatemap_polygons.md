# DeepStateMap.live — Polygon Features (attributes only, no coordinates)

Source: https://deepstatemap.live/api/history/last (snapshot id **1787662201**)

⚠️ Note: This JSON feed is extremely large (mostly long coordinate arrays for each polygon).
The fetch tool truncated the response before reaching the end of the file, so the list below
covers only the **first ~35 polygon features** that were fully returned — it is *not* the
complete dataset. If you need every feature, the file would need to be downloaded directly
(e.g. via `curl`/`wget` from a machine that isn't blocked by the site's anti-bot protection —
my sandbox got a 403 trying to hit the API directly).

All `name` fields in the source data already come in the format
`Ukrainian /// English /// translation-key`, so the "English name" column below is simply the
middle part of that string.

| # | English name | Status category | Fill/stroke color | Stroke width | Notes / description |
|---|---|---|---|---|---|
| 1 | Unknown status | Статус невідомий (grey/neutral) | `#bcaaa4` | 2 | Near Bakhmut area |
| 2 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Zaporizhzhia Oblast |
| 3 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Large polygon, Kupiansk area |
| 4 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Zaporizhzhia Oblast |
| 5 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Zaporizhzhia Oblast |
| 6 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Kherson Oblast |
| 7 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Bakhmut area |
| 8 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Kherson Oblast (small) |
| 9 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Kharkiv Oblast |
| 10 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Kharkiv Oblast |
| 11 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Sumy Oblast |
| 12 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Kharkiv Oblast (small) |
| 13 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Small polygon |
| 14 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Kupiansk/Kharkiv area |
| 15 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Kharkiv Oblast |
| 16 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Kherson Oblast (small) |
| 17 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Zaporizhzhia Oblast (large) |
| 18 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Kharkiv Oblast (small) |
| 19 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Sumy Oblast (small) |
| 20 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Kharkiv Oblast (small) |
| 21 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Kharkiv Oblast (small) |
| 22 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Sumy Oblast (small) |
| 23 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Sumy Oblast (small) |
| 24 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Sumy Oblast (small) |
| 25 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Sumy Oblast (small) |
| 26 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Kharkiv Oblast (small) |
| 27 | Unknown status | grey/neutral | `#bcaaa4` | 2 | Large polygon, Kharkiv Oblast |
| 28 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Kharkiv Oblast (small) |
| 29 | Unknown status | grey/neutral | `#bcaaa4` | 1.2 | Kharkiv Oblast |
| 30 | Occupied | Окуповано (red) | `#a52714` | 1.2 | Sumy Oblast |
| 31 | Occupied | red | `#a52714` | 2 | Kharkiv Oblast (small) |
| 32 | Occupied | red | `#a52714` | 2 | Sumy Oblast (large) |
| 33 | Transnistria | Придністров'я (bright red) | `#ff5252` | 2 | Description: "Occupied in 1992 by 14th Army of Russia" (Moldova/Transnistria border region) |
| 34 | Occupied | red | `#a52714` | 1 | Very large polygon, Luhansk/Donetsk Oblasts |
| 35 | *(cut off before name/properties were returned)* | — | — | — | Polygon began near the Georgia (Caucasus) border area (~42.4°N, 44.4–44.5°E) — likely South Ossetia-related; data was truncated here |

## Common attribute schema for every feature
Each feature in the source also carries these style fields (same for all "Unknown status" polygons,
same for all "Occupied" polygons, etc.):
- `styleUrl` / `styleHash` / `styleMapHash` — internal styling identifiers
- `stroke-opacity`: 1
- `fill-opacity`: ~0.30

## Status category legend (translated)
- **Статус невідомий → Unknown status** — grey (`#bcaaa4`), contested/unclear control
- **Окуповано → Occupied** — red (`#a52714`), Russian-occupied territory
- **Придністров'я → Transnistria** — bright red (`#ff5252`), a distinctly labeled occupied territory (Moldova)
