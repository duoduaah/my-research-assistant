from src.preprocessing.normalize import normalize_enum


ALLOWED_STUDY_DESIGN = {
    "rct", "observational", "cohort", "meta-analysis", "unclear"
}

ALLOWED_SAMPLE_SIZE = {
    "large", "medium", "small", "unclear"
}

ALLOWED_BIAS_RISK = {
    "low", "moderate", "high"
}

ALLOWED_EVIDENCE_STRENGTH = {
    "strong", "moderate", "weak"
}


def validate_study_quality(raw_output: dict) -> dict:
    sq = raw_output.get("study_quality", {})

    validated = {
        "study_design": normalize_enum(
            sq.get("study_design"),
            ALLOWED_STUDY_DESIGN
        ),
        "sample_size": normalize_enum(
            sq.get("sample_size"),
            ALLOWED_SAMPLE_SIZE
        ),
        "bias_risk": normalize_enum(
            sq.get("bias_risk"),
            ALLOWED_BIAS_RISK,
            default="high"   # conservative default
        ),
        "evidence_strength": normalize_enum(
            sq.get("evidence_strength"),
            ALLOWED_EVIDENCE_STRENGTH,
            default="weak"
        ),
        "notes": sq.get("notes", "").strip()[:500]
    }

    return {
        "paper_id": raw_output.get("paper_id"),
        "study_quality": validated
    }