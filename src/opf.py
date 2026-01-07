from __future__ import annotations

import os
from typing import Any

import pypsa


def resolve_solver_name(solver_name: str | None) -> str:
    if solver_name:
        return solver_name
    return os.environ.get("DEMO3_SOLVER", "highs")


def solve_lopf(network: pypsa.Network, solver_name: str | None = None) -> dict:
    result: Any
    solver_name = resolve_solver_name(solver_name)
    if hasattr(network, "lopf"):
        result = network.lopf(network.snapshots, solver_name=solver_name)
    else:
        result = network.optimize(solver_name=solver_name)

    return {
        "result": result,
        "objective": getattr(network, "objective", None),
        "network": network,
    }
