from __future__ import annotations

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
