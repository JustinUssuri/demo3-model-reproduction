# Modelling Assumptions and Their Validity Regimes

This project investigates **when and why common modelling assumptions in power system analysis—particularly DC power flow—become decision-relevant misleading**, rather than merely inaccurate in an absolute sense.

The goal is **not** to argue that DC models are “wrong”, but to make explicit:
- which assumptions are embedded,
- under which regimes they are reasonable,
- and under which regimes they may distort system-level decisions.

---

## 1. Linearised DC Power Flow Assumption

### Assumption
Power flows are modelled using the linearised DC approximation:
- voltage magnitudes are fixed at 1.0 p.u.
- line resistances are neglected (R ≈ 0)
- phase angle differences are assumed small
- reactive power and voltage constraints are ignored

Under these assumptions, active power flows are proportional to phase angle differences.

### Typical Justification
The DC approximation is widely used because it:
- simplifies the network physics to a linear form,
- scales well to large systems,
- preserves nodal power balance and Kirchhoff’s laws,
- is often sufficient for **planning-level** or **market-level** analysis.

For many high-voltage transmission networks under normal operating conditions, DC power flow provides a reasonable first-order approximation.

### Validity Regime
The approximation is generally reasonable when:
- line resistances are small relative to reactances (high X/R ratio),
- voltage magnitudes remain close to nominal,
- phase angle differences are small,
- the system operates away from thermal or stability limits.

### Potential Failure Modes
The DC approximation may become **decision-relevant misleading** when:
- transfer levels are high and angle differences are no longer small,
- resistive losses affect congestion patterns,
- voltage constraints or reactive power scarcity become binding,
- congestion ranking between corridors depends on AC effects.

Importantly, even when DC errors are moderate in absolute terms, **the relative ordering of constraints or decisions may change**, which is critical for planning and dispatch decisions.

---

## 2. Lossless Network Representation

### Assumption
Transmission losses are neglected or treated implicitly.

### Implications
- Total generation equals total demand exactly.
- Loss-induced redispatch is ignored.
- Long-distance transfers are effectively “free” in energy terms.

### Validity Regime
This assumption is often acceptable for:
- short-term operational comparisons,
- systems where losses are a small fraction of total flows,
- conceptual or pedagogical models.

### Potential Failure Modes
When transfers are large or geographically long-distance:
- losses can materially affect feasible dispatch,
- congestion signals may shift,
- system stress may be underestimated.

---

## 3. Static, Single-Snapshot Analysis

### Assumption
The model considers isolated snapshots rather than full time-coupled dynamics.

### Implications
- Ramping constraints are ignored.
- Inter-temporal coupling (storage, unit commitment) is excluded.
- Stability and transient dynamics are not represented.

### Validity Regime
This is acceptable when:
- the goal is structural insight rather than operational realism,
- snapshots are representative of broader regimes,
- conclusions are framed qualitatively rather than as schedules.

### Limitations
Results should **not** be interpreted as operational dispatch solutions.

---

## 4. Network Topology Simplification

### Assumption
The toy networks used in this project are intentionally small and stylised.

### Rationale
The purpose is not realism, but **mechanism isolation**:
- making causal relationships legible,
- avoiding confounding factors,
- enabling controlled parameter sweeps.

### Implication
Findings should be interpreted as **mechanism demonstrations**, not system forecasts.

---

## 5. Scope of Conclusions

This project does **not** claim:
- that DC power flow should be abandoned,
- that AC models are always superior,
- or that simplified models are inherently misleading.

Instead, it aims to show that:
> modelling assumptions can cross a threshold where they alter qualitative conclusions,  
> and that this threshold is often implicit rather than explicit.

Making these boundaries visible is essential for responsible system-level modelling.

---

## 6. Intended Use

The results of this project are intended for:
- methodological reflection,
- research and teaching,
- assumption-aware interpretation of large-scale energy system models.

They are **not** intended for direct operational or investment decisions.

---

## 7. Summary

In short:
- DC models are powerful and useful.
- Their assumptions are often reasonable.
- But under certain regimes, they can distort decisions in non-obvious ways.

This repository provides minimal, reproducible experiments to make those regimes explicit.
