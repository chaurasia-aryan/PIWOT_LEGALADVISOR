import io
import os
import sys
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert "models" in data


def test_models_endpoint(client):
    res = client.get("/api/models")
    assert res.status_code == 200
    data = res.get_json()
    assert data["local_execution"] is True
    assert data["llm_dependency"] is False
    assert "termination" in data["supported_categories"]


def test_analyze_endpoint_missing_file(client):
    res = client.post("/api/analyze", data={})
    assert res.status_code == 400
    data = res.get_json()
    assert "error" in data


def test_analyze_endpoint_with_valid_pdf(client):
    sample_pdf_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "ml", "data", "sample_contracts", "sample_msa_contract.pdf")
    )
    with open(sample_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    data = {
        "file": (io.BytesIO(pdf_bytes), "sample_msa_contract.pdf")
    }

    res = client.post("/api/analyze", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    payload = res.get_json()

    assert "document" in payload
    assert payload["document"]["filename"] == "sample_msa_contract.pdf"
    assert payload["document"]["page_count"] >= 1
    assert "risk" in payload
    assert payload["risk"]["level"] in ["Low", "Medium", "High"]
    assert "clauses" in payload
    assert len(payload["clauses"]) >= 2
    assert "entities" in payload
    assert "summary" in payload
    assert len(payload["summary"]["summary_sentences"]) >= 1


def test_legacy_analyze_adapter_endpoint(client):
    sample_pdf_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "ml", "data", "sample_contracts", "sample_msa_contract.pdf")
    )
    with open(sample_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    data = {
        "resume": (io.BytesIO(pdf_bytes), "sample_msa_contract.pdf"),
        "input_text": "Please summarize"
    }

    res = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    payload = res.get_json()

    assert "response" in payload
    assert "CONTRACT SUMMARY" in payload["response"]
    assert "risk" in payload
    assert "clauses" in payload
