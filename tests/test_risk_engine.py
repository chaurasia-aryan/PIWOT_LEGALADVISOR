import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))

from ml.risk.risk_engine import LegalRiskEngine


def test_risk_engine_low_risk_contract():
    engine = LegalRiskEngine()
    chunks = [
        {"category": "termination", "text": "Either party may terminate upon thirty (30) days notice.", "page_start": 1},
        {"category": "liability", "text": "Liability is capped at the total amount paid under this agreement ($100,000 USD).", "page_start": 1},
        {"category": "confidentiality", "text": "Each party shall maintain confidentiality for 5 years.", "page_start": 1},
        {"category": "dispute_resolution", "text": "Disputes shall be resolved via arbitration.", "page_start": 2},
        {"category": "governing_law", "text": "Governing law of California.", "page_start": 2}
    ]
    entities = {
        "effective_date": "2024-01-15",
        "expiry_date": "2025-01-14",
        "all_jurisdictions": ["State of California"]
    }

    report = engine.evaluate_contract_risk({}, chunks, entities)

    assert report["level"] == "Low"
    assert report["score"] < 35
    assert len(report["inconsistencies"]) == 0


def test_risk_engine_high_risk_contract_with_anomalies():
    engine = LegalRiskEngine()
    chunks = [
        {"category": "termination", "text": "Company reserves the sole right to terminate immediately without cause and without any payment.", "page_start": 1},
        {"category": "liability", "text": "Contractor agrees to accept uncapped and unlimited liability for all damages.", "page_start": 1},
        {"category": "non_compete", "text": "Non-compete covenant shall last for ten (10) years worldwide.", "page_start": 2}
    ]
    # Date anomaly: effective 2024-06-01 but expiry 2024-01-01!
    entities = {
        "effective_date": "2024-06-01",
        "expiry_date": "2024-01-01",
        "all_jurisdictions": ["State of New York", "England and Wales"]
    }

    report = engine.evaluate_contract_risk({}, chunks, entities)

    assert report["level"] == "High"
    assert report["score"] >= 70
    assert any(i["type"] == "CHRONOLOGICAL_CONTRADICTION" for i in report["inconsistencies"])
    assert any(i["type"] == "JURISDICTION_CONFLICT" for i in report["inconsistencies"])
    assert any(r["type"] == "UNCAPPED_LIABILITY" for r in report["reasons"])
    assert any(r["type"] == "UNILATERAL_TERMINATION" for r in report["reasons"])
