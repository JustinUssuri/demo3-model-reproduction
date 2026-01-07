from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_table(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def plot_dc_ac_error(df: pd.DataFrame, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    x = df["alpha"] if "alpha" in df.columns else df.index
    mean_col = "dc_ac_abs_error_mean" if "dc_ac_abs_error_mean" in df.columns else "abs_error_mean"
    max_col = "dc_ac_abs_error_max" if "dc_ac_abs_error_max" in df.columns else "abs_error_max"
    if mean_col not in df.columns:
        raise ValueError("Missing abs error mean column for DC vs AC plot")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, df[mean_col], marker="o", label="abs error mean")
    if max_col in df.columns:
        ax.plot(x, df[max_col], marker="s", label="abs error max")
    ax.set_xlabel("alpha")
    ax.set_ylabel("abs error")
    ax.set_title("DC vs AC flow error")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_congestion_match(df: pd.DataFrame, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    x = df["alpha"] if "alpha" in df.columns else df.index
    candidates = [
        "congestion_match_rate",
        "congestion_match_mean",
        "congestion_match",
        "congestion_consistency",
        "congestion_agreement",
    ]
    match_col = next((col for col in candidates if col in df.columns), None)
    if match_col is None:
        raise ValueError("Missing congestion match/consistency column for plot")

    series = df[match_col]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, series, marker="o", label=match_col)
    ax.set_xlabel("alpha")
    ax.set_ylabel("match rate")
    ax.set_title("Congestion consistency")
    if series.max() <= 1.2:
        ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_loading(df: pd.DataFrame, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    x = df["alpha"] if "alpha" in df.columns else df.index
    mean_col = "congestion_loading_mean"
    max_col = "congestion_loading_max"
    if mean_col not in df.columns:
        raise ValueError("Missing loading column for plot")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, df[mean_col], marker="o", label="loading mean")
    if max_col in df.columns:
        ax.plot(x, df[max_col], marker="s", label="loading max")
    ax.set_xlabel("alpha")
    ax.set_ylabel("loading")
    ax.set_title("Line loading vs alpha")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
