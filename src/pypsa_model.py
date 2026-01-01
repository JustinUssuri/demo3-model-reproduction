from __future__ import annotations

from typing import Iterable

import pandas as pd
import pypsa


def build_network(case: dict, snapshots: Iterable[float] | None = None) -> pypsa.Network:
    if snapshots is None:
        snapshots = [case.get("alpha", 0.0)]

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
            r=line["r"],
            x=line["x"],
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
