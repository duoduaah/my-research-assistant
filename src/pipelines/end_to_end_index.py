import sys
from pathlib import Path

project_root = Path.cwd().parent
sys.path.append(str(project_root))

from src.config import Config
from src.agents.paper_searcher import SearchAgent
from src.agents.claim_extractor import ClaimExtractorAgent
from src.agents.evaluator import QualityEvaluatorAgent
from src.retrieval.search_tool import run_search
from src.retrieval.claim_extraction import ClaimsService
from src.pipelines.paper_ingestion import PaperIngestionService
from src.preprocessing.chunk import chunk_paper
from src.preprocessing.quality_validation import validate_study_quality
from src.preprocessing.enrich_claims import attach_quality_to_claims
from src.embeddings.update_index import append_claims

""" 
from research_assistant.src.agents.paper_searcher import SearchAgent
from research_assistant.src.agents.claim_extractor import ClaimExtractorAgent
from research_assistant.src.agents.evaluator import QualityEvaluatorAgent
from research_assistant.src.retrieval.search_tool import run_search
from research_assistant.src.retrieval.claim_extraction import ClaimsService
from research_assistant.src.pipelines.paper_ingestion import PaperIngestionService
from research_assistant.src.preprocessing.chunk import chunk_paper
from research_assistant.src.preprocessing.quality_validation import validate_study_quality
from research_assistant.src.preprocessing.enrich_claims import attach_quality_to_claims
from research_assistant.src.embeddings.update_index import append_claims
"""

SEARCH_MODEL = Config.SEARCH_MODEL_ID


def test(user_query: str, limit:int=10):

    search_agent = SearchAgent(
        llm_id=SEARCH_MODEL,
        search_tool=run_search
    )
    papers = search_agent.run(user_query, limit)
    print(f"Number of papers: {len(papers)}")
    
    #
    papers_text = []
    ingestion = PaperIngestionService()
    for paper in papers:
        try:
            paper["text"] = ingestion.get_text(paper)
            papers_text.append(paper)
        except Exception as e:
            print(f"Error processing paper {paper.get('id', 'unknown')}: {e}")
            papers_text.append({})

    print(f"Paper_text length: {len(papers_text)}")
    #
    claim_agent = ClaimExtractorAgent()
    claim_service = ClaimsService(claim_agent)
    evaluator = QualityEvaluatorAgent()
    fresh_claims = []

    for paper in papers_text:
        if not paper:
            continue
        chunks = chunk_paper(paper["id"], paper["text"])
        chunks_claims = claim_service.process_chunks(chunks)
        paper_claims = claim_service.aggregate_claims(chunks_claims, paper["id"])
        claimed_paper = {
        "paper_id":paper["id"],
        "metadata":{
            "title": paper["title"],
            "year": paper["year"],
            "venue": paper["venue"],
            "field_of_study": paper["fieldsOfStudy"],
            "publication_type": paper["publicationTypes"]
        },
        "claims": paper_claims
        }
        if not paper_claims:
            print("nothing to index")
            return
        print("Claims extracted")
        evaluated = evaluator.evaluate_study_quality(claimed_paper)
        validated = validate_study_quality(evaluated)
        enriched_claims = attach_quality_to_claims(claimed_paper["claims"], validated)
        updated_claims = [{**claim, "paper_id":claimed_paper['paper_id'], "title":claimed_paper['metadata']['title']} for claim in enriched_claims]
        print("Claims enriched")
        final_claims = append_claims(updated_claims)
        fresh_claims.append(final_claims)

    return fresh_claims

