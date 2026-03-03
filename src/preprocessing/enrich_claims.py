def attach_quality_to_claims(
    claims: list[dict],
    study_quality_result: dict,
) -> list[dict]:
    """
    Attaches paper-level study quality metadata to each claim.

    Args:
        claims (list[dict]): Claims extracted from a single paper
        study_quality_result (dict): Output of study quality agent

    Returns:
        list[dict]: Claims enriched with study_quality
    """

    if not claims:
        return []

    # Fail-closed default quality
    default_quality = {
        "study_design": "unclear",
        "sample_size": "unclear",
        "bias_risk": "high",
        "evidence_strength": "weak",
        "notes": ""
    }

    quality = study_quality_result.get("study_quality", default_quality)

    enriched_claims = []

    for claim in claims:
        enriched_claim = {
            **claim,
            "study_quality": quality
        }
        enriched_claims.append(enriched_claim)

    return enriched_claims