from src.preprocessing.clean_json import clean_json
from src.config import Config

BRT = Config.get_bedrock_client()
MODEL_ID = Config.MODEL_ID
MAX_OUTPUT_TOKENS = Config.MAX_OUTPUT_TOKENS


SYSTEM_PROMPT = (
    "You are a scientific research analyst.\n\n"
    "Your task is to identify limitations, null results, or contradictory findings based only on the provided claims.\n"
    "\n"
    "You must:\n"
    "- Use ONLY the supplied claims\n"
    "- Do NOT restate the main summary\n"
    "- Highlight where evidence is weak, mixed, or context-dependent\n"
    "- Cite the claim IDs for every statement\n"
    "- Avoid speculative language\n"
    "- If no meaningful limitations exist, state that explicitly.\n\n"
    
    "Output rules(STRICT):\n"
    "- Output must follow the exact JSON schema provided(VERY STRICT):\n\n"
    "{\n"
    '"limitations": [\n'
    '    {\n'
    '    "statement": "Some trials report no significant improvement in glycemic control among patients with long-standing type 2 diabetes.",\n'
    '        "supporting_claim_ids": [\n'
    '            "paperA::003",\n'
    '        ],\n'
    '        },\n'
    '        {\n'
    '        "statement": "Some studies report limited clinical impact of AMPK activation in advanced type 2 diabetes.",\n'
    '        "supporting_claim_ids": [\n'
    '            "paperC::005"\n'
    '        ]\n'
    '        }\n'
    '    ],\n'
    "    }"
)




class CounterArgumentAgent:
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
    Your task is to identify limitations, null results, or contradictory findings based only on the provided claims.
    """.strip()


    def run_counterarg(self, claims:list):
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
