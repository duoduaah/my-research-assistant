from src.config import Config

BRT = Config.get_bedrock_client()
MODEL_ID = Config.MODEL_ID
MAX_OUTPUT_TOKENS = Config.MAX_OUTPUT_TOKENS

SYSTEM_PROMPT = (
    "You are an expert scientific research analyst.\n\n"
    "Your task is to extract explicit empirical claims from academic research papers.\n"
    "A claim must be directly supported by evidence in the provided text.\n\n"
    "Rules:\n"
    "- Focus only on results, findings, outcomes, or conclusions\n"
    "- Ignore background, literature review, methods, and references\n"
    "- Ignore speculative or future work statements\n"
    "- Do not hallucinate or infer beyond the text\n"
    "- If no extractable claims exist, return an empty list\n\n"
    
    "Output rules(STRICT):\n"
    "- Output ONLY a valid JSON array with at most 5 claim objects\n"
    "- Do NOT use markdown\n"
    "- Do NOT include explanations or comments.\n"
    "- Do NOT include paper_id or chunk identifiers.\n"
    "- Escape all quotation marks inside strings.\n"
    "- If the output would be truncated, return an empty JSON array instead"

    "- Each array element MUST match this schema:\n\n"
    "{\n"
    '   "claim": "string", \n'
    '   "evidence": "string",\n'
    '   "section": "string",\n'
    '   "strength": "strong | moderate | weak"\n'
    "}"
    
)



class ClaimExtractorAgent:
    def __init__(self, model_id: str = MODEL_ID, max_output_tokens: int = MAX_OUTPUT_TOKENS):
        self.model_id = model_id
        self.max_output_tokens = max_output_tokens


    def build_user_prompt(self, text) -> str:
        return f"""
    You are given a chunk of text from a research paper.
    Text:
    \"\"\"
    {text}
    \"\"\"
    Extract all empirical claims present in this text.
    """.strip()


    def run_claim_extractor(self, paper_id:str, chunk_id:str, text: str):
        conversation = [
            {
                "role": "user",
                "content": [{"text": self.build_user_prompt(text)}],
            },
        ]

        response = BRT.converse(
            modelId=self.model_id,
            system=[
                {
                    "text": SYSTEM_PROMPT
                }
            ],
            messages=conversation,
            inferenceConfig={
                "maxTokens": self.max_output_tokens,
                "temperature": 0.0,
            },
        )

        stop_reason = response.get("stopReason", "")
        if stop_reason == "max_tokens":
            print(f"Output truncated for paper_id: {paper_id}, chunk_id:{chunk_id}")
            return[]

        output_text = response["output"]["message"]["content"][0]["text"]

        return output_text
