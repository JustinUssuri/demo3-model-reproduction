# Toy Network Design (GB-inspired) — DC vs AC Agreement Validation
Version: v0.1

## 0. Objective (aligned with PRD)
Quantify how closely **DC power flow** agrees with **AC power flow** across a controlled
**system stress sweep** in a minimal, GB-inspired transmission-style network.

This toy system is **not** a GB reproduction.
It is a **GB-inspired cartoon** used to isolate and quantify the validity regime of DC power flow
for decision-relevant conclusions (e.g., congestion identification).

---

## 1. GB-inspired mapping (why this topology)
We model a simplified “North–Interface–South” structure:

- **North (N)**: wind-rich generation region (exporting power southward)
- **Mid (M)**: transmission interface / bottleneck region (represents a key corridor)
- **South (S)**: load center + dispatchable generation (importing from North)

This mirrors a common stylized GB narrative: renewable generation concentrated in one area,
demand concentrated elsewhere, connected by limited transmission corridors.

---

## 2. Network topology (3-bus baseline)
### Buses
- Bus N: generator bus (wind)
- Bus M: interface bus (no generation in baseline, small load optional)
- Bus S: load bus + dispatchable generator (slack-like role for AC convergence)

### Lines
- Line L1: N — M (corridor segment 1)
- Line L2: M — S (corridor segment 2)
Optional (off by default in v0.1):
- Line L3: N — S (weak tie-line)

Rationale: A 3-bus chain is the smallest topology that still produces a meaningful corridor flow.

---

## 3. Electrical parameterization (transmission-style baseline)
We choose transmission-like parameters to make DC expected to perform well at low stress.

### Baseline line parameters (suggested)
- Use per-unit on a common base (e.g., 100 MVA) or consistent MW units if using pandapower defaults.
- Set **R small relative to X** (high X/R) in baseline.

Example (conceptual):
- L1: r = 0.01, x = 0.10, thermal limit = 100 MW
- L2: r = 0.01, x = 0.10, thermal limit = 100 MW
- (Optional) L3: r = 0.02, x = 0.20, thermal limit = 30 MW

Note: Exact numbers may change depending on solver conventions.
The key is: baseline is transmission-like (high X/R), then we apply stress via transfer/load.

---

## 4. Generation and load setup
### Loads
- Base load at S: P_load_S = 80 MW (baseline)
- Optional small load at M: P_load_M = 0–10 MW (default 0)

### Generators
- Wind generator at N:
  - P_wind_N = variable (controlled by sweep)
  - Cost irrelevant (no OPF in v0.1)
- Dispatchable generator at S (for AC reference feasibility):
  - Acts as balancing generator so that AC has a feasible solution across sweep
  - Set broad P limits (e.g., 0–200 MW)

Model intent:
- Under low stress, power largely flows N → S through the corridor (L1+L2).
- Under high stress, corridor loading increases toward thermal limits.

---

## 5. Stress sweep definition (single dimension)
We run exactly **one** sweep dimension in v0.1 to keep interpretation clean.

### Sweep choice (recommended): Wind injection scaling
Let alpha ∈ [0.2, 1.5] be a scaling factor.

- P_wind_N(alpha) = alpha * P_wind_base
- Keep load fixed at S (baseline load)

Balancing:
- Dispatchable generator at S adjusts to satisfy power balance
  (in DC: exact balance; in AC: includes losses as solved)

Alternative (if easier): load scaling at S with fixed wind base.
But wind-scaling aligns nicely with the “north export” story.

### Sweep range & resolution
- alpha from 0.2 to 1.5
- step size: 0.05 (or 0.1 if runtime is a concern)
- total cases: ~27 (0.05 step) or ~14 (0.1 step)

---

## 6. Models to compare (v0.1)
### DC model
- Lossless DC power flow (as documented in assumptions.md)
- Outputs:
  - line active power flows P_dc(L1), P_dc(L2)
  - implied bus angles (optional)

### AC reference model
- Full AC power flow (pandapower preferred)
- Outputs:
  - line active power flows P_ac(L1), P_ac(L2)
  - convergence flag
  - (optional) voltage magnitudes to confirm near-1.0 p.u. under baseline

---

## 7. Metrics (decision-relevant)
For each alpha:
1) **Line flow deviation**
   - abs_err(L) = |P_dc(L) - P_ac(L)|
   - rel_err(L) = abs_err(L) / max(|P_ac(L)|, eps)

2) **Congestion indicator consistency**
   - loading_dc(L) = |P_dc(L)| / limit(L)
   - loading_ac(L) = |P_ac(L)| / limit(L)
   - Compare:
     - which line is more loaded (argmax over L1,L2)
     - top-1 match rate across sweep
     - (optional) rank correlation if >2 lines

3) **Feasibility / convergence**
   - AC converged? (True/False)
   - If AC fails to converge at high alpha, record that as “beyond reliable operating regime”
     (do not treat as a bug; document as limitation)

Primary story:
- Under low-to-moderate stress, DC–AC agreement should be tight.
- As stress increases, deviations may grow; quantify where they remain acceptable.

---

## 8. Plots to generate (minimum set)
- Plot A: abs_err vs alpha (one curve per line)
- Plot B: loading_dc and loading_ac vs alpha (per line)
- Plot C: indicator of “most loaded line” under DC vs AC vs alpha (simple categorical or marker)

Outputs:
- results/tables/sweep.csv
- results/figures/abs_error_vs_alpha.png
- results/figures/loading_vs_alpha.png

---

## 9. Acceptance criteria (v0.1)
- Baseline (alpha near 1.0) runs successfully for both DC and AC and produces comparable flows.
- Sweep runs end-to-end, producing CSV + at least two plots.
- results/summary.md can state, based on evidence:
  - “In this transmission-style cartoon, DC tracks AC closely up to [range], and divergence grows near [range].”
  - plus caveats (no Q/voltage constraints, toy topology, etc.)

---

## 10. Implementation notes (to help coding)
- Keep case definition deterministic (no randomness).
- Separate concerns:
  - cases.py defines alpha grid + base case params
  - dc_flow.py computes DC flows
  - ac_flow.py runs AC solver and returns flows + converged flag
  - metrics.py computes errors + congestion consistency
  - plotting.py makes plots from a single tidy dataframe

No optimization, no OPF in v0.1.
