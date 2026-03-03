import json

STRENGTH_RANK = {
    "weak": 1,
    "moderate": 2,
    "strong": 3,
}

class ClaimsService:
    def __init__(self, claims_agent):
        self.claims_agent = claims_agent

        
    def _clean_json(self, json_text:str) -> list:
        cleaned_json = json_text.strip()
        cleaned_json = cleaned_json.removeprefix("```json").removesuffix("```").strip()
        try:
            return json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return [] 
    

    def process_chunks(self, chunks:list):
        if not chunks:
            print("Error, no chunks")
        
        chunk_outputs = []
        for chunk in chunks:
            claims = self.claims_agent.run_claim_extractor(chunk["paper_id"], chunk["chunk_id"], chunk["text"])
            if not claims:
                continue
            claims = self._clean_json(claims)
            claims_dict = {
                "paper_id": chunk.get("paper_id", ""),
                "chunk_id": chunk.get("chunk_id", ""),
                "claims": claims
            }
            chunk_outputs.append(claims_dict)

        return chunk_outputs
    
    
    def aggregate_claims(self, chunk_outputs: list, paper_id: str):
        """
        Aggregates claims extracted from multiple chunks of the same paper.

        Args:
            chunk_outputs (list): List of dicts, each containing:
                - chunk_id
                - claims (list of claim dicts)
            paper_id (str): Paper identifier

        Returns:
            dict: Aggregated paper-level claims
        """

        aggregated = {}

        for chunk in chunk_outputs:
            chunk_id = chunk["chunk_id"]
            claims = chunk.get("claims", [])

            for c in claims:
                claim_text = c["claim"].strip()

                if claim_text not in aggregated:
                    aggregated[claim_text] = {
                        "claim": claim_text,
                        "evidence": set(),
                        "sections": set(),
                        "strength": c.get("strength", "moderate"),
                        "source_chunks": set(),
                    }

                aggregated_entry = aggregated[claim_text]

                aggregated_entry["evidence"].add(c.get("evidence", "").strip())
                aggregated_entry["sections"].add(c.get("section", "unknown"))
                aggregated_entry["source_chunks"].add(chunk_id)

                # Upgrade strength if stronger evidence appears
                current_strength = aggregated_entry["strength"]
                new_strength = c.get("strength", "moderate")

                if STRENGTH_RANK.get(new_strength, 0) > STRENGTH_RANK.get(
                    current_strength, 0
                ):
                    aggregated_entry["strength"] = new_strength

        # Convert sets to lists for JSON compatibility
        final_claims = []
        for entry in aggregated.values():
            final_claims.append(
                {
                    "claim": entry["claim"],
                    "evidence": list(entry["evidence"]),
                    "sections": list(entry["sections"]),
                    "strength": entry["strength"],
                    "source_chunks": list(entry["source_chunks"]),
                }
            )

        return final_claims
        