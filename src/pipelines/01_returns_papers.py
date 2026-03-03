
"""
Script to search for papers using a language model and a search tool.

Parameters
----------
SEARCH_MODEL : str
    The model ID to use for the search agent (e.g., "meta.llama3-8b-instruct-v1:0").
user_query : str
    The user query string to search for relevant papers.

Returns
-------
papers : list
    List of papers returned by the search agent.
"""

import argparse
from research_assistant.src.agents.paper_searcher import SearchAgent
from research_assistant.src.retrieval.search_tool import run_search

def main(SEARCH_MODEL: str, user_query: str):
    search_agent = SearchAgent(
        llm_id=SEARCH_MODEL,
        search_tool=run_search
    )
    question = user_query
    papers = search_agent.run(question, limit=10)
    #print(papers)
    return papers

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for papers using a language model and search tool.")
    parser.add_argument("--SEARCH_MODEL", type=str, required=True, help="Model ID for the search agent.")
    parser.add_argument("--user_query", type=str, required=True, help="User query string.")
    args = parser.parse_args()
    main(args.SEARCH_MODEL, args.user_query)


