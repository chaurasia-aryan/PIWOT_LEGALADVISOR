import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))

from ml.retrieval.clause_retriever import ClauseSimilarityRetriever
from ml.summarization.extractive_summarizer import ExtractiveContractSummarizer


def test_clause_similarity_retriever():
    retriever = ClauseSimilarityRetriever()
    query_clause = "Either party may terminate this agreement upon providing thirty (30) days notice in writing."
    matches = retriever.find_similar_reference_clauses(query_clause, top_k=2)

    assert len(matches) >= 1
    assert matches[0]["category"] == "termination"
    assert matches[0]["similarity_score"] > 0.5
    assert "Standard" in matches[0]["title"]


def test_extractive_contract_summarizer():
    pages = [
        {
            "page": 1,
            "text": "This Master Services Agreement is entered into between Apex Corp and Quantum Byte LLC. The agreement governs cloud AI services. Total compensation is $150,000 USD payable monthly."
        },
        {
            "page": 2,
            "text": "Either party may terminate with 30 days notice. All disputes shall be settled by arbitration in California. Each party agrees to maintain strict confidentiality."
        }
    ]

    summarizer = ExtractiveContractSummarizer(max_summary_sentences=3)
    summary_result = summarizer.summarize(pages, num_sentences=3)

    assert "summary_sentences" in summary_result
    assert len(summary_result["summary_sentences"]) <= 3
    assert len(summary_result["source_pages"]) >= 1
    assert summary_result["method"] in ["extractive_textrank", "chronological_fallback"]
