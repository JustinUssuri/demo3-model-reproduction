# Demo3 PRD — Paradigm-Aware Power System Modeling (PyPSA-GB Case Study)

## 0. One-line summary
Build a minimal, reproducible experiment that makes *modeling assumptions* first-class
and demonstrates *where/when DC power flow (as used in PyPSA-GB) becomes misleading*.

This is not a full PyPSA-GB reproduction. It is a paradigm-aware modeling study.

---

## 1. Motivation & Problem Statement

### Motivation
Many power-system models rely on engineering approximations (e.g., DC power flow) to scale.
As compute + renewables + inverter penetration grow, some legacy approximations may become
less reliable in specific regimes.

### Problem statement
We want a transparent, minimal experiment that answers:

1) What assumptions does DC power flow rely on?
2) In which regimes do those assumptions break down?
3) What kind of *decision-relevant errors* can arise (e.g., wrong congestion ranking)?

---

## 2. Goals (v0.1)

### G1: Assumptions are explicit
Create a clear `assumptions.md` describing the DC approximation assumptions and validity regimes.

### G2: Minimal reproducible experiment
Provide a small toy network with a parameterized sweep that compares:

- DC power flow results
- A more physically complete reference for comparison (AC load flow)

Output: plots + tables + short write-up showing *where DC deviates materially*.

### G3: Research-style artifact
Produce a repo that a PI can skim in 3 minutes and understand:
- research question
- methodology
- results
- limitations

---

## 3. Non-goals (explicitly excluded in v0.1)
- Reproducing the full Great Britain network / dataset
- Full dispatch optimization / OPF / investment planning
- Market modeling, unit commitment
- Stability, dynamics, protection, frequency response
- Building a “product”

---

## 4. Key Deliverables

### D1: Repo documentation
- `README.md`: 2-min overview + how to run + what results mean
- `paper_to_model.md`: already exists; keep as “translation layer”
- `assumptions.md`: DC assumptions + validity + failure modes
- `results/summary.md`: short result interpretation (research style)

### D2: Reproducible experiment code
- `src/cases.py`: defines toy networks and parameter sweep cases
- `src/dc_flow.py`: DC power flow solver (minimal, transparent)
- `src/ac_flow.py`: AC load flow wrapper (reference method)
- `src/metrics.py`: error metrics + “decision-relevant” indicators
- `src/plotting.py`: generate plots
- `run_experiments.py`: CLI entry to run baseline + sweep and write results

### D3: Outputs
- `results/tables/*.csv`
- `results/figures/*.png`
- `results/summary.md` with key findings and caveats

---

## 5. Reference Model Choice (AC “ground truth”)

### Option A (preferred): AC load flow via pandapower
- Use pandapower to run AC power flow on the toy network
- Compare line active power flows and feasibility
Reason: widely used, accessible, good for small networks.

### Option B: AC via PyPSA (if easier in environment)
- Use PyPSA's AC capability if straightforward
- Keep the API usage minimal

Decision: start with Option A unless dependency pain is unacceptable.

---

## 6. Experimental Design (v0.1)

### 6.1 Toy network
Base case: 3–5 buses, 3–6 lines, 1–2 generators, 1–2 loads.
Keep it small enough to inspect by eye.

### 6.2 “Failure mode” sweeps
Run parameter sweeps that target DC assumption violations:

- Sweep S1: large angle differences (increase transfer / tighten lines)
- Sweep S2: high R/X ratio (DC ignores resistance/losses; AC responds differently)
- Sweep S3: voltage constraints relevance (AC feasible but voltage-stressed; DC unaware)
- Sweep S4 (optional): reactive power effects (AC redispatch/flow impacts, DC ignores)

At minimum implement S1 + S2 in v0.1.

### 6.3 Metrics
Compute for each case:
- Line flow absolute error: |P_dc - P_ac|
- Relative error: |P_dc - P_ac| / max(|P_ac|, eps)
- Congestion ranking mismatch:
  - Identify top-k most loaded lines under DC vs AC
  - Measure overlap / rank correlation
- Feasibility mismatch:
  - AC converges? DC feasible? (flag divergences)

---

## 7. User Stories (what “done” looks like)

### US1: PI skim test (3 minutes)
As a PI, I can open README and:
- understand the research question
- see the key result plots
- see why DC was chosen in PyPSA-GB, and where it may mislead

### US2: Repro run (one command)
As a reader, I can run a single command to reproduce results.

### US3: Transparent code (inspectability)
As a reviewer, I can inspect toy case definitions and solvers without digging into complex frameworks.

---

## 8. CLI / Usage Requirements

### Required commands
- `python run_experiments.py baseline`
  - runs base case comparison (DC vs AC)
  - writes one CSV + one plot

- `python run_experiments.py sweep --suite S1`
  - runs a sweep suite and writes results to `results/`

Optional:
- `python run_experiments.py all`
  - runs baseline + all sweeps

---

## 9. Repo Structure (proposed)

- README.md
- paper_to_model.md
- assumptions.md
- results/
  - figures/
  - tables/
  - summary.md
- src/
  - cases.py
  - dc_flow.py
  - ac_flow.py
  - metrics.py
  - plotting.py
- run_experiments.py
- tests/
  - test_dc_flow.py
  - test_metrics.py
- environment.yml (or pyproject.toml)

---

## 10. Quality & Acceptance Criteria (v0.1)

### A1: Reproducibility
- Fresh environment setup succeeds
- Running baseline produces deterministic outputs

### A2: Correctness sanity checks
- DC solver passes simple conservation checks (KCL)
- AC solver converges for baseline case

### A3: Research signal
- At least one sweep produces a clear regime where DC deviates materially
  AND the deviation is interpreted in `results/summary.md`.

---

## 11. Milestones (small, safe steps)

### M0: Scaffold (0.5–1 day)
- Create file structure, placeholder modules, minimal CLI, environment file

### M1: Baseline DC vs AC (1–2 days)
- Implement toy network
- DC flow + AC flow
- One plot + one table + short notes

### M2: Sweep S1 (1–2 days)
- Parameter sweep implementation
- Metrics + plots

### M3: Sweep S2 (1–2 days)
- High R/X or resistance sweep
- Decision-relevant mismatch plot

### M4: Write-up polish (0.5–1 day)
- assumptions.md finalized
- results/summary.md tightened
- README “PI skim test” pass

---

## 12. Risks & Mitigations

- Risk: AC solver dependency friction
  - Mitigation: fall back to PyPSA AC or keep reference to a simplified AC proxy
- Risk: scope creep (“let’s add OPF/time series/full GB”)
  - Mitigation: non-goals section + milestone gatekeeping
- Risk: unclear “why it matters”
  - Mitigation: emphasize congestion ranking mismatch and feasibility mismatch

---

## 13. Definition of Done (v0.1)
Repo contains:
- assumptions.md + results/summary.md
- runnable baseline + at least one sweep suite
- reproducible figures/tables
- README communicates question → method → results → limitations
