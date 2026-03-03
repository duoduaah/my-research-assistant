from src.preprocessing.soft_scoring import soft_score

def select_counter_claims(claims, k=5):
    """
    Select lower-ranked but still high-quality claims
    to surface limitations or contradictory evidence.
    """
    eligible = [
        c for c in claims
        if c["metadata"]["study_quality"]["evidence_strength"] in {"strong", "moderate"}
    ]

    # Lower relevance, not lower quality
    eligible = sorted(eligible, key=soft_score)

    return eligible[:k]