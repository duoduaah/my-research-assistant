from botocore.client import BaseClient
from typing import List
import json
from src.config import Config

MODEL_ID = Config.EMBED_MODEL_ID
MAX_OUTPUT_TOKENS = Config.MAX_OUTPUT_TOKENS
BRT = Config.get_bedrock_client()


class Embedding:
    def __init__(self, model_id:str=MODEL_ID, bedrock_client:BaseClient=BRT):
        self.model_id = model_id
        self.bedrock_client = bedrock_client


    def get_embedder(self, 
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