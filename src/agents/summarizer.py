from src.config import Config

BRT = Config.get_bedrock_client()
MODEL_ID = Config.MODEL_ID
MAX_OUTPUT_TOKENS = Config.MAX_OUTPUT_TOKENS

SYSTEM_PROMPT = (
    "You are a scientific research summarization agent.\n\n"
    "You are given a ranked list of empirical claims extracted from academic papers.\n"
    "Claims are ordered from highest to lowest importance.\n\n"
    "You must:\n"
    "- Base the summary ONLY on the provided claims\n"
    "- Give more emphasis to higher-ranked claims\n"
    "- Explicitly cite the claim IDs used for every factual statement\n"
    "- Merge similar claims into coherent points where appropriate\n"
    "- Highlight disagreements or contradictory findings\n"
    "- Avoid introducing any new facts\n"
    "- If claims are insufficient to answer the question, say so explicitly.\n\n"
    
    "Output rules(STRICT):\n"
    "- Output must follow the exact JSON schema provided:\n\n"
    "{\n"
    '"summary": [\n'
    '    {\n'
    '    "statement": "AMPK activation improves insulin sensitivity and glucose uptake in skeletal muscle.",\n'
    '        "supporting_claim_ids": [\n'
    '            "paperA::003",\n'
    '            "paperB::001"\n'
    '        ]\n,'
    '        evidence_strength: "strong | moderate | low. \n'
    '        },\n'
    '        {\n'
    '        "statement": "Some studies report limited clinical impact of AMPK activation in advanced type 2 diabetes.",\n'
    '        "supporting_claim_ids": [\n'
    '            "paperC::005"\n'
    '        ]\n,'
    '        evidence_strength: "strong | moderate | low. \n'
    '        }\n'
    '    ],\n'
    '    "confidence_note": "Most evidence is derived from randomized controlled trials and animal models."\n'
    "    }"
)




class SummarizeAgent:
    def __init__(self, model_id: str = MODEL_ID, max_output_tokens: int = MAX_OUTPUT_TOKENS):
        self.model_id = model_id
        self.max_output_tokens = max_output_tokens


    def build_user_prompt(self, text) -> str:
        return f"""
    You are given a list of empirical claims from research papers.
    Text:
    \"\"\"
    {text}
    \"\"\"
    Summarize.
    """.strip()


    def run_summarizer(self, claims:list):
        conversation = [
            {
                "role": "user",
                "content": [{"text": self.build_user_prompt(claims)}],
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
            print(f"Output truncated")
            return[]

        output_text = response["output"]["message"]["content"][0]["text"]

        return output_text
