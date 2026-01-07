# Model Reproduction

## Project overview
This repository runs a small PyPSA-based experiment comparing DC linear optimal power flow (LOPF) decisions to AC power-flow checks on a toy 3-bus network. A parameter sweep scales wind availability (`alpha`) and records DC vs AC line-flow errors and congestion agreement. The workflow is meant for quick reproducibility rather than generality; see `summary.md` for observations and limitations.

## Quickstart
Create the environment (conda is the preferred method in this repo):
```bash
conda env create -f environment.yml
conda activate model-reproduction
```

Run the end-to-end experiment (writes the CSV table and figures):
```bash
python run_experiments.py
```

Regenerate plots from an existing table:
```bash
python - <<'PY'
from pathlib import Path

from src.plotting import load_table, plot_congestion_match, plot_dc_ac_error, plot_loading

df = load_table("results/tables/sweep.csv")
out_dir = Path("results/figures")
plot_dc_ac_error(df, out_dir / "dc_ac_error.png")
plot_congestion_match(df, out_dir / "congestion_match.png")
plot_loading(df, out_dir / "loading.png")
PY
```

Expected outputs:
- `results/tables/sweep.csv`
- `results/figures/dc_ac_error.png`
- `results/figures/congestion_match.png`
- `results/figures/loading.png`

## Repository structure
- `run_experiments.py`: end-to-end sweep runner (LOPF → AC PF → metrics → plots).
- `src/cases.py`: case generator and alpha sweep definition.
- `src/pypsa_model.py`: builds a PyPSA `Network` from a case dict.
- `src/opf.py`: DC LOPF solve wrapper (selects solver via `LOPF_SOLVER`).
- `src/ac_flow.py`: AC power-flow wrapper and convergence handling.
- `src/metrics.py`: error/congestion metrics and CSV writing.
- `src/plotting.py`: plotting utilities for the sweep outputs.
- `environment.yml`: pinned dependencies for a reproducible environment.

## Reproducibility notes
- Dependency pins live in `environment.yml` (notably `python=3.10`, `numpy<2.0`, `xarray<2025`, `highs<1.7`).
- The LOPF solver defaults to `highs`; override with `LOPF_SOLVER` if you want another PyPSA-supported solver.
- `run_experiments.py` uses `alpha_min=0.8`, `alpha_max=1.0`, `alpha_step=0.1`; changing these changes the sweep output.

## Results
- `results/tables/sweep.csv`
- `results/figures/dc_ac_error.png`
- `results/figures/congestion_match.png`
- `results/figures/loading.png`
- `summary.md` (observations and limitations write-up)

## Troubleshooting
- Solver errors in LOPF: ensure the conda environment is active, and try `export LOPF_SOLVER=highs` or `export LOPF_SOLVER=glpk`.
- AC PF does not converge: check the `ac_converged` column in `results/tables/sweep.csv` and reduce the `alpha` sweep range in `run_experiments.py`.
- Plotting failures in headless environments: run `python run_experiments.py` (it sets `MPLBACKEND=Agg`) or set `MPLBACKEND=Agg` before custom plotting.
