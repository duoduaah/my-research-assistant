def build_final_response(user_query, summary_output, counter_output):
    key_findings = summary_output["summary"]
    limitations = counter_output.get("limitations", [])

    citation_ids = set()
    for item in key_findings + limitations:
        citation_ids.update(item.get("supporting_claim_ids", []))

    return {
        "query":user_query,
        "answer": {
            "key_findings": key_findings,
            "confidence_note": summary_output.get("confidence_note", "")
        },
        "limitations": limitations,
        "metadata": {
            "num_supporting_claims": len(citation_ids),
            "num_limitations": len(limitations),
            "citation_ids": sorted(citation_ids)
        }
    }