from src.preprocessing.normalize_similarity import normalize_similarity
from src.preprocessing.soft_scoring import soft_score

def merge_and_rank_claims(
    retrieved_claims,
    fresh_claims,
    passes_quality_gate
):
    all_claims = []

    for c in retrieved_claims + fresh_claims:
        if not passes_quality_gate(c):
            continue
        all_claims.append(normalize_similarity(c))

    return sorted(all_claims, key=soft_score, reverse=True)