# Demo3 – Model Reproduction

This project reproduces and critiques an energy system model from the literature
using small, controlled PyPSA cases. The current focus is a simple 3-bus system
with a wind generator, a gas slack generator, and an optional line extension.

Current focus areas:
- modeling choices and assumptions
- AC vs DC decisions
- scope and limitations of the model

## Status
- AC power flow wrapper implemented
- Linear OPF wrapper implemented (requires a PyPSA-supported solver)
- Case generator and PyPSA network builder implemented
- DC flow, metrics, plotting, and experiment runner are stubs

## Repository layout
- `run_experiments.py`: placeholder entrypoint
- `src/cases.py`: base case plus alpha sweep case generator
- `src/pypsa_model.py`: build a PyPSA `Network` from a case dict
- `src/ac_flow.py`: AC power flow wrapper
- `src/opf.py`: linear OPF wrapper
- `src/dc_flow.py`, `src/metrics.py`, `src/plotting.py`: stubs
- `notes/`: design notes and planning docs

## Setup
Create the conda environment defined in `environment.yml`:
```bash
conda env create -f environment.yml
conda activate demo3-model-reproduction
```

## Quick start
Run a single case and inspect both AC PF and LOPF outputs:
```bash
python - <<'PY'
from src.cases import make_cases
from src.pypsa_model import build_network
from src.ac_flow import solve_ac_pf
from src.opf import solve_lopf

case = make_cases(alpha_min=0.5, alpha_max=0.5, alpha_step=0.1)[0]
network = build_network(case)

pf = solve_ac_pf(network)
print("pf_converged", pf["converged"])

opf = solve_lopf(network)
print("objective", opf["objective"])
PY
```

Notes:
- `alpha` scales the wind generator availability (`p_max_pu`).
- LOPF requires a solver supported by PyPSA (for example HiGHS via `highspy`).
