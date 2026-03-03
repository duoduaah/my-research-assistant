import numpy as np
import boto3
from src.config import Config
from src.embeddings.embedder import Embedding
from src.embeddings.load_index import get_index_metadata

MODEL_ID = Config.EMBED_MODEL_ID
MAX_OUTPUT_TOKENS = Config.MAX_OUTPUT_TOKENS

BRT = Config.get_bedrock_client()
embedder = Embedding(MODEL_ID, BRT)
index, metadata = get_index_metadata()


def append_claims(new_claims: list[dict]):
        """
        Appends new claims to an existing FAISS index.
        new_claims: claims per single paper
        """

        if not new_claims:
            print("Empty text to embed")
            return None

        claims_list = [
        {
            "id": f"{claim['paper_id']}::{idx:03d}",
            "embedding_text": f"Claim: {claim['claim']} Evidence: {claim['evidence']}",
            "metadata": {
                "paper_id": claim['paper_id'],
                "claim": claim['claim'],
                "evidence": claim['evidence'],
                "section": claim['sections'],
                "study_quality": claim['study_quality'],
                "title": claim['title']
            }
        }
        for idx, claim in enumerate(new_claims, start=1)
        ]

        # 1. Build embedding text
        texts = [
            f"{c['embedding_text']}" for c in claims_list
        ]

        # 2. Embed
        embeddings = [
            embedder.get_embedder(text=x, dimensions=256,) for x in texts
        ]
        embeddings = np.array(embeddings, dtype="float32")
        
        # 4. Append to index
        index.add(embeddings)

        # 5. Append metadata in SAME ORDER
        metadata.extend(claims_list)
        print("Index and metadata updated!")

        return claims_list

        