def make_base_case() -> dict:
    return {
        "name": "base",
        "base_mva": 100.0,
        "buses": [
            {"id": "N", "role": "gen"},
            {"id": "M", "role": "interface"},
            {"id": "S", "role": "load_slack"},
        ],
        "lines": [
            {"id": "L1", "from": "N", "to": "M", "r": 0.01, "x": 0.10, "s_nom": 100.0},
            {"id": "L2", "from": "M", "to": "S", "r": 0.01, "x": 0.10, "s_nom": 100.0},
        ],
        "generators": [
            {
                "id": "wind_N",
                "bus": "N",
                "carrier": "wind",
                "p_nom": 80.0,
                "p_min_pu": 0.0,
                "p_max_pu": 1.0,
                "marginal_cost": 0.0,
            },
            {
                "id": "gen_S",
                "bus": "S",
                "carrier": "gas",
                "p_nom": 200.0,
                "p_min_pu": 0.0,
                "p_max_pu": 1.0,
                "marginal_cost": 50.0,
                "control": "Slack",
            },
        ],
        "loads": [
            {"id": "load_M", "bus": "M", "p_set": 0.0},
            {"id": "load_S", "bus": "S", "p_set": 80.0},
        ],
    }


def _alpha_grid(alpha_min: float, alpha_max: float, alpha_step: float) -> list[float]:
    count = int(round((alpha_max - alpha_min) / alpha_step)) + 1
    alphas = []
    for i in range(count):
        alpha = alpha_min + alpha_step * i
        alphas.append(round(float(alpha), 10))
    return alphas


def make_cases(
    alpha_min: float = 0.2,
    alpha_max: float = 1.5,
    alpha_step: float = 0.1,
    *,
    include_optional_l3: bool = False,
    load_m_mw: float | None = None,
) -> list[dict]:
    if alpha_step <= 0:
        raise ValueError("alpha_step must be positive")
    if alpha_max < alpha_min:
        raise ValueError("alpha_max must be >= alpha_min")
    alphas = _alpha_grid(alpha_min, alpha_max, alpha_step)
    cases: list[dict] = []

    for alpha in alphas:
        case = make_base_case()
        case["alpha"] = alpha
        case["name"] = f"alpha_{alpha:.2f}"

        if include_optional_l3:
            case["lines"].append(
                {"id": "L3", "from": "N", "to": "S", "r": 0.02, "x": 0.20, "s_nom": 30.0}
            )

        for gen in case["generators"]:
            if gen["id"] == "wind_N":
                gen["p_max_pu"] = alpha

        if load_m_mw is not None:
            for load in case["loads"]:
                if load["id"] == "load_M":
                    load["p_set"] = load_m_mw

        cases.append(case)

    return cases


if __name__ == "__main__":
    cases = make_cases()
    print(f"case_count={len(cases)}")
