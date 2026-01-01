# Demo3 v0.1 -- Development Architecture (PyPSA DC LOPF vs AC PF)

This document summarizes the runtime dataflow, module dependencies, and module boundaries for
Demo3 v0.1, aligned to the PRD objective: DC vs AC agreement across a controlled stress sweep.

---

## 1) Runtime Dataflow

```mermaid
flowchart TD
  A[User or CLI: run_experiments.py] --> B[Experiment Orchestrator: parse args, select sweep]
  B --> C[Case Factory: src/cases.py, toy network spec + alpha grid]

  C --> D[PyPSA Network Builder: src/pypsa_model.py, network-constrained]
  D --> E1[DC LOPF: src/opf.py, PyPSA + HiGHS]
  D --> E2[AC PF: src/ac_flow.py, PyPSA pf]

  E1 --> F[Metrics Engine: src/metrics.py, DC-AC errors + congestion consistency]
  E2 --> F

  F --> G1[Results Tables: results/tables/*.csv]
  F --> G2[Plotting: src/plotting.py, results/figures/*.png]
  G1 --> H[Write-up Stub: results/summary.md]
  G2 --> H
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
    MODEL[src/pypsa_model.py]
    OPF[src/opf.py]
    AC[src/ac_flow.py]
    MET[src/metrics.py]
    PLOT[src/plotting.py]
  end

  subgraph Artifacts
    TBL[results/tables/*.csv]
    FIG[results/figures/*.png]
    SUM[results/summary.md]
  end

  CLI --> CASES
  CLI --> MODEL
  CLI --> OPF
  CLI --> AC
  CLI --> MET
  CLI --> PLOT

  CASES --> MODEL
  MODEL --> OPF
  MODEL --> AC
  OPF --> MET
  AC --> MET
  MET --> TBL
  MET --> PLOT
  PLOT --> FIG
  TBL --> SUM
  FIG --> SUM
```

---

## 3) Module Boundaries (v0.1)

- `src/cases.py`
  - Defines the toy network spec and alpha sweep grid.
  - Outputs: structured inputs for buses/lines/gens/loads and scenario parameters.

- `src/pypsa_model.py`
  - Builds a PyPSA `Network` with buses/lines/generators/loads and snapshots.
  - Encodes the network-constrained topology used for DC vs AC comparison.

- `src/opf.py`
  - Runs PyPSA LOPF using HiGHS by default (configurable to gurobi).
  - Outputs: solved network with dispatch, flows, and shadow prices.

- `src/ac_flow.py`
  - Runs PyPSA AC power flow (`Network.pf`) on the network-constrained case.
  - Outputs: line flows, voltage angles/magnitudes, convergence flag.

- `src/metrics.py`
  - Computes DC-AC flow errors and congestion consistency.
  - Outputs: tidy metrics rows and `results/tables/*.csv`.

- `src/plotting.py`
  - Generates plots from the metrics table (DC-AC error, congestion).

- Artifacts
  - `results/tables/*.csv` -- per-alpha metrics table(s)
  - `results/figures/*.png` -- comparison plots
  - `results/summary.md` -- short write-up with headline findings and caveats

- Optional legacy baseline
  - `src/dc_flow.py` may remain as a non-primary reference, but must not be the main solver.
