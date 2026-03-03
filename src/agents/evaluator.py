from src.preprocessing.clean_json import clean_json
from src.config import Config

BRT = Config.get_bedrock_client()
MODEL_ID = Config.MODEL_ID



class QualityEvaluatorAgent:
    def __init__(self):
        pass
    
    def build_user_prompt(self, data: dict) -> str:
        return f"""
    You are a scientific study quality assessment agent.

    Your role is to evaluate the reliability of a research study based strictly on the provided claims and metadata.

    Data:
    \"\"\"
    {data}
    \"\"\"

    Guidelines:
    - Do not infer methods or details that are not explicitly supported by the provided information.
    - If any information is missing or unclear, explicitly mark it as "unclear."
    - Be conservative in your assessment and avoid overconfidence in your conclusions.

    Output:
    - Return ONLY a valid JSON object that adheres to the following schema:
    {{
    "paper_id": "...",
    "study_quality": {{
        "study_design": "RCT | observational | cohort | meta-analysis | unclear",
        "sample_size": "large | medium | small | unclear",
        "bias_risk": "low | moderate | high",
        "evidence_strength": "strong | moderate | weak",
        "notes": "short justification grounded in claims"
    }}
    }}

    Strict Rules:
    - Do NOT include any additional text, explanations, or comments outside the JSON object.
    - Ensure the JSON is well-formed and adheres to the schema exactly.
    """.strip()


    def evaluate_study_quality(self, data:dict):
        conversation = [
        {
            "role": "user",
            "content": [{"text":self.build_user_prompt(data)}]
        }
        ]
        response = BRT.converse(
            modelId= MODEL_ID,
            messages=conversation
            # add more config
        )

        raw_output = response["output"]["message"]["content"][0]["text"]
        cleaned_output = clean_json(raw_output)
        
        return cleaned_output

