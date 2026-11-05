"""Notebook hotspot calculation with optional exclusion of reported gains.

Copyright (c) 2026 Walker Rowe. SPDX-License-Identifier: MIT.
Data source: DeepStateMap.Live (https://deepstatemap.live/en).
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import box

from shapely.ops import unary_union
from shapely.prepared import prep
import numpy as np

LOOKBACK_DAYS = 4
HOTSPOT_WINDOW_KM = 15  # Size of the compact area returned
HOTSPOT_STRIDE_KM = 5   # Smaller values give a finer, slower search
MIN_GAIN_KM2 = 0.01     # Keep sub-square-kilometre changes detectable
AREA_CRS = "EPSG:3035"  # Equal-area projection suitable for Europe


class NoNewGainError(ValueError):
    """The rolling comparison has no qualifying, previously unreported gain."""

def _deepstate_status(properties):
    """Normalize a DeepState feature name to an analysis status."""
    if not isinstance(properties, dict):
        return None
    name = str(properties.get("name", "")).lower()
    # Prefer DeepState's machine-readable suffix. Looking only at the last
    # /// field loses the English label because that field is the layer key.
    if "geojson.status.dismissed" in name or "liberated" in name:
        return "liberated"
    if "geojson.status.unknown" in name or "unknown status" in name:
        return "gray"
    if (
        "geojson.status.occupied" in name
        or "geojson.territories.ordlo" in name
        or "geojson.territories.crimea" in name
    ):
        return "occupied"
    return None

def _union_status(frame, status):
    geometries = [
        geom.buffer(0)
        for geom in frame.loc[frame["status"] == status, "geometry"]
        if geom is not None and not geom.is_empty
    ]
    return unary_union(geometries) if geometries else None

def prepare_hotspot_comparison(gdf):
    """Prepare the notebook's comparison once, including tracking geometry."""
    work = gdf.dropna(subset=["geometry", "epoch_time"]).copy()
    work["dt"] = pd.to_datetime(work["epoch_time"], unit="s").dt.normalize()
    work["status"] = work["properties"].apply(_deepstate_status)
    work = work[work["status"].notna()]
    work = gpd.GeoDataFrame(work, geometry="geometry", crs="EPSG:4326")

    dates = pd.DatetimeIndex(sorted(work["dt"].unique()))
    if dates.empty:
        raise ValueError("No dated occupied/liberated snapshots are available")
    latest_date = dates[-1]
    eligible = dates[dates <= latest_date - pd.Timedelta(days=LOOKBACK_DAYS)]
    if eligible.empty:
        raise ValueError("Not enough history for the requested lookback period")
    baseline_date = eligible[-1]

    projected = work.to_crs(AREA_CRS)
    before = projected[projected["dt"] == baseline_date]
    latest = projected[projected["dt"] == latest_date]

    occupied_before = _union_status(before, "occupied")
    liberated_before = _union_status(before, "liberated")
    liberated_latest = _union_status(latest, "liberated")
    occupied_latest = _union_status(latest, "occupied")
    if occupied_before is None or liberated_latest is None:
        raise ValueError("The comparison snapshots lack occupied or liberated geometry")

    # Prefer a confirmed occupied -> liberated transition. If the source
    # layers do not overlap cleanly, fall back to newly liberated geometry.
    gain = occupied_before.intersection(liberated_latest)
    gain_method = "occupied to liberated"
    if gain.is_empty or gain.area / 1_000_000 < MIN_GAIN_KM2:
        if liberated_before is None:
            raise ValueError("No earlier liberated geometry is available")
        gain = liberated_latest.difference(liberated_before)
        gain_method = "newly liberated"
    return {
        "baseline_date": baseline_date,
        "latest_date": latest_date,
        "occupied_before": occupied_before,
        "occupied_latest": occupied_latest,
        "liberated_latest": liberated_latest,
        "gray_latest": _union_status(latest, "gray"),
        "gain": gain,
        "method": gain_method,
    }


def select_weekly_ukrainian_hotspot(gdf, *, exclude_gain=None, _comparison=None):
    """Choose the notebook's compact hotspot, optionally around new gains.

    exclude_gain is previously reported EPSG:3035 geometry. When provided,
    the window search scores only unreported land, while the original
    gain/occupied/gray fields still describe the full comparison in that window.
    """
    comparison = _comparison if _comparison is not None else prepare_hotspot_comparison(gdf)
    gain = comparison["gain"]
    if gain.is_empty or gain.area / 1_000_000 < MIN_GAIN_KM2:
        raise ValueError("No Ukrainian gain above MIN_GAIN_KM2 was found")
    search_gain = gain if exclude_gain is None else gain.difference(exclude_gain)
    if search_gain.is_empty or search_gain.area / 1_000_000 < MIN_GAIN_KM2:
        raise NoNewGainError("No previously unreported Ukrainian gain above MIN_GAIN_KM2")
    baseline_date = comparison["baseline_date"]
    latest_date = comparison["latest_date"]
    occupied_before = comparison["occupied_before"]
    occupied_latest = comparison["occupied_latest"]
    gain_method = comparison["method"]

    # Search overlapping compact windows. Scoring uses the exact vector
    # intersection area, not the size of the source polygon or grid cell.
    window_m = HOTSPOT_WINDOW_KM * 1_000
    stride_m = HOTSPOT_STRIDE_KM * 1_000
    half_window = window_m / 2
    minx, miny, maxx, maxy = search_gain.bounds
    xs = np.arange(minx, maxx + stride_m, stride_m)
    ys = np.arange(miny, maxy + stride_m, stride_m)
    prepared_gain = prep(search_gain)
    best_window = None
    best_gain_m2 = -1

    for x in xs:
        for y in ys:
            candidate = box(
                x - half_window, y - half_window,
                x + half_window, y + half_window,
            )
            if not prepared_gain.intersects(candidate):
                continue
            changed_m2 = search_gain.intersection(candidate).area
            if changed_m2 > best_gain_m2:
                best_window = candidate
                best_gain_m2 = changed_m2

    if exclude_gain is not None and best_gain_m2 / 1_000_000 < MIN_GAIN_KM2:
        raise NoNewGainError("No compact window contains MIN_GAIN_KM2 of unreported gain")

    # Measure the opposite-direction change in the same winning window.
    # This is called newly mapped occupied, rather than confirmed land lost,
    # because the source lacks a wall-to-wall Ukrainian-control layer.
    newly_occupied_m2 = 0.0
    if occupied_latest is not None:
        newly_occupied = occupied_latest.difference(occupied_before)
        if not newly_occupied.is_empty:
            newly_occupied_m2 = newly_occupied.intersection(best_window).area

    # Pressure indicator: area that was occupied at baseline and is now gray.
    # When DeepState reclassifies formerly occupied land as contested/unknown
    # it is the earliest signal that Ukraine may be contesting that ground.
    gray_latest = comparison["gray_latest"]
    occupied_to_gray_m2 = 0.0
    if gray_latest is not None:
        occ_to_gray = occupied_before.intersection(gray_latest)
        if not occ_to_gray.is_empty:
            occupied_to_gray_m2 = occ_to_gray.intersection(best_window).area

    best_window_ll = gpd.GeoSeries([best_window], crs=AREA_CRS).to_crs(4326).iloc[0]
    min_lon, min_lat, max_lon, max_lat = best_window_ll.bounds
    selected_area = {
        "top_left": (max_lat, min_lon),
        "bottom_right": (min_lat, max_lon),
    }
    details = {
        "latest_date": latest_date,
        "baseline_date": baseline_date,
        "gain_km2_in_window": gain.intersection(best_window).area / 1_000_000,
        "new_gain_km2_in_window": best_gain_m2 / 1_000_000,
        "method": gain_method,
        "newly_occupied_km2_in_window": newly_occupied_m2 / 1_000_000,
        "occupied_to_gray_km2_in_window": occupied_to_gray_m2 / 1_000_000,
    }
    return selected_area, details
