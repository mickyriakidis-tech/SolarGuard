def calculate_costs(risk_score):
    if risk_score is None:
        return {"NORMAL": float('inf'), "PROTECTIVE": float('inf'), "LIMITED": 0}

    return {
        "NORMAL": 100 * risk_score,
        "PROTECTIVE": 20 + 15 * risk_score,
        "LIMITED": 25 + 20 * risk_score,
    }