import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))

from ml.ner.entity_extractor import LegalEntityExtractor, normalize_to_iso_date


def test_normalize_to_iso_date():
    assert normalize_to_iso_date("January 15, 2024") == "2024-01-15"
    assert normalize_to_iso_date("15th Jan 2024") == "2024-01-15"
    assert normalize_to_iso_date("2024-06-01") == "2024-06-01"
    assert normalize_to_iso_date("12/31/2023") == "2023-12-31"


def test_extract_all_entities_from_sample():
    sample_text = """
    This Master Services Agreement is entered into as of January 15, 2024 by and between
    Apex Global Solutions Inc. ('Client') and Quantum Byte Technologies LLC ('Service Provider').
    The Agreement shall expire on January 14, 2025.
    Either party may terminate upon thirty (30) days prior written notice.
    Client shall pay a total fee of $150,000 USD in monthly installments of $12,500 USD Net 30 days.
    Late fees accrue at 1.5% per month.
    This Agreement shall be governed by the laws of the State of California.
    Any dispute shall be submitted to arbitration administered by JAMS in San Francisco, California.
    """

    extractor = LegalEntityExtractor()
    entities = extractor.extract_all_entities(sample_text)

    assert len(entities["parties"]) >= 2
    assert any("Apex Global" in p["name"] for p in entities["parties"])
    assert any("Quantum Byte" in p["name"] for p in entities["parties"])
    assert entities["effective_date"] == "2024-01-15"
    assert entities["expiry_date"] == "2025-01-14"
    assert "30 days" in entities["notice_period"]
    assert any("$150,000" in amt for amt in entities["monetary_amounts"])
    assert any("1.5%" in pct for pct in entities["percentages"])
    assert "State of California" in entities["governing_jurisdiction"]
    assert any("JAMS in San Francisco" in v for v in entities["dispute_venues"])
