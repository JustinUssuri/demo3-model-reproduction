#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

from src.ac_flow import solve_ac_pf
from src.cases import make_cases
from src.metrics import (
    compute_congestion,
    compute_congestion_match,
    compute_dc_ac_errors,
    make_row,
    write_csv,
)
from src.opf import solve_lopf
from src.plotting import plot_congestion_match, plot_dc_ac_error, plot_loading
from src.pypsa_model import build_network

TABLE_PATH = Path("results/tables/sweep.csv")
FIGURES_DIR = Path("results/figures")


def seed_pf_from_dc(network) -> None:
    dc_dispatch = getattr(network.generators_t, "p", None)
    if dc_dispatch is not None and not dc_dispatch.empty:
        network.generators_t.p_set = dc_dispatch.copy()


def run_case(case: dict) -> dict:
    network = build_network(case)
    solve_lopf(network)
    dc_flow = network.lines_t.p0.copy()
    line_limits = network.lines.s_nom.copy()

    seed_pf_from_dc(network)
    ac = solve_ac_pf(network)
    ac_flow = ac["line_p0"]

    metrics = {
        "dc_ac": compute_dc_ac_errors(dc_flow, ac_flow),
        "congestion": compute_congestion(dc_flow, line_limits),
        "ac_converged": ac["converged"],
    }
    metrics.update(compute_congestion_match(dc_flow, ac_flow, line_limits))
    return make_row(case, metrics)


def main() -> None:
    cases = make_cases(alpha_min=0.8, alpha_max=1.0, alpha_step=0.1)
    rows = [run_case(case) for case in cases]
    df = write_csv(rows, TABLE_PATH)
    plot_dc_ac_error(df, FIGURES_DIR / "dc_ac_error.png")
    plot_congestion_match(df, FIGURES_DIR / "congestion_match.png")
    plot_loading(df, FIGURES_DIR / "loading.png")


if __name__ == "__main__":
    main()
