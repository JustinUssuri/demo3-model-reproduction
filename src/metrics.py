from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def compute_dc_ac_errors(dc: Any, ac: Any) -> dict:
    """Compute absolute and relative errors between DC and AC flows."""
    dc_df = pd.DataFrame(dc)
    ac_df = pd.DataFrame(ac)
    dc_df, ac_df = dc_df.align(ac_df, join="inner", axis=None)

    abs_error = (dc_df - ac_df).abs()
    denom = ac_df.abs()
    eps = 1e-9
    rel_error = abs_error.div(denom)
    # Treat zero/near-zero AC flow as undefined relative error.
    rel_error = rel_error.mask(denom <= eps)

    abs_vals = abs_error.to_numpy()
    rel_vals = rel_error.to_numpy()

    return {
        "abs_error": abs_error,
        "rel_error": rel_error,
        "abs_error_mean": float(abs_vals.mean()),
        "abs_error_max": float(abs_vals.max()),
        "rel_error_mean": float(np.nanmean(rel_vals)),
        "rel_error_max": float(np.nanmax(rel_vals)),
    }


def compute_congestion(flow: Any, limit: Any, tol: float = 1e-6) -> dict:
    """Compute line loading and congestion flags."""
    flow_arr = np.asarray(flow, dtype=float)
    limit_arr = np.asarray(limit, dtype=float)
    denom = np.where(limit_arr == 0, np.nan, limit_arr)
    loading = np.abs(flow_arr) / denom
    congested = loading >= (1.0 - tol)

    return {
        "flow": flow_arr,
        "limit": limit_arr,
        "loading": loading,
        "congested": congested,
        "loading_mean": float(np.nanmean(loading)),
        "loading_max": float(np.nanmax(loading)),
    }


def compute_congestion_match(
    dc_flow: Any, ac_flow: Any, limit: Any, tol: float = 1e-6
) -> dict:
    """Compute how often DC and AC congestion flags agree."""
    dc = compute_congestion(dc_flow, limit, tol)
    ac = compute_congestion(ac_flow, limit, tol)
    dc_loading = np.asarray(dc["loading"], dtype=float)
    ac_loading = np.asarray(ac["loading"], dtype=float)
    valid = ~np.isnan(dc_loading) & ~np.isnan(ac_loading)
    match = np.asarray(dc["congested"], dtype=bool) == np.asarray(ac["congested"], dtype=bool)
    total = int(valid.sum())
    match_count = int(match[valid].sum()) if total else 0
    match_rate = float(match_count / total) if total else float("nan")

    return {
        "congestion_match_rate": match_rate,
        "congestion_match_count": match_count,
        "congestion_match_total": total,
    }


def _coerce_scalar(value: Any) -> Any:
    if isinstance(value, (np.integer, np.floating)):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def make_row(case: dict, metrics: dict) -> dict:
    """Build a flat row from case metadata and scalar metrics."""
    row = {"case": case.get("name"), "alpha": case.get("alpha")}
    scalar_types = (int, float, bool, np.integer, np.floating, np.bool_)

    for key, value in metrics.items():
        if isinstance(value, scalar_types):
            row[key] = _coerce_scalar(value)
        elif isinstance(value, dict):
            for sub_key, sub_val in value.items():
                if isinstance(sub_val, scalar_types):
                    row[f"{key}_{sub_key}"] = _coerce_scalar(sub_val)

    return row


def write_csv(rows: list[dict], path: str | Path) -> pd.DataFrame:
    """Write rows to CSV and return the DataFrame."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return df
