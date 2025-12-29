# Demo3 PRD — Assumption-Aware Validation of DC Power Flow
Version: v1.0 (Reframed Objective)

## 1. Background and Motivation

Large-scale energy system models such as PyPSA-GB commonly rely on
the linearised DC power flow approximation.

This modelling choice is not made because AC models are unknown,
but because DC models offer:
- computational tractability,
- scalability to national-scale systems,
- transparent system-level reasoning.

Despite its widespread use, the **validity regime of DC power flow
is often treated implicitly rather than explicitly quantified**.

This project aims to make that regime visible.

---

## 2. Research Objective (v0.1 Scope)

The objective of Demo3 v0.1 is **not to find pathological failures of DC power flow**, but to:

> **Quantify how closely DC and AC power flow agree across controlled system stress,
and identify parameter regimes where DC can be considered reliable
for system-level decision-making.**

The focus is on **decision-relevant metrics**, rather than raw numerical accuracy.

---

## 3. Research Questions

RQ1. Under typical transmission-style conditions, how large is the deviation
between DC and AC power flow results?

RQ2. How does this deviation evolve as system stress increases
(e.g. higher transfer levels or tighter line limits)?

RQ3. For which classes of system-level conclusions
(e.g. congestion identification, interface flow ranking)
does DC remain robust?

RQ4. At what point does divergence become large enough to warrant
explicit sensitivity checks?

---

## 4. System Scope and Modelling Choices

### 4.1 Network Type

- A **GB-inspired minimal transmission network** is used.
- The network is intentionally small (3–5 buses) to:
  - isolate mechanisms,
  - avoid confounding effects,
  - enable full parameter sweeps.

This is a **mechanism validation exercise**, not a national-scale reproduction.

### 4.2 Power Flow Models

Two models are compared:
- DC power flow (lossless, fixed voltage magnitude)
- AC power flow (full nonlinear reference)

Both models share identical topology, generation, and load data.

---

## 5. Experimental Design

### 5.1 Baseline Scenario

- Moderate load and transfer levels
- System operating well within limits
- Expected outcome: high agreement between DC and AC

### 5.2 Stress Sweep

A single stress dimension is swept continuously, such as:
- load scaling factor, or
- north–south transfer level, or
- effective line capacity tightening

Only **one sweep dimension** is used to maintain interpretability.

---

## 6. Evaluation Metrics (Decision-Relevant)

The comparison focuses on:
- line flow deviation (DC vs AC),
- congestion identification consistency,
- ranking agreement of constrained interfaces,
- feasibility mismatch (if any).

Absolute numerical error is secondary to **qualitative decision alignment**.

---

## 7. Expected Outcomes

Possible outcomes include:

- DC and AC results remain highly consistent across the tested range,
  supporting the continued use of DC for system-level studies.

- Divergence increases smoothly near system limits,
  suggesting clear regimes where sensitivity checks are advisable.

Both outcomes are considered valid and informative.

---

## 8. Assumptions and Limitations

- Reactive power, voltage stability, and transient dynamics
  are outside the scope of this study.
- Results apply to transmission-style networks,
  not distribution or low-voltage systems.
- Conclusions are illustrative rather than exhaustive.

All assumptions are documented explicitly in `assumptions.md`.

---

## 9. Deliverables

- Reproducible codebase implementing DC and AC comparisons
- Parameter sweep experiments with saved results
- Clear plots illustrating agreement and divergence
- `results/summary.md` describing findings and implications
- Documentation linking results to modelling practice

---

## 10. Definition of Done (v0.1)

The project is considered complete when:
- DC vs AC agreement has been quantified across at least one stress sweep
- Results are reproducible from a clean environment
- Conclusions are clearly stated and scoped
- The validity regime of DC is explicitly articulated

Reply emails or external feedback are not part of the completion criteria.

---

## 11. Intended Audience

This project is intended for:
- energy system researchers,
- open modelling practitioners,
- reviewers and users of large-scale DC-based models.

It serves as a **methodological reference**, not an operational tool.
