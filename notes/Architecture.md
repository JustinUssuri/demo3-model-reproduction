# Demo3 v0.1 — Development Architecture (Aligned with Tech Design)

This document summarizes the **runtime dataflow**, **module dependencies**, and **module boundaries** for Demo3 v0.1, aligned to the toy GB-inspired DC vs AC agreement study.

---

## 1) Runtime Dataflow

```mermaid
flowchart TD
  A[User / CLI<br/>run_experiments.py] --> B[Experiment Orchestrator<br/>parse args, select sweep]
  B --> C[Case Factory<br/>src/cases.py<br/>3-bus toy network + alpha grid]
  C --> D1[DC Solver<br/>src/dc_flow.py<br/>lossless DC flow]
  C --> D2["AC Reference\nsrc/ac_flow.py\npandapower AC flow"]
  D1 --> E[Metrics Engine<br/>src/metrics.py<br/>flow errors + congestion consistency + convergence]
  D2 --> E
  E --> F1[Results Table<br/>results/tables/sweep.csv]
  E --> F2[Plotting<br/>src/plotting.py<br/>results/figures/*.png]
  F1 --> G[Write-up Stub<br/>results/summary.md]
  F2 --> G
```

---

## 2) Module Dependency View

```mermaid
flowchart LR
  subgraph Entry
    CLI[run_experiments.py]
  end

  subgraph Core
    CASES[src/cases.py]
    DC[src/dc_flow.py]
    AC[src/ac_flow.py]
    MET[src/metrics.py]
    PLOT[src/plotting.py]
  end

  subgraph Artifacts
    TBL[results/tables/sweep.csv]
    FIG[results/figures/*.png]
    SUM[results/summary.md]
  end

  CLI --> CASES
  CLI --> DC
  CLI --> AC
  CLI --> MET
  CLI --> PLOT

  CASES --> DC
  CASES --> AC
  DC --> MET
  AC --> MET
  MET --> TBL
  MET --> PLOT
  PLOT --> FIG
  TBL --> SUM
  FIG --> SUM
```

---

## 3) Module Boundaries (v0.1)

- **`src/cases.py`**
  - Defines the 3-bus toy network and alpha sweep grid.
  - Outputs: buses/branches, injections (P), and case labels/parameters.

- **`src/dc_flow.py`**
  - Computes lossless DC flows for each case.
  - Outputs: per-branch active power flows, optional angles, feasibility flags.

- **`src/ac_flow.py`**
  - AC reference solver using pandapower.
  - Outputs: per-branch active power flows, optional voltage magnitudes/angles, convergence flag.

- **`src/metrics.py`**
  - Computes flow errors and congestion indicator consistency across the sweep.
  - Outputs: structured metrics and row-wise records for `results/tables/sweep.csv`.

- **`src/plotting.py`**
  - Generates plots from the tidy metrics table (e.g., error vs alpha, loading vs alpha).

- **Artifacts**
  - `results/tables/sweep.csv` — per-alpha metrics table
  - `results/figures/abs_error_vs_alpha.png`
  - `results/figures/loading_vs_alpha.png`
  - `results/summary.md` — short write-up stub with headline findings and caveats
