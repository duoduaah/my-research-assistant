def soft_score(claim):
    sim = claim["similarity_score"]  # 0–1 cosine
    sq = claim["metadata"]["study_quality"]

    design_bonus = {
        "meta_analysis": 1.0,
        "systematic_review": 0.9,
        "rct": 0.8,
        "controlled_trial": 0.7,
    }.get(sq["study_design"], 0.0)

    bias_penalty = {
        "low": 1.0,
        "moderate": 0.85
    }.get(sq["bias_risk"], 0.0)

    return (
        0.5 * sim +
        0.3 * design_bonus +
        0.2 * bias_penalty
    )