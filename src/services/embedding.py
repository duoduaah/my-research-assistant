from botocore.client import BaseClient
from typing import List
import numpy as np


class Embedding:
    def __init__(self, model_id:str, bedrock_client:BaseClient, index, metadata:List[dict]):
        self.model_id = model_id
        self.bedrock_client = bedrock_client
        self.index = index
        self.metadata = metadata


    def get_titan_embedding(self, 
        text: str,
        dimensions: int = 1024,
        normalize: bool = True,
    ) -> List[float]:
        """
        Generate a vector embedding for input text using Amazon Titan Text Embeddings V2.

        Parameters
        ----------
        text : str
            Text to convert into an embedding vector.
        bedrock_client : botocore.client.BaseClient
            Boto3 client configured for the Amazon Bedrock Runtime service.
        dimensions : int, optional
            Dimensionality of the output embedding vector. Defaults to 1024.
        normalize : bool, optional
            Whether to normalize the output embedding vector. Defaults to True.

        Returns
        -------
        list of float
            Embedding vector representing the input text.
        """

        body = json.dumps({
            "inputText": text,
            "dimensions": dimensions,
            "normalize": normalize,
        })

        response = self.bedrock_client.invoke_model(
            modelId=self.model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        try:
            response_body = json.loads(response["body"].read())
        except Exception as e:
            raise RuntimeError(f"Failed to parse Bedrock response: {response}") from e

        embedding = response_body.get("embedding")
        if embedding is None:
            raise RuntimeError(f"Unexpected Bedrock response: {response_body}")

        return embedding
    

    def append_claims(self,
        new_claims: list[dict],
    ):
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
            self.get_titan_embedding(text=x, dimensions=256,) for x in texts
        ]
        embeddings = np.array(embeddings, dtype="float32")
        
        # 4. Append to index
        self.index.add(embeddings)

        # 5. Append metadata in SAME ORDER
        self.metadata.extend(claims_list)

        return None
        