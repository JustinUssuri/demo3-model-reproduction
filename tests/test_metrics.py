
import numpy as np
import pandas as pd
import pytest

from src.metrics import compute_dc_ac_errors


def test_compute_dc_ac_errors_basic() -> None:
    dc = pd.DataFrame([[1.0, 2.0], [3.0, 4.0]], columns=["L1", "L2"])
    ac = pd.DataFrame([[1.5, 1.5], [2.5, 4.5]], columns=["L1", "L2"])

    result = compute_dc_ac_errors(dc, ac)

    assert result["abs_error_mean"] == pytest.approx(0.5)
    assert result["abs_error_max"] == pytest.approx(0.5)
    assert result["rel_error_mean"] == pytest.approx(0.24444444444444446)
    assert result["rel_error_max"] == pytest.approx(1.0 / 3.0)


def test_rel_error_nan_when_ac_zero() -> None:
    dc = pd.DataFrame([[0.0, 2.0]], columns=["L1", "L2"])
    ac = pd.DataFrame([[0.0, 1.0]], columns=["L1", "L2"])

    result = compute_dc_ac_errors(dc, ac)

    assert np.isnan(result["rel_error"].iloc[0, 0])
    assert result["rel_error_mean"] == pytest.approx(1.0)
