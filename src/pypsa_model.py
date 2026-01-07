from __future__ import annotations

from typing import Iterable

import pandas as pd
import pypsa

try:
    from src.cases import make_cases
except ModuleNotFoundError:
    from cases import make_cases


def build_network(case: dict, snapshots: Iterable[float] | None = None) -> pypsa.Network:
    if snapshots is None:
        snapshots = [case.get("alpha", 0.0)]

    base_mva = float(case.get("base_mva", 1.0))
    if base_mva <= 0:
        raise ValueError("base_mva must be positive")
    line_scale = 1.0 / base_mva

    network = pypsa.Network()
    network.set_snapshots(list(snapshots))

    for bus in case["buses"]:
        network.add("Bus", bus["id"])

    for line in case["lines"]:
        network.add(
            "Line",
            line["id"],
            bus0=line["from"],
            bus1=line["to"],
            r=float(line["r"]) * line_scale,
            x=float(line["x"]) * line_scale,
            s_nom=line["s_nom"],
        )

    for gen in case["generators"]:
        kwargs: dict = {
            "bus": gen["bus"],
            "carrier": gen.get("carrier"),
            "p_nom": gen["p_nom"],
            "p_min_pu": gen.get("p_min_pu", 0.0),
            "p_max_pu": gen.get("p_max_pu", 1.0),
            "marginal_cost": gen.get("marginal_cost", 0.0),
        }
        if gen.get("control"):
            kwargs["control"] = gen["control"]
        network.add("Generator", gen["id"], **kwargs)

    for load in case["loads"]:
        network.add("Load", load["id"], bus=load["bus"], p_set=load.get("p_set", 0.0))

    if not network.generators.empty:
        gen_p_max = pd.DataFrame(1.0, index=network.snapshots, columns=network.generators.index)
        for gen in case["generators"]:
            if "p_max_pu" in gen:
                gen_p_max[gen["id"]] = float(gen["p_max_pu"])
        network.generators_t.p_max_pu = gen_p_max

    if not network.loads.empty:
        load_p_set = pd.DataFrame(0.0, index=network.snapshots, columns=network.loads.index)
        for load in case["loads"]:
            load_p_set[load["id"]] = float(load.get("p_set", 0.0))
        network.loads_t.p_set = load_p_set

    return network


def _basic_stats(network: pypsa.Network) -> dict:
    snapshots = list(network.snapshots)
    total_load = 0.0
    if not network.loads_t.p_set.empty:
        total_load = float(network.loads_t.p_set.sum(axis=1).iloc[0])

    total_gen = 0.0
    if not network.generators.empty:
        total_gen = float(network.generators.p_nom.sum())

    total_line_rating = 0.0
    if not network.lines.empty:
        total_line_rating = float(network.lines.s_nom.sum())

    return {
        "snapshots": snapshots,
        "bus_count": len(network.buses),
        "line_count": len(network.lines),
        "gen_count": len(network.generators),
        "load_count": len(network.loads),
        "total_load_mw": total_load,
        "total_gen_p_nom_mw": total_gen,
        "total_line_s_nom_mva": total_line_rating,
    }


if __name__ == "__main__":
    case = make_cases(alpha_min=1.0, alpha_max=1.0, alpha_step=0.1)[0]
    network = build_network(case)
    stats = _basic_stats(network)
    print("basic_network_stats")
    for key, value in stats.items():
        print(f"{key}={value}")
