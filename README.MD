# Research Assistant

A prototype research assistant that automates literature review tasks using modular agents, embeddings, and retrieval. 

## Primary workflow
1. User submits a research question (e.g. "Does intermittent fasting improve metabolic health in adults?")
2. Planner Agent decomposes the question into ordered subtasks.
3. Search Agent finds relevant papers (metadata + abstracts) via web/paper search tools.
4. Claim Extraction Agent extracts key claims, methods, sample size, conclusions and indexes them into a vector DB.
5. Evaluation Agent scores study quality (sample size, design, bias, confounders, reproducibility) and produces justification.
6. Synthesis Agent writes a structured summary with inline citations.
7. Counterargument Agent generates limitations and opposing evidence.
8. Report Generator outputs a PDF or slide deck.

## Agents
- Planner Agent — task decomposition
- Search Agent — paper discovery (arXiv, Semantic Scholar, etc.)
- Claim Extraction Agent — extract claims and metadata
- Evaluation Agent — quality scoring and rationale
- Synthesis Agent — final structured report with citations
- Counterargument Agent — limitations and opposing evidence

## Tools & Components
- Web / Paper search connectors (arXiv API, Semantic Scholar, Kaggle, etc.)
- PDF loader and parser
- Embeddings + vector store (long-term memory)
- Python utility functions for scoring and parsing
- File generator for PDF / slide export

