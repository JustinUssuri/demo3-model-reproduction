from __future__ import annotations

from typing import Any

import pypsa


def solve_ac_pf(network: pypsa.Network) -> dict:
    result: Any = network.pf()

    if isinstance(result, tuple):
        converged = bool(result[0])
    elif isinstance(result, bool):
        converged = result
    else:
        converged = bool(getattr(network, "pf_converged", False))

    return {
        "converged": converged,
        "line_p0": network.lines_t.p0.copy(),
        "line_p1": network.lines_t.p1.copy(),
        "vm_pu": network.buses_t.v_mag_pu.copy(),
        "va_rad": network.buses_t.v_ang.copy(),
        "network": network,
    }
