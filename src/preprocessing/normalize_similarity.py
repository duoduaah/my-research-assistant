#needed for fresh claims to be passed through passes_quality_gate
def normalize_similarity(claim, default_sim=0.6):
    if "similarity_score" not in claim or claim["similarity_score"] is None:
        claim["similarity_score"] = default_sim
    return claim