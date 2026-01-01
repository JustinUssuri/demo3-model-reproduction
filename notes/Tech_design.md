# Toy Network Design (GB-inspired) -- DC vs AC with PyPSA
Version: v0.1

## 0. Objective (aligned with PRD)
Quantify how closely DC power flow agrees with AC power flow across a controlled
system stress sweep in a minimal, GB-inspired transmission-style network.

This toy system is not a GB reproduction.
It is a GB-inspired cartoon used to isolate and quantify the validity regime of DC power flow
for decision-relevant conclusions (e.g., congestion identification).

---

## 1. Core container and solvers
- Primary container: PyPSA `Network` (buses/lines or buses/links, generators, loads, storage, snapshots).
- DC model: PyPSA LOPF (linear, network-constrained) is the main DC solve path.
- AC reference: PyPSA AC power flow (`Network.pf`) on the same network topology.
- Solver default: HiGHS (open-source). Allow optional switch to gurobi without hard dependency.
- Constraint: do not hand-write a DC solver as the main implementation (legacy reference only).

---

## 2. GB-inspired mapping (why this topology)
We model a simplified "North-Interface-South" structure:

- North (N): wind-rich generation region (exporting power southward)
- Mid (M): transmission interface / bottleneck region (represents a key corridor)
- South (S): load center + dispatchable generation (importing from North)

This mirrors a common stylized GB narrative: renewable generation concentrated in one area,
demand concentrated elsewhere, connected by limited transmission corridors.

---

## 3. Network topology (3-bus baseline)
### Buses
- Bus N: generator bus (wind)
- Bus M: interface bus (no generation in baseline, small load optional)
- Bus S: load bus + dispatchable generator

### Lines
- Line L1: N - M (corridor segment 1)
- Line L2: M - S (corridor segment 2)
Optional (off by default in v0.1):
- Line L3: N - S (weak tie-line)

Rationale: A 3-bus chain is the smallest topology that still produces a meaningful corridor flow.

---

## 4. Electrical parameterization (transmission-style baseline)
We choose transmission-like parameters to make DC expected to perform well at low stress.

Example (conceptual):
- L1: r = 0.01, x = 0.10, thermal limit = 100 MW
- L2: r = 0.01, x = 0.10, thermal limit = 100 MW
- (Optional) L3: r = 0.02, x = 0.20, thermal limit = 30 MW

Note: Exact numbers may change depending on solver conventions.

---

## 5. Generation and load setup
### Loads
- Base load at S: P_load_S = 80 MW (baseline)
- Optional small load at M: P_load_M = 0-10 MW (default 0)

### Generators
- Wind generator at N:
  - P_wind_N = variable (controlled by sweep)
  - Low marginal cost (e.g., 0-5)
  - `p_max_pu` scaled by alpha
- Dispatchable generator at S:
  - Acts as balancing generator
  - Higher marginal cost (e.g., 30-60)
  - Broad P limits (e.g., 0-200 MW)

---

## 6. Stress sweep definition (single dimension)
We run exactly one sweep dimension in v0.1 to keep interpretation clean.

### Sweep choice (recommended): Wind availability scaling
Let alpha in [0.2, 1.5] be a scaling factor.

- P_wind_N(alpha) = alpha * P_wind_base
- Load stays fixed at S (baseline load)

### Sweep implementation (PyPSA snapshots)
- Use snapshots indexed by alpha values.
- Apply `p_max_pu` time series to the wind generator.
- Apply `p_set` time series to loads (if needed).

---

## 7. Experiments to compare
### DC vs AC (primary PRD objective)
- Run DC LOPF on the network-constrained case.
- Run AC power flow on the same network and injections.
- Compare line flows, congestion indicators, and feasibility.

---

## 8. Metrics (decision-relevant)
For each alpha:

DC vs AC:
1) Line flow deviation
   - abs_err(L) = |P_dc(L) - P_ac(L)|
   - rel_err(L) = abs_err(L) / max(|P_ac(L)|, eps)
2) Congestion indicator consistency
   - loading_dc(L) = |P_dc(L)| / limit(L)
   - loading_ac(L) = |P_ac(L)| / limit(L)
   - Compare top-1 most loaded line across DC/AC
3) Feasibility / convergence
   - AC converged? (True/False)

## 9. Outputs and plots (minimum set)
- `results/tables/sweep.csv` with per-alpha metrics for DC vs AC.
- `results/figures/*.png`:
  - DC vs AC flow error vs alpha
  - congestion consistency vs alpha
  - loading vs alpha (per line)
- `results/summary.md` with short findings + caveats.

---

## 10. Solver configuration
- Default solver: HiGHS (open-source).
- Optional override: gurobi (configurable, not required).
- Expose solver choice via CLI or config.

---

## 11. Implementation notes (to help coding)
- Keep case definition deterministic (no randomness).
- Use PyPSA `Network` and LOPF as the main DC solve path.
- Use PyPSA AC power flow for the reference path.
- Use tidy outputs for tables/plots to keep downstream steps simple.
