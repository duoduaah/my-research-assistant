def passes_quality_gate(claim):
    sq = claim.get("metadata", {}).get("study_quality")

    if not sq:
        return False

    if sq.get("study_design") not in {
        "rct", "systematic_review", "meta_analysis", "controlled_trial"
    }:
        return False

    if sq.get("bias_risk") not in {"low", "moderate"}:
        return False

    return True