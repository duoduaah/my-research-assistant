import json
import hashlib
import time
from pathlib import Path
from semanticscholar import SemanticScholar

BASE_DIR = Path(__file__).resolve().parents[2]
CACHE_DIR = BASE_DIR / "cache" / "semantic_scholar"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_TTL_SECONDS = 7 * 24 * 60 * 60 # 7 days

def _make_cache_key(payload: dict) -> str:
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


_scholar = None

def _get_scholar():
    global _scholar
    if _scholar is None:
        _scholar = SemanticScholar(timeout=10)
    return _scholar


def paper_search_tool(query: str, max_results: int = 8) -> list:
    """
    Search papers from semantic scholar and return metadata.
    
    Input:
        query (str): keyword query
        max_results (int): number of papers to return
    
    Output:
        Dictionary with status and search outcome information
        Error: {
            "status": "error",
            "error_message": f'Semantic scholar request failed ...'}
        Success:{
            "status": "success",
            "data": List of dicts with fields:
                "id": str
                "title": str,
                "authors": [str],
                "year": int or None,
                "abstract": str or None,
                "pdf_url": str or None
        }
    """

    cache_payload = {
        "query": query,
        "max_results": max_results,
        "source": "semantic_scholar",
    }

    cache_key = _make_cache_key(cache_payload)
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < CACHE_TTL_SECONDS:
            return json.loads(cache_file.read_text())

    fields = ['paperId', 'publicationVenue', 'title', 'venue', 'year', 'openAccessPdf', 'fieldsOfStudy', 's2FieldsOfStudy', 'publicationTypes', 'journal']
   
    scholar = _get_scholar()
    try:
        response = scholar.search_paper(query, 
                                        open_access_pdf=True,
                                        limit=max_results,
                                        fields=fields
                                        )
        data = response.raw_data
    except Exception as e:
        return {
            "status":"error",
            "error_message": f'Semantic scholar request failed: {str(e)}'}


    papers = []
    for item in data:
        paper = {
            "id": item.get("paperId"),
            "title": item.get("title"),
            #"authors":[author.get("name") for author in item.get("authors")],
            "year": item.get("year"),
            "venue": item.get("venue", "Unknown"),
            "fieldsOfStudy": item.get("fieldsOfStudy", "Unknown"),
            "publicationTypes": item.get("publicationTypes", "Unknown"),
            "pdf_url": item["openAccessPdf"].get("url")
        }
        papers.append(paper)

    cache_file.write_text(json.dumps(papers))

    return papers