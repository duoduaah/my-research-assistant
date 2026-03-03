import numpy as np
import boto3
import faiss
import pickle


session = boto3.Session(profile_name="aws_learning")
s3 = session.client("s3", region_name="ca-central-1")


def build_faiss_index(embeddings: np.ndarray):
    """
    Builds a cosine-similarity FAISS index.
    """
    dim = len(embeddings[0])

    # Normalize vectors → cosine similarity
    #faiss.normalize_L2(embeddings)  #not needed if embedding is already normalized

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    return index


def save_index(index, metadata: list[dict], index_path: str, meta_path: str):
    """
    Saves FAISS index + metadata locally.
    """
    faiss.write_index(index, index_path)

    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)


def upload_file(local_path: str, bucket: str, s3_key: str):
    s3.upload_file(local_path, bucket, s3_key)
    print(f"Uploaded {s3_key}")