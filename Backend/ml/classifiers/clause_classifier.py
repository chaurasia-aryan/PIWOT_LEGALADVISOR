"""
PIWOT Legal Advisor — Production Legal Clause Classification Service
Provides high-performance inference using the trained Transformer embedding classifier
with automatic graceful fallback to the classical TF-IDF baseline.
"""

import os
import logging
import joblib
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

LEGAL_CATEGORIES = [
    "termination",
    "governing_law",
    "confidentiality",
    "indemnification",
    "liability",
    "payment",
    "intellectual_property",
    "dispute_resolution",
    "warranty",
    "force_majeure",
    "non_compete",
    "miscellaneous"
]

# High-risk trigger phrases per clause type
RISK_PATTERNS = {
    "termination": ["without cause", "immediately without notice", "sole discretion", "no refund", "without penalty"],
    "liability": ["unlimited liability", "uncapped", "consequential damages", "sole liability", "strict liability"],
    "indemnification": ["indemnify without limitation", "hold harmless against all", "sole control", "defend and hold harmless"],
    "payment": ["non-refundable", "immediate liquidated penalty", "late fee of 20%", "accelerate all remaining"],
    "non_compete": ["worldwide", "five (5) years", "ten (10) years", "any competing business", "perpetual"]
}


class LegalClauseClassifier:
    """Production clause classification service."""

    def __init__(self, model_dir: Optional[str] = None):
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "models", "clause_classifier")

        self.model_dir = model_dir
        self.encoder = None
        self.transformer_clf = None
        self.tfidf_vectorizer = None
        self.baseline_clf = None
        self.active_backend = "none"

        self._load_models()

    def _load_models(self):
        """Loads Transformer model first, falls back to TF-IDF baseline."""
        # 1. Try loading Transformer classifier
        try:
            from sentence_transformers import SentenceTransformer
            transformer_path = os.path.join(self.model_dir, "transformer_head.pkl")
            if os.path.exists(transformer_path):
                self.transformer_clf = joblib.load(transformer_path)
                self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
                self.active_backend = "transformer"
                logger.info("Loaded Transformer Clause Classifier (all-MiniLM-L6-v2 + Logistic Head).")
                return
        except Exception as e:
            logger.warning(f"Could not initialize Transformer classifier: {e}")

        # 2. Fallback to TF-IDF Baseline
        try:
            tfidf_path = os.path.join(self.model_dir, "tfidf_vectorizer.pkl")
            clf_path = os.path.join(self.model_dir, "baseline_classifier.pkl")
            if os.path.exists(tfidf_path) and os.path.exists(clf_path):
                self.tfidf_vectorizer = joblib.load(tfidf_path)
                self.baseline_clf = joblib.load(clf_path)
                self.active_backend = "tfidf_baseline"
                logger.info("Loaded TF-IDF Baseline Clause Classifier.")
                return
        except Exception as e:
            logger.warning(f"Could not initialize TF-IDF classifier: {e}")

        self.active_backend = "heuristic_fallback"
        logger.warning("Using heuristic rule-based classifier as fallback.")

    def _heuristic_classify(self, text: str) -> str:
        """Heuristic fallback based on legal keywords."""
        lower = text.lower()
        if any(k in lower for k in ["terminat", "expire", "expiration", "cancel"]):
            return "termination"
        if any(k in lower for k in ["govern", "jurisdiction", "delaware", "california", "laws of"]):
            return "governing_law"
        if any(k in lower for k in ["confidenti", "proprietary information", "non-disclosure"]):
            return "confidentiality"
        if any(k in lower for k in ["indemnif", "hold harmless", "defend"]):
            return "indemnification"
        if any(k in lower for k in ["liabilit", "damages", "consequential", "aggregate"]):
            return "liability"
        if any(k in lower for k in ["payment", "invoice", "fee", "usd", "$", "price", "installments"]):
            return "payment"
        if any(k in lower for k in ["intellectual property", "patent", "copyright", "trademark", "work made for hire"]):
            return "intellectual_property"
        if any(k in lower for k in ["arbitrat", "dispute", "jams", "mediation", "jury trial"]):
            return "dispute_resolution"
        if any(k in lower for k in ["warrant", "as is", "merchantability", "defect"]):
            return "warranty"
        if any(k in lower for k in ["force majeure", "act of god", "strike", "war", "pandemic"]):
            return "force_majeure"
        if any(k in lower for k in ["non-compete", "non-solicit", "solicit", "covenant"]):
            return "non_compete"
        return "miscellaneous"

    def classify_clause(self, text: str) -> Dict[str, Any]:
        """Classifies a single text clause."""
        if not text or len(text.strip()) == 0:
            return {
                "category": "miscellaneous",
                "confidence": 0.5,
                "model_backend": self.active_backend,
                "clause_risk": "Low"
            }

        category = "miscellaneous"
        confidence = 0.5

        if self.active_backend == "transformer" and self.encoder and self.transformer_clf:
            try:
                emb = self.encoder.encode([text], show_progress_bar=False, normalize_embeddings=True)
                probs = self.transformer_clf.predict_proba(emb)[0]
                pred_idx = int(probs.argmax())
                category = self.transformer_clf.classes_[pred_idx]
                confidence = float(probs[pred_idx])
            except Exception as e:
                logger.error(f"Transformer inference error: {e}")
                category = self._heuristic_classify(text)
                confidence = 0.7

        elif self.active_backend == "tfidf_baseline" and self.tfidf_vectorizer and self.baseline_clf:
            try:
                X = self.tfidf_vectorizer.transform([text])
                probs = self.baseline_clf.predict_proba(X)[0]
                pred_idx = int(probs.argmax())
                category = self.baseline_clf.classes_[pred_idx]
                confidence = float(probs[pred_idx])
            except Exception as e:
                logger.error(f"TF-IDF inference error: {e}")
                category = self._heuristic_classify(text)
                confidence = 0.7
        else:
            category = self._heuristic_classify(text)
            confidence = 0.75

        # Evaluate risk level based on category and trigger terms
        clause_risk = "Low"
        lower_text = text.lower()
        if category in RISK_PATTERNS:
            triggers = RISK_PATTERNS[category]
            if any(t in lower_text for t in triggers):
                clause_risk = "High"
            elif category in ["liability", "indemnification", "termination"]:
                clause_risk = "Medium"

        return {
            "category": category,
            "confidence": round(confidence, 3),
            "model_backend": self.active_backend,
            "clause_risk": clause_risk
        }

    def classify_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classifies all chunks in a document."""
        enriched = []
        for c in chunks:
            res = self.classify_clause(c["text"])
            c_copy = dict(c)
            c_copy["category"] = res["category"]
            c_copy["confidence"] = res["confidence"]
            c_copy["model_backend"] = res["model_backend"]
            c_copy["risk_level"] = res["clause_risk"]
            enriched.append(c_copy)
        return enriched
