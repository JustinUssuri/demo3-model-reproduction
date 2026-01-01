from __future__ import annotations

from typing import Any

import pypsa


def solve_lopf(network: pypsa.Network, solver_name: str = "highs") -> dict:
    result: Any
    if hasattr(network, "lopf"):
        result = network.lopf(network.snapshots, solver_name=solver_name)
    else:
        result = network.optimize(solver_name=solver_name)

    return {
        "result": result,
        "objective": getattr(network, "objective", None),
        "network": network,
    }
