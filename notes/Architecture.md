# Demo3 v0.1 — Development Architecture (Integrated)

This document consolidates the **runtime dataflow**, **module dependency view**, and **module boundary notes** for Demo3 v0.1.

---

## 1) Runtime Dataflow Architecture

```mermaid
flowchart TD
  A[User / CLI<br/>run_experiments.py] --> B[Experiment Orchestrator<br/>parse args, select suite, seed]
  B --> C[Case Factory<br/>src/cases.py<br/>toy networks + sweep generator]
  C --> D1[DC Solver<br/>src/dc_flow.py<br/>DC power flow]
  C --> D2["AC Reference\nsrc/ac_flow.py\npandapower (preferred)\nPyPSA AC fallback"]
  D1 --> E[Metrics Engine<br/>src/metrics.py<br/>errors + ranking mismatch + feasibility flags]
  D2 --> E
  E --> F1[Results Writer<br/>results/tables/*.csv]
  E --> F2[Plotting<br/>src/plotting.py<br/>results/figures/*.png]
  F1 --> G[Research Write-up Stub<br/>results/summary.md]
  F2 --> G
  B --> H[Docs Layer<br/>README.md / assumptions.md / paper_to_model.md]
  G --> H

  subgraph "Suites (v0.1)"
    S1[Sweep S1<br/>angle/transfer stress] --> C
    S2[Sweep S2<br/>high R/X stress] --> C
  end
```

---

## 2) Code Module Dependency Architecture

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
    TBL[results/tables/]
    FIG[results/figures/]
    SUM[results/summary.md]
  end

  subgraph Docs
    R[README.md]
    A[assumptions.md]
    P[paper_to_model.md]
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
  SUM --> R
  SUM --> A
  SUM --> P
```

---

## 3) Module Boundaries (v0.1)

- **`src/cases.py`**
  - Generates *networks + operating conditions* for baseline cases and sweeps.
  - Outputs: buses/branches metadata, injections (P), and any case labels/parameters.

- **`src/dc_flow.py`**
  - Given a case/network + injections, computes DC power flow results.
  - Outputs: per-branch active power flows, nodal angles (if applicable), feasibility flags.

- **`src/ac_flow.py`**
  - AC reference solver (prefer pandapower; fallback acceptable).
  - Outputs: per-branch active power flows (and optionally voltage magnitudes/angles), feasibility flags.

- **`src/metrics.py`**
  - Compares DC vs AC outputs and produces decision-relevant metrics:
    - flow error norms
    - congestion / ranking mismatches
    - feasibility mismatch flags
  - Outputs: a structured metrics object + row-wise records for CSV.

- **`src/plotting.py`**
  - Converts tables/metrics into figures (PNG) without touching solver logic.

- **Artifacts**
  - `results/tables/*.csv` — metrics tables per suite/case
  - `results/figures/*.png` — visualizations per suite/case
  - `results/summary.md` — short write-up stub: what was tested + headline findings

---

## Suggested Filename Convention

- This doc: `Demo3_v0.1_Dev_Architecture.md`
- Optional: keep diagrams in a dedicated `docs/` folder if you prefer.
