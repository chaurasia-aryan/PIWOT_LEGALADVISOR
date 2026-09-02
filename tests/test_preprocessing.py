import os
import sys
import pytest

# Add parent and Backend paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.preprocessing.document_pipeline import (
    process_contract_document,
    normalize_legal_text,
    validate_pdf_stream,
    DocumentPreprocessingError
)


def test_normalize_legal_text():
    dirty_text = "This   Agreement (“Agreement”) is  entered  into on  January\xa015, 2024.\n\n\nSection 1.2 — Termination."
    cleaned = normalize_legal_text(dirty_text)
    assert '“' not in cleaned
    assert '”' not in cleaned
    assert '\xa0' not in cleaned
    assert 'January 15, 2024' in cleaned
    assert 'Section 1.2 - Termination' in cleaned


def test_validate_pdf_stream_invalid_header():
    with pytest.raises(DocumentPreprocessingError):
        validate_pdf_stream(b"Invalid not a pdf content")


def test_validate_pdf_stream_empty():
    with pytest.raises(DocumentPreprocessingError):
        validate_pdf_stream(b"")


def test_process_sample_contract_pdf():
    sample_pdf_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "ml", "data", "sample_contracts", "sample_msa_contract.pdf")
    )
    assert os.path.exists(sample_pdf_path), f"Sample file not found: {sample_pdf_path}"

    with open(sample_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    doc_result = process_contract_document(pdf_bytes, filename="sample_msa_contract.pdf")

    assert doc_result["document_id"].startswith("doc_")
    assert doc_result["filename"] == "sample_msa_contract.pdf"
    assert doc_result["page_count"] >= 1
    assert doc_result["char_count"] > 200
    assert len(doc_result["pages"]) >= 1
    assert len(doc_result["chunks"]) >= 3
    assert any("PARTIES" in c["section"] or "TERM" in c["section"] or "COMPENSATION" in c["section"] for c in doc_result["chunks"])
