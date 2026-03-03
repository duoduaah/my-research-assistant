import sys
import numpy as np
from pathlib import Path

project_root = Path.cwd().parent
sys.path.append(str(project_root))

from src.config import Config
from src.embeddings.embedder import Embedding
from src.embeddings.load_index import get_index_metadata
from src.pipelines.end_to_end_index import test
from src.preprocessing.quality_gate import passes_quality_gate
from src.preprocessing.merge_and_rank_claims import merge_and_rank_claims
from src.preprocessing.clean_json import clean_json
from src.agents.summarizer import SummarizeAgent


bedrock_client = Config.get_bedrock_client()
embedder = Embedding(Config.EMBED_MODEL_ID, bedrock_client)
summarizer = SummarizeAgent()


def get_retrieved_claims(user_query, k:int=2):
    index, metadata = get_index_metadata()
    embeddings = embedder.get_embedder(text=user_query, dimensions=256)
    embeddings = np.array(embeddings, dtype="float32").reshape(1, -1)
    scores, indices = index.search(embeddings, k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        item = metadata[idx].copy()
        item["similarity_score"] = float(score)
        results.append(item)
    results = [{**x, "source":"retrieved"} for x in results]

    return results


def get_fresh_claims(user_query, k:int=4):
    fresh_claims = test(user_query, k)
    fresh_claims = [item for sublist in fresh_claims for item in sublist]
    fresh_claims = [{**x, "source":"fresh"} for x in fresh_claims]

    return fresh_claims


def run_summary(retrieved, fresh):
    merged_claims = merge_and_rank_claims(retrieved, fresh, passes_quality_gate)
    summarized = clean_json(summarizer.run_summarizer(merged_claims))

    return summarized


