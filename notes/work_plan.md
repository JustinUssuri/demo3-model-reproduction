# Demo3 v0.1 Development Plan

Goal: Based on a 3-bus toy network, run a single alpha sweep and complete the minimal closed loop
for DC vs AC agreement (PyPSA LOPF vs PyPSA AC PF).

Scope and constraints:
- Use PyPSA `Network` as the core modeling container.
- DC/linear power flow must be solved via PyPSA LOPF (no hand-written DC solver as main path).
- AC reference uses PyPSA `Network.pf` on the same topology.
- Default solver is HiGHS; allow config switch to gurobi without hard dependency.
- Keep outputs in `results/tables/*.csv`, `results/figures/*.png`, `results/summary.md`.

---

## Milestones and deliverables

M1. Project skeleton and data structures
- Define base modules under `src/` and result directory structure.
- Define case data structure (buses/lines/gens/loads/limits/alpha).
- Deliverable: loadable base case + alpha grid.

M2. PyPSA network builder
- Implement `src/pypsa_model.py` to build a `Network` with buses/lines/gens/loads and snapshots.
- Deliverable: a single alpha snapshot can be built with the constrained network topology.

M3. DC LOPF and AC PF solve loop
- Implement `src/opf.py` to run LOPF with solver selection (HiGHS default).
- Implement `src/ac_flow.py` to run PyPSA AC power flow on the constrained network.
- Deliverable: a single alpha snapshot can run DC LOPF and AC PF successfully.

M4. Metrics and results table
- Implement `src/metrics.py`:
  - DC-AC flow errors and congestion consistency
  - AC convergence flag
- Output `results/tables/sweep.csv` (one row per alpha).
- Deliverable: full sweep table.

M5. Plots and summary
- Implement `src/plotting.py`:
  - DC vs AC error plot
  - congestion consistency plot
  - loading vs alpha (per line)
- Generate `results/figures/*.png` and `results/summary.md`.
- Deliverable: key plots + short conclusion.

M6. Run entrypoint and docs
- `run_experiments.py` wires the full pipeline.
- Update README with run instructions and solver notes.
- Deliverable: one command can reproduce the experiment.

---

## Micro task list (ADHD friendly)

Principle: each task should take 5-20 minutes. Check it off when done. Only do one small module step at a time.

### 0) Prep and skeleton
- [x] Create `src/` and `results/` directories (skip if already exist).
- [x] Create empty files: `src/cases.py`, `src/metrics.py`, `src/plotting.py`, `run_experiments.py`.
- [x] Create `src/pypsa_model.py`, `src/opf.py`, `src/ac_flow.py`.
- [x] Create `tables/` and `figures/` under `results/`.
- [x] Write a minimal `main()` in `run_experiments.py` that prints "ok".
- [x] Run the entry script once to confirm it executes.

### 1) `src/cases.py` (start with data shape)
- [x] Write a `make_base_case()` function that returns a base dict.
- [x] Put a buses list into the dict (N/M/S).
- [x] Put a lines list into the dict (L1/L2, with r/x/limit).
- [x] Add an optional L3 toggle field (default off).
- [x] Write `make_cases()` to combine the base case + alpha into a case list.
- [x] Add a short `__main__` self-check at the bottom (print case count).
- [x] Manually run the self-check once, confirm no exceptions.

### 2) `src/pypsa_model.py`
- [x] Write `build_network(case, snapshots)` that returns a PyPSA `Network`.
- [x] Add buses, lines (or links), generators, and loads.
- [x] Encode the alpha sweep as snapshots with time series for load and wind availability.
- [ ] Try building a single alpha snapshot and print basic network stats.

### 3) `src/opf.py`
- [x] Write `solve_lopf(network, solver_name)` with HiGHS default.
- [ ] Expose a CLI/config option to switch to gurobi if available.
- [x] Return solved network and status flag.
- [ ] Run once on the baseline case and record success.

### 4) `src/ac_flow.py`
- [x] Write `solve_ac_pf(network)` and run PyPSA AC power flow.
- [x] Return a structured result dict: `line_flows`, `vm`, `va`, `converged`.
- [ ] Try one run on the baseline case and record convergence.

### 5) `src/metrics.py`
- [ ] Write `compute_dc_ac_errors(dc, ac)` for abs/rel error.
- [ ] Write `compute_congestion(flow, limit)` to compute loading and match flags.
- [ ] Write `make_row(case, metrics)` to build one row dict (include alpha).
- [ ] Write `write_csv(rows, path)` to save the sweep table.
- [ ] Validate on 2-3 cases and output a CSV once.

### 6) `src/plotting.py`
- [ ] Write `load_table(path)` to read `results/tables/sweep.csv`.
- [ ] Write `plot_dc_ac_error(df, out_path)` for DC vs AC error.
- [ ] Write `plot_congestion_match(df, out_path)` for congestion consistency.
- [ ] Write `plot_loading(df, out_path)` for loading vs alpha.
- [ ] Run once on a small table and confirm files are generated.

### 7) `run_experiments.py` (end-to-end wiring)
- [ ] Parse CLI args (alpha range/step, solver).
- [ ] Call `make_cases()` to generate the sweep.
- [ ] For each case, build a network, run DC LOPF, run AC PF.
- [ ] Compute DC-AC metrics.
- [ ] Write `results/tables/sweep.csv`.
- [ ] Generate plots into `results/figures/`.
- [ ] Generate `results/summary.md` (start with a fixed template).
- [ ] Run end-to-end once, confirm no exceptions.

### 8) Docs sync
- [ ] Update README: how to run the sweep and solver selection.
- [ ] Update assumptions: clarify DC assumptions and toy network limits.

---

## Even smaller "next step" suggestions (if stuck)
- [ ] Only finish `src/pypsa_model.py` with a single alpha snapshot.
- [ ] Only make `run_experiments.py` print the alpha list.
- [ ] Only make `src/opf.py` return solver status on one case.

---

## Acceptance criteria (v0.1)

- DC LOPF and AC PF both converge on the baseline (alpha ~= 1.0).
- Sweep runs end-to-end, generates CSV + at least two plots.
- `results/summary.md` describes DC vs AC agreement and limitations.

---

## Pending confirmation

- Alpha step size (0.05 or 0.1).
- Final line parameters and base MVA.
