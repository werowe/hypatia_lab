# DeepState Battlefield Change Analysis

This project downloads historical battlefield-map snapshots from DeepState,
stores every snapshot in MongoDB, and uses GeoPandas to calculate how the
occupied, contested, and liberated areas change over time.

## Contact

- 📧 [werowe@walkerrowe.com](mailto:werowe@walkerrowe.com)  
- 💻 [Analysis on Youtube ](https://www.youtube.com/watch?v=TqFHMRnLgIk)


![](https://github.com/werowe/hypatia_lab/blob/main/deepstate/screen.png)

## Data source and authorship

- **Data source:** Battlefield geometries, classifications, labels, and
  snapshot times come from
  [DeepStateMap.Live](https://deepstatemap.live/en#6/49.4383200/32.0526800).
  DeepState is the source of the underlying map data; this project does not
  create or independently verify those battlefield observations.
- **Concepts and code:** The analytical concepts, project design, and most of
  the code were written by **Walker Rowe**.
- **AI-assisted enhancement:** AI tools were used to help review, explain,
  debug, document, and enhance the analysis and code. AI assistance does not
  change the provenance of the source data or imply independent verification
  of DeepState's classifications.

Any map, table, chart, or derived number produced by this project should
therefore be described as a **Walker Rowe analysis of DeepState data, enhanced
with AI tools**.

## License and citation

Copyright © 2026 Walker Rowe. The original code and documentation in this
`deepstate` project are available under the [MIT License](LICENSE). The MIT
license requires the copyright and permission notice to be retained in copies
or substantial portions of the software.

If you use the code, analysis, maps, charts, or derived results in a public
project, article, presentation, or research work, please cite both the analysis
author and the underlying data source:

```text
Rowe, Walker (2026). DeepState Battlefield Change Analysis.
https://github.com/werowe/hypatia_lab/tree/main/deepstate
Data source: DeepStateMap.Live,
https://deepstatemap.live/en#6/49.4383200/32.0526800
AI tools were used to enhance the code and documentation.
```

Machine-readable citation metadata is provided in [`CITATION.cff`](CITATION.cff).

The MIT license applies only to original code and documentation contributed by
Walker Rowe in this project. It does **not** grant rights to DeepState's source
data, map tiles, names, trademarks, or other third-party material. Those remain
subject to their respective owners' terms. Users are responsible for checking
the terms that apply to DeepState data and any other external material.

MIT is an open-source software license, so the scholarly citation above is a
clear attribution request rather than an additional restriction on software
use. The legally required MIT attribution is preservation of the copyright
and permission notice. A mandatory publication-citation condition would
require a custom, non-standard license and would no longer be the standard MIT
license.

The main analysis notebook is `time_series_whole_country.ipynb`. Despite its
name, the notebook first searches the whole battlefield for the strongest
recent Ukrainian gain and then creates a compact local time series around that
hotspot.

## What the DeepState download contains

The downloader requests:

```text
https://deepstatemap.live/api/history/last
```

The response is a JSON document containing:

- `id`: the DeepState snapshot identifier, represented as a Unix timestamp;
- `map.features`: GeoJSON features from the current map;
- `geometry`: a Point, Polygon, MultiPolygon, or another GeoJSON geometry;
- `properties.name`: a Ukrainian label, English label, and machine-readable
  layer key separated by `///`.

The response contains more than the battlefield polygons. It can also include
military-unit markers and territory layers outside Ukraine. The analysis must
therefore select the relevant polygon layers rather than treating every feature
as battlefield territory.

The important DeepState status keys are:

| Map color | Meaning | Machine-readable key |
| --- | --- | --- |
| Red | Russian-occupied territory | `geoJSON.status.occupied` |
| Gray | Contested or unknown status | `geoJSON.status.unknown` |
| Liberated layer | Territory marked liberated | `geoJSON.status.dismissed` |

The analysis also recognizes the static Crimea and CADR/CALR territory layers
when constructing occupied geometry.

## Project workflow

```text
DeepState API
    |
    v
download_deepstate.py
    |-- saves the raw JSON snapshot in data/<epoch>.json
    `-- inserts each GeoJSON feature into MongoDB
             |
             v
       geodb.geodata
             |
             v
time_series_whole_country.ipynb
    |-- compares the latest and earlier battlefield geometry
    |-- automatically selects the strongest weekly hotspot
    |-- calculates occupied, gray, and liberated area by date
    |-- plots the local time series
    `-- displays the result on an interactive map
```

## Downloading and storing snapshots

`deepstate_download.sh` changes to the project directory and runs
`download_deepstate.py` with the Python interpreter in `tf_env`:

```bash
bash deepstate_download.sh
```

The downloader performs these operations:

1. Requests the latest DeepState snapshot.
2. Uses `data["id"]` as the snapshot's `epoch_time`.
3. Saves the complete JSON response as `data/<epoch_time>.json`.
4. Adds `epoch_time` to every feature.
5. Calculates a SHA-256 `doc_hash`.
6. Inserts the features into MongoDB collection `geodb.geodata`.

A stored document has approximately this structure:

```json
{
  "type": "Feature",
  "properties": {
    "name": "... /// Occupied /// geoJSON.status.occupied"
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": []
  },
  "epoch_time": 1786559811,
  "doc_hash": "sha256-value"
}
```

MongoDB credentials are read from `.env`:

```text
MONGODB_USER=...
MONGODB_PWD=...
CLUSTER=...
```

Do not commit `.env` or place credentials directly in Python source files.

### Why the hash includes the snapshot time

The downloader adds `epoch_time` before calculating `doc_hash`. This is
intentional for the present database design. The same unchanged polygon must be
stored once for every snapshot, or a later date would not represent a complete
map.

The unique `doc_hash` index prevents the same snapshot from being inserted
twice:

```javascript
db.geodata.createIndex({doc_hash: 1}, {unique: true})
```

The legacy `add_missing_hash.py` script removes `epoch_time` before hashing.
That is a different hash definition and should not be run against the current
collection without first reconciling the schema.

## How automatic hotspot selection works

The notebook no longer requires this hard-coded selection:

```python
area = Oleksandrivka
area_name = "Oleksandrivka"
```

Instead, `select_weekly_ukrainian_hotspot()` searches the stored snapshots.

### 1. Choose comparison dates

The newest available snapshot is selected as `latest_date`. The baseline is the
newest stored snapshot that is at least `LOOKBACK_DAYS` before the latest one:

```python
LOOKBACK_DAYS = 7
```

Because downloads are not necessarily daily, the actual interval may be more
than seven days. The notebook prints both dates.

### 2. Normalize the DeepState status labels

The notebook reads the machine-readable suffix in `properties.name` and maps
each relevant feature to:

```text
occupied
gray
liberated
```

Points and unrelated map layers are excluded from the battlefield comparison.

### 3. Project to an equal-area coordinate system

The comparison geometry is projected from latitude/longitude (`EPSG:4326`) to
European equal-area projection `EPSG:3035`. This allows areas to be measured in
square metres consistently.

### 4. Combine the source polygons

All polygons belonging to the same status and date are combined with a spatial
union. This removes the original DeepState polygon boundaries from the
analysis. A hotspot can therefore cross one or many source polygons.

### 5. Calculate the exact gained geometry

The preferred definition of a confirmed Ukrainian gain is:

```python
gain = occupied_before.intersection(liberated_latest)
```

This returns only territory that was occupied in the baseline snapshot and is
liberated in the latest snapshot. The inputs can be enormous polygons while the
result can be a sliver much smaller than 1 km².

If the occupied and liberated layers do not overlap cleanly, the notebook falls
back to:

```python
gain = liberated_latest.difference(liberated_before)
```

This represents territory appearing in the liberated layer for the first time.

### 6. Search overlapping compact windows

The notebook searches 15 km windows whose centers are spaced 5 km apart:

```python
HOTSPOT_WINDOW_KM = 15
HOTSPOT_STRIDE_KM = 5
MIN_GAIN_KM2 = 0.01
```

For every candidate window, it calculates the exact intersection with the gain
geometry:

```python
changed_m2 = gain.intersection(candidate).area
```

The full 15 km window is not counted as changed territory. It is only the
viewing and analysis region. Consequently, a 0.2 km² or 5 km² gain remains a
0.2 km² or 5 km² gain regardless of the source-polygon or window size.

Overlapping windows reduce the chance that a change will be split by an
arbitrary grid boundary. The window containing the greatest exact gained area
is selected.

### 7. Generate `area` automatically

The winning window is converted back to latitude and longitude and expressed in
the format expected by the remaining notebook cells:

```python
area = {
    "top_left": (max_lat, min_lon),
    "bottom_right": (min_lat, max_lon),
}
```

This automatically generated rectangle replaces the manually selected town or
battlefield rectangle.

## How the local time series is calculated

After selecting `area`, the notebook performs the original local analysis:

1. Creates a rectangular Shapely mask from `top_left` and `bottom_right`.
2. Clips all historical features to that rectangle.
3. Projects the clipped geometry to `EPSG:32636` for local area measurement.
4. Converts `epoch_time` to a date.
5. Groups polygon features by date.
6. Separates them into liberated, occupied, and gray groups.
7. Sums the geometry areas and divides by `1_000_000` to obtain km².
8. Calculates percentage change from the preceding stored snapshot with
   `pct_change()`.

The resulting table contains:

```text
dt
liberated
liberated Delta %
occupied
occupied Delta %
gray
gray Delta %
```

The percentage columns compare consecutive stored snapshots, not necessarily
consecutive calendar days.

### Sub-kilometre precision warning

The hotspot detector retains floating-point area and can detect changes down to
`MIN_GAIN_KM2`.

The later time-series calculation currently applies `int()` to each total:

```python
int(area_sum / 1_000_000)
```

That truncates the displayed totals to whole square kilometres. To preserve
small changes in the CSV and plot, use floating-point values instead:

```python
area_sum / 1_000_000
```

and round only when displaying the result.

## Plot and map outputs

The notebook produces:

- a table of occupied, gray, and liberated area by snapshot date;
- a logarithmic time-series plot;
- the latest full DeepState battlefield layer;
- an interactive `ipyleaflet` map;
- a yellow rectangle marking the automatically selected hotspot;
- red, gray, and blue status coloring.

The full current map is downloaded separately from the DeepState API for the
interactive display. The historical time series comes from MongoDB.

## Running the analysis

1. Download a new snapshot:

   ```bash
   cd /home/werowe/Documents/deepstate
   bash deepstate_download.sh
   ```

2. Open `time_series_whole_country.ipynb` with the `Python (tf)` kernel.

3. Run the cells from top to bottom.

4. Review the printed comparison dates, selection method, gained area, and
   generated coordinates.

5. Inspect the time-series table, plot, and interactive map.

## Interpretation and limitations

- These calculations measure changes in DeepState's published geometry. They
  are not an independent determination of battlefield control.
- DeepState may redraw, correct, or reclassify a polygon. A large calculated
  change can therefore be a source revision rather than movement on one day.
- Gray territory means contested or unknown status. It should be reported
  separately from confirmed liberated territory.
- The automatic selector reports the largest concentration inside one compact
  window. It does not imply that other parts of the front were unchanged.
- Very large or implausible changes should be checked against the raw JSON
  snapshots in `data/`.
- Only complete MongoDB snapshots should be compared. The current downloader
  does not yet maintain a separate snapshot-completeness record.

## Main files

| File | Purpose |
| --- | --- |
| `download_deepstate.py` | Downloads one snapshot and inserts it into MongoDB |
| `deepstate_download.sh` | Runs the downloader with the project Python environment |
| `create_index.js` | Creates the unique `doc_hash` index |
| `time_series_whole_country.ipynb` | Finds weekly hotspots and calculates the local time series |
| `data/*.json` | Raw downloaded DeepState snapshots |
| `geodata/` | Ukraine administrative boundary data |
| `add_missing_hash.py` | Legacy hash migration; review before use |

## Detailed explanation: how polygon overlays and the sweeping window find change

It is reasonable to ask how the notebook can locate a battlefield change when
there is no table of changes inside a DeepState polygon. The short answer is
that it does **not** infer a change by subdividing one polygon or by assuming
that some unknown part of it changed. It compares the spatial footprints in
two complete, dated map snapshots. The change is encoded by the difference
between their boundaries and status layers.

### What information a polygon actually contains

A GeoJSON battlefield feature supplies two different kinds of information:

1. Its `geometry.coordinates` define the exact footprint covered by the
   feature. Every point inside that boundary belongs to the feature for the
   purposes of the map.
2. Its `properties.name` identifies the DeepState layer, such as occupied,
   unknown, or liberated.

The polygon does not need to contain a separate record for every square metre.
In vector GIS, the boundary plus the layer classification is the information.
For example, an occupied polygon in Monday's snapshot states that its entire
mapped footprint was in the occupied layer on Monday. A liberated polygon in
the following Monday's snapshot states that its entire mapped footprint was in
the liberated layer on that later date.

This is categorical map information, not evidence about events inside the
polygon. It does not say when troops moved through each point, how the change
happened, or whether every location was surveyed independently. The notebook
can measure a change in DeepState's published classification; it cannot derive
more detailed battlefield facts than the source geometry contains.

### The source polygons are not the analysis units

The original feature boundaries may be very large, may overlap, and may change
from one download to another. The notebook first unions all features of a
given status in each comparison snapshot:

```python
occupied_before = unary_union(all_baseline_occupied_polygons)
liberated_latest = unary_union(all_latest_liberated_polygons)
```

After this union, the identity and size of each original feature no longer
matter. The result is a single occupied footprint for the baseline and a
single liberated footprint for the latest date. A source polygon is therefore
not treated as one indivisible observation, and the code never assigns the
area of a whole source polygon merely because a small part overlaps.

Shapely's overlay operations can create new boundaries wherever two inputs
cross. This is sometimes described as splitting or subdividing polygons, but
it is a calculated geometric overlay, not a claim that the source supplied
attributes for hidden sub-polygons. Each output piece inherits its meaning
from the explicit spatial question used to construct it.

### How the changed geometry is constructed

The preferred calculation is:

```python
gain = occupied_before.intersection(liberated_latest)
```

For every coordinate in the result, both of these statements are true:

- the coordinate lies inside the occupied footprint at the baseline date;
- the same coordinate lies inside the liberated footprint at the latest date.

The intersection is therefore the area whose published classification matches
an occupied-to-liberated transition. This logical test can be written as:

```text
gain(x, y) = occupied_at_baseline(x, y)
             AND liberated_at_latest(x, y)
```

No regular grid is used to estimate this shape. GEOS, the geometry engine used
by Shapely, calculates the intersections of the polygon edges and constructs
the exact vector pieces enclosed by the appropriate edges. Within normal
floating-point and source-coordinate precision, the resulting area follows
the input boundaries rather than a pixel or cell approximation.

Imagine that the baseline occupied footprint is a 100 km² polygon. In the
latest snapshot, a 2 km² liberated polygon overlaps one corner of it. The
intersection is only that 2 km² corner. The other 98 km² is not counted. It
does not matter whether the original occupied footprint was stored as one
100 km² polygon, ten 10 km² polygons, or a MultiPolygon: union followed by
intersection produces the same changed footprint when the covered geometry is
the same.

If the DeepState occupied and liberated layers do not overlap cleanly enough
to produce a confirmed transition above `MIN_GAIN_KM2`, the notebook uses:

```python
gain = liberated_latest.difference(liberated_before)
```

This second expression means "inside the latest liberated footprint but not
inside the earlier liberated footprint." It detects an addition to the
liberated layer even when the earlier occupied layer does not geometrically
cover it. This fallback is less specific: it proves a change in the published
liberated layer, but not by itself an occupied-to-liberated transition.

### The sweeping window does not create or detect the gain

The `gain` geometry is completely calculated **before** the sweeping-window
loop begins. The window's only job is to answer a different question:

> Which compact 15 km by 15 km viewing area contains the largest amount of the
> already calculated gain geometry?

The code moves the center of a square candidate window in 5 km steps across
the bounding box of `gain`. Because `AREA_CRS` is `EPSG:3035`, these distances
are metres in an equal-area projected coordinate system, rather than degrees
of longitude and latitude.

For each candidate square, the notebook first performs a fast intersection
test. Candidates that do not touch `gain` are skipped. For every candidate
that does touch it, the score is:

```python
changed_m2 = gain.intersection(candidate).area
```

This operation clips the irregular gain geometry at the square boundary and
measures only the clipped gain pieces. It does not count the 225 km² area of
the whole 15 km by 15 km square. A window containing 1.7 km² of gain receives
a score of 1.7 km², even though most of that window may contain unchanged
territory or no DeepState battlefield layer at all.

The window with the greatest score becomes `area`. Its rectangle is then used
by later notebook cells to make a local historical time series and map. Thus
there are two separate outputs that should not be confused:

- `gain` is the irregular polygon or MultiPolygon representing change between
  the two selected snapshots;
- `area` is a convenient rectangular region around the strongest
  concentration of that change.

### Why the windows overlap

If the analysis used non-overlapping 15 km grid cells, a single cluster of
change could fall across a cell boundary. Each of two neighboring cells might
then contain only half the cluster and lose to a smaller cluster elsewhere.
Moving a 15 km window in 5 km strides creates overlapping candidates and gives
the cluster several chances to lie near the middle of a candidate.

The search is still discrete. A 5 km stride does not test every possible
window center, so the returned square is the best of the tested candidates,
not a mathematical guarantee of the globally optimal square. Reducing
`HOTSPOT_STRIDE_KM` makes the location more precise but increases the number of
intersections and runtime. It does not change the underlying `gain` geometry.

### Worked conceptual example

Suppose the overlay creates three disconnected gain pieces:

```text
western piece:  0.8 km²
central piece:  1.1 km²
eastern piece:  0.6 km²
```

A western candidate window might contain all 0.8 km² of the western piece and
0.3 km² of the central piece, for a score of 1.1 km². A central candidate
might contain all 1.1 km² of the central piece plus 0.5 km² of the western
piece, for a score of 1.6 km². An eastern candidate might contain 1.4 km² in
total. The central candidate wins with 1.6 km². The code has not declared all
225 km² in that window liberated; it has only selected that window because it
contains 1.6 km² of the separately computed gain.

### What this method can and cannot establish

The method is valid only to the resolution and semantics of the source
snapshots. In particular:

- It measures changes in DeepState's drawn and classified geometry, not direct
  observations of troop positions.
- A boundary correction, delayed map update, layer redesign, or geometry error
  can appear as a calculated battlefield change.
- The result has no meaningful spatial precision beyond that of DeepState's
  coordinates and mapping process, even though Shapely returns a highly precise
  floating-point number.
- The comparison assumes that each database date is a complete snapshot with
  consistent status meanings. Missing features can produce false differences.
- The fallback `liberated_latest.difference(liberated_before)` identifies newly
  published liberated geometry, but cannot prove the earlier status of that
  geometry.
- A single baseline-to-latest comparison does not reveal the exact time of the
  transition within the interval.
- The chosen rectangle identifies the strongest concentration according to
  window size and stride. It is not a natural battlefield boundary, and other
  gains outside it are still real parts of the calculated `gain` geometry.

In summary, the polygons contain enough information to make a spatial overlay
because they specify classified footprints at known snapshot times. The
overlay derives the locations whose classifications meet the before-and-after
test. The sweeping window then ranks compact rectangles by how much of that
derived geometry they contain; it never invents finer battlefield information
inside an otherwise unclassified polygon.

## Polygon sizes, map coverage, and a defensible net-change number

### There are several different kinds of polygons

The word "polygon" can refer to three different objects in this notebook, and
they do not have the same size or purpose:

| Polygon type | Size | Meaning |
| --- | --- | --- |
| DeepState source feature | Variable; there is no fixed size | One footprint supplied by a DeepState map layer |
| Calculated `gain` piece | Variable; determined by intersecting snapshot boundaries | An irregular piece that passed a before-and-after status test |
| Sweeping candidate window | Exactly 15 km by 15 km, or 225 km² | A search and viewing square, not an assertion that its whole area changed |

The notebook's latest saved output says that it loaded 123 polygon features
from the DeepState API. Those 123 features are not 123 equal grid cells. Some
can be small local shapes, while others can represent very large continuous
territories. The notebook currently prints only category totals, not the area
of every individual source feature.

The saved full-map totals are also useful for understanding coverage:

```text
Liberated areas:  41,306 km²
Occupied areas:  117,096 km²
Gray areas:        1,631 km²
Combined:        160,033 km²
```

These values change whenever the API and notebook output are refreshed. The
combined value is only about 26.5% of Ukraine's roughly 604,000 km² national
area. Therefore, these status polygons do **not** constitute a complete
wall-to-wall subdivision of Ukraine. In particular, ordinary
Ukrainian-controlled land that has never been placed in a DeepState
"liberated" layer is generally not represented by one of these three status
totals. The API response can also contain points, military markers, static
territory layers, and polygons unrelated to the three battlefield statuses.

Consequently, "whole country" in the notebook filename means that the hotspot
search starts across all available battlefield geometry. It does not mean
that every square kilometre inside Ukraine's national boundary has been
classified as liberated, occupied, or gray.

### The search square and returned time-series rectangle are currently different sizes

Every candidate constructed inside the sweeping loop is a true 15 km by 15 km
square in `EPSG:3035`:

```text
candidate search area = 15 km × 15 km = 225 km²
```

There is, however, an important reprojection detail in the current code. It
transforms the winning square to latitude and longitude, takes the transformed
polygon's axis-aligned bounds, and returns only those four bounds. The next
cell constructs a new latitude/longitude rectangle from the bounds. Because a
projected square becomes slightly rotated relative to longitude and latitude,
its bounding rectangle is larger than the original square.

For the currently printed coordinates:

```python
{
    "top_left": (48.091857248903636, 36.54101593838309),
    "bottom_right": (47.91895293351347, 36.80103457484069),
}
```

the returned rectangle is approximately 19.4 km wide by 19.2 km high, or
373 km². Thus:

- the hotspot ranking used a 225 km² candidate square;
- the later local time series used an approximately 373 km² bounding
  rectangle;
- `gain_km2_in_window`, currently 39.72 km², measured only changed geometry
  inside the original winning search square;
- neither 225 km² nor 373 km² should be reported as the amount of land gained.

If the intended time-series mask must remain exactly 225 km², the notebook
should return the transformed winning polygon itself and clip with that
polygon, rather than discard it and reconstruct a box from its bounds.

## Interpreting the status table

The table headers mean:

| Header | Meaning in the current notebook |
| --- | --- |
| **liberated** | Total km² covered by features whose label contains "liberated" in that snapshot and rectangle |
| **liberated Δ %** | Percentage change in that total from the preceding stored snapshot |
| **occupied** | Total km² covered by features classified as occupied in that snapshot and rectangle |
| **occupied Δ %** | Percentage change in that total from the preceding stored snapshot |
| **gray** | Total km² covered by unknown/gray features in that snapshot and rectangle |
| **gray Δ %** | Percentage change in that total from the preceding stored snapshot |

The displayed heading currently says "Square Meters," but the code divides
each value by `1_000_000`. The status totals are therefore square
**kilometres**, not square metres.

The row in question is:

```text
            liberated  liberated Δ %  occupied  occupied Δ %  gray  gray Δ %
2026-08-12        127        1714.2857        97       -43.2749    51   -56.7797
```

Its preceding stored snapshot, 2026-08-10, contains:

```text
liberated = 7 km², occupied = 171 km², gray = 118 km²
```

The absolute differences are therefore:

```text
liberated: 127 -   7 = +120 km²
occupied:   97 - 171 =  -74 km²
gray:       51 - 118 =  -67 km²
```

The percentage calculations are mathematically consistent with those
integer totals:

```text
liberated: 120 /   7 × 100 = +1714.2857%
occupied:  -74 / 171 × 100 =   -43.2749%
gray:      -67 / 118 × 100 =   -56.7797%
```

The 1714% value looks extraordinary mainly because the earlier liberated
denominator is only 7 km². For a land-change report, the absolute transition
area in km² is more interpretable than a percentage calculated from a small
category total.

The current calculation also applies `int()` separately to every status
total. That truncates fractional square kilometres before the differences and
percentages are calculated. Future calculations should retain floating-point
areas internally and round only the displayed result.

### Why `liberated + occupied + gray` is not net land reclaimed

Adding the three values in one row gives the area covered by those three
published layers, subject to possible overlaps and truncation. It does not
give a direction of change:

```text
2026-08-10 covered total =   7 + 171 + 118 = 296 km²
2026-08-12 covered total = 127 +  97 +  51 = 275 km²
difference                                    -21 km²
```

If the three categories were mutually exclusive and completely covered a
fixed rectangle, their total would remain constant. Here it falls by 21 km².
That is evidence that the table is not a conserved land-accounting system.
Possible causes include unclassified space, gaps or overlaps between source
layers, boundary revisions, the larger reconstructed mask, and independent
integer truncation.

Nor can the absolute category changes simply be added:

```text
+120 - 74 - 67 = -21 km²
```

That arithmetic measures the change in the combined area covered by the three
layers. It does not measure Ukrainian gain or loss. The same square kilometre
can disappear from one category and appear in another, so the transition of
that square kilometre must be identified before it can be interpreted.

### Gray must not automatically be counted as a Ukrainian gain

The machine-readable gray status is `geoJSON.status.unknown`. It should be
treated as contested or unknown for this analysis, not as a synonym for
Ukrainian control. An increase in gray can indicate increased uncertainty or
fighting, but its direction depends on the earlier classification:

| Transition | Defensible interpretation |
| --- | --- |
| occupied → gray | Russian-occupied classification became contested/unknown; possible Ukrainian progress, but not confirmed reclamation |
| gray → liberated | Contested/unknown classification became liberated; Ukrainian progress |
| liberated → gray | Liberated classification became contested/unknown; deterioration or renewed fighting |
| gray → occupied | Contested/unknown classification became occupied; Russian progress |
| unclassified → gray | Newly mapped uncertainty/fighting; direction cannot be inferred from these layers alone |

Therefore, `gray +10 km²` is not inherently a gain. It could be favorable if
that land was previously occupied, unfavorable if it was previously
liberated, or indeterminate if it was previously unclassified. The earlier
status is essential.

## Recommended calculation for land reclaimed and land lost

A defensible calculation should compare the same coordinates at two dates and
measure explicit transitions. It should not infer transitions from differences
between three aggregate columns.

For two snapshots, first create unioned status footprints:

```python
O0 = occupied_before
G0 = gray_before
L0 = liberated_before

O1 = occupied_after
G1 = gray_after
L1 = liberated_after
```

Then calculate the transition geometries with spatial intersections. The most
conservative confirmed measures are:

```python
confirmed_reclaimed = O0.intersection(L1)
confirmed_re_lost = L0.intersection(O1)

reclaimed_km2 = confirmed_reclaimed.area / 1_000_000
lost_km2 = confirmed_re_lost.area / 1_000_000
net_confirmed_km2 = reclaimed_km2 - lost_km2
```

The result can be reported as:

```text
confirmed land reclaimed = occupied → liberated
confirmed land re-lost   = liberated → occupied
net confirmed change     = reclaimed - re-lost
```

The name `confirmed_re_lost` is deliberate. Because the DeepState liberated
layer does not represent every part of ordinary Ukrainian-controlled Ukraine,
`L0 ∩ O1` can detect land lost after appearing in the liberated layer, but it
cannot detect every Russian advance into previously Ukrainian-controlled land.

A useful additional Russian-expansion measure is:

```python
newly_occupied = O1.difference(O0)
newly_occupied_km2 = newly_occupied.area / 1_000_000
```

This reports additions to the published occupied footprint. Without a
wall-to-wall baseline control layer, however, it cannot always determine
whether that addition came from Ukrainian-controlled, gray, or previously
unclassified territory. It should therefore be called "newly mapped
occupied" rather than automatically called "Ukrainian land lost."

### Keep gray transitions as separate evidence

Instead of forcing gray into a net land-control number, report four directional
indicators alongside the confirmed metric:

```python
occupied_to_gray = O0.intersection(G1)
gray_to_liberated = G0.intersection(L1)
liberated_to_gray = L0.intersection(G1)
gray_to_occupied = G0.intersection(O1)
```

They can be grouped descriptively as:

```text
possible Ukrainian progress = occupied → gray
additional Ukrainian progress = gray → liberated
possible Ukrainian deterioration = liberated → gray
additional Russian progress = gray → occupied
```

These should remain separate from confirmed reclaimed/lost land because gray
means unknown/contested. If a single experimental "momentum" score is later
desired, weights could be assigned to these intermediate transitions, but
that would be an analytical assumption rather than a measured land area. Such
a score should never be labeled square kilometres reclaimed.

### Build a complete transition matrix

The best diagnostic output is a matrix whose rows are baseline states and
whose columns are latest states:

| Baseline → latest | Liberated | Gray | Occupied | Unclassified |
| --- | ---: | ---: | ---: | ---: |
| Liberated | unchanged liberated | renewed uncertainty | re-lost | no longer in a status layer |
| Gray | progress | unchanged gray | Russian progress | no longer in a status layer |
| Occupied | confirmed reclaimed | possible progress | unchanged occupied | no longer in a status layer |
| Unclassified | newly mapped liberated | newly mapped gray | newly mapped occupied | unchanged unclassified |

Each cell is calculated as the area of the intersection between one baseline
state and one latest state. The `Unclassified` state is the part of a fixed
analysis mask not covered by any of the three status footprints. Including it
explains area that otherwise appears or disappears from the three-column
table.

Before constructing this matrix, the code must also check whether liberated,
gray, and occupied footprints overlap within a snapshot. If they overlap, it
must either resolve them using a documented precedence rule or report the
overlap separately. Every coordinate must belong to exactly one state for the
matrix totals to conserve area.

The row shown above cannot by itself justify saying that 120 km² was reclaimed.
It establishes that the liberated layer total increased by approximately
120 km² after integer truncation. The existing hotspot overlay separately
establishes 39.72 km² of `occupied_before ∩ liberated_latest` inside the
original winning search window. A transition matrix over one fixed mask and
the same two dates is required to explain the rest and produce a sound net
number.

## Label displayed beside the hotspot boundary

The interactive map places a white, yellow-bordered label immediately above
the yellow analysis boundary. It uses the same baseline date, latest date, and
winning search window as the hotspot calculation. Its content has this form:

```text
DeepState status change · 04 Aug 2026–13 Aug 2026
UA confirmed reclaimed: 39.72 km²
RU newly mapped occupied: <calculated value> km²
Walker Rowe analysis · AI-enhanced
```

The Ukrainian number is labeled **confirmed reclaimed** only when its geometry
is `occupied_before.intersection(liberated_latest)`. If the selector has to use
the less-specific `liberated_latest.difference(liberated_before)` fallback,
the map automatically changes the wording to **newly mapped liberated**.

The Russian-side value is calculated in the same winning search window as:

```python
newly_occupied = occupied_latest.difference(occupied_before)
```

It is deliberately labeled **newly mapped occupied**, not "Russia captured,"
because the DeepState layers do not provide a complete baseline polygon for
all Ukrainian-controlled land. The label reports two separately measured
directions and does not subtract them into a potentially misleading net value.

The label also gives visible credit for the source and analysis: DeepState is
named as the status-data source, and the footer identifies this as a Walker
Rowe analysis enhanced with AI tools.
