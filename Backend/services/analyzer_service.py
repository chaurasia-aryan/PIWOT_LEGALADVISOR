"""
PIWOT Legal Advisor — Backend Analysis Orchestration Service
Coordinates all local ML/DL components into a single deterministic inference pipeline.
"""

import time
import logging
from typing import Dict, Any, Optional

from ml.preprocessing.document_pipeline import process_contract_document, DocumentPreprocessingError
from ml.classifiers.clause_classifier import LegalClauseClassifier
from ml.ner.entity_extractor import LegalEntityExtractor
from ml.risk.risk_engine import LegalRiskEngine
from ml.retrieval.clause_retriever import ClauseSimilarityRetriever
from ml.summarization.extractive_summarizer import ExtractiveContractSummarizer

logger = logging.getLogger(__name__)


class ContractAnalysisService:
    """Singleton-style service encapsulating all pipeline models."""

    def __init__(self):
        logger.info("Initializing ML Analysis Models...")
        self.classifier = LegalClauseClassifier()
        self.extractor = LegalEntityExtractor()
        self.risk_engine = LegalRiskEngine()
        self.retriever = ClauseSimilarityRetriever()
        self.summarizer = ExtractiveContractSummarizer(max_summary_sentences=4)
        logger.info("ML Analysis Models Initialized Successfully.")

    def analyze_pdf_document(self, pdf_bytes: bytes, filename: str = "contract.pdf") -> Dict[str, Any]:
        """Runs the complete local ML/DL legal contract analysis pipeline."""
        start_time = time.time()

        # 1. Document Extraction & Normalization
        doc_schema = process_contract_document(pdf_bytes, filename=filename)

        # 2. Clause Classification
        classified_chunks = self.classifier.classify_chunks(doc_schema["chunks"])

        # 3. Key Information & Legal Entity Extraction
        entities = self.extractor.extract_all_entities(doc_schema["full_text"])

        # 4. Risk Scoring & Contradiction Detection
        risk_report = self.risk_engine.evaluate_contract_risk(doc_schema, classified_chunks, entities)

        # 5. Semantic Similarity Benchmark Retrieval
        for c in classified_chunks:
            if c.get("risk_level") in ["High", "Medium"] or c.get("category") in ["liability", "termination", "indemnification"]:
                c["similar_standard_clauses"] = self.retriever.find_similar_reference_clauses(c["text"], top_k=1)
            else:
                c["similar_standard_clauses"] = []

        # 6. Extractive Summarization (Zero LLM)
        summary_report = self.summarizer.summarize(doc_schema["pages"], num_sentences=4)

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "document": {
                "document_id": doc_schema["document_id"],
                "filename": doc_schema["filename"],
                "page_count": doc_schema["page_count"],
                "char_count": doc_schema["char_count"],
                "chunk_count": len(doc_schema["chunks"]),
                "ocr_used": doc_schema["ocr_used"]
            },
            "summary": summary_report,
            "risk": risk_report,
            "clauses": classified_chunks,
            "entities": entities,
            "inconsistencies": risk_report.get("inconsistencies", []),
            "metadata": {
                "classifier_backend": self.classifier.active_backend,
                "latency_ms": elapsed_ms,
                "disclaimer": "PIWOT Legal Advisor is an AI decision-support system and does not provide formal legal advice or guarantee legal validity."
            }
        }
