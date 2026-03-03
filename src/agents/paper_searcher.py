import sys
import boto3
from pathlib import Path
from botocore.exceptions import ClientError
from src.config import Config

BRT = Config.get_bedrock_client()


class SearchAgent:
    def __init__(self, llm_id, search_tool):
        self.llm = llm_id
        self.search_tool = search_tool

    def build_prompt(self, question):
        return f"""
You are an academic search keyword extraction agent.

Your task:
- Convert the research question into 3 - 5 concise academic search keywords.
- Keywords must be suitable for searching scholarly databases.

STRICT OUTPUT RULES:
- Output ONLY the keywords.
- Do NOT add explanations, introductions, or commentary.
- Do NOT use full sentences.
- Do NOT include bullet points.
- Do NOT include labels.
- Do NOT include quotation marks.
- Separate keywords with commas only.

Incorrect output example:
Based on the question, the keywords are: "early childhood, screen exposure"

Correct output example:
early childhood, screen exposure, cognitive development

Research question:
{question}
"""
    
    def extract_keywords(self, question):
        prompt = self.build_prompt(question)
        conversation = [
            {
                "role": "user",
                "content": [{"text":prompt}]
            }
        ]
        try:
            response = BRT.converse(modelId=self.llm,
                            messages=conversation,
                            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9}
                            )
            keywords = response["output"]["message"]["content"][0]["text"]

        except (ClientError, Exception) as e:
            print(f"ERROR: can't invoke '{self.llm}'. Reason: {e}")
            
        return keywords.strip()
    

    def run(self, question, limit=5):
        keywords = self.extract_keywords(question)
        print(" Extracted keywords:", keywords)
        papers = self.search_tool(keywords, limit)
        return papers


"""
from src.agents.paper_searcher import SearchAgent
from src.services.paper_search import paper_search_tool

MODEL_ID = 'meta.llama3-8b-instruct-v1:0'
search_agent = SearchAgent(
    llm_id = MODEL_ID,
    search_tool = paper_search_tool
)
question = "What are the benefits of intermittent fasting"
papers = search_agent.run(question, limit=5)

"""
