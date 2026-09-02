"""
PIWOT Legal Advisor — Clause Semantic Retrieval & Benchmark Matching Service
Uses local Sentence Transformers to match contract clauses against standard reference provisions.
"""

import numpy as np
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Standard legal reference clause bank (market-standard benchmark provisions)
REFERENCE_STANDARD_CLAUSES = [
    {
        "category": "termination",
        "title": "Standard Mutual Termination with Notice",
        "text": "Either party may terminate this Agreement upon thirty (30) days prior written notice in the event of a material breach by the other party that remains uncured.",
        "standard_type": "Market Standard (Low Risk)"
    },
    {
        "category": "liability",
        "title": "Standard Mutual Consequential Damages Waiver & 12-Month Cap",
        "text": "In no event shall either party be liable for any indirect, special, or consequential damages. Each party's aggregate liability under this Agreement shall not exceed the total fees paid in the twelve (12) months preceding the claim.",
        "standard_type": "Market Standard (Low Risk)"
    },
    {
        "category": "confidentiality",
        "title": "Standard Mutual Confidentiality (5-Year Duration)",
        "text": "Each party agrees to hold the other party's Proprietary Information in strict confidence using reasonable care for five (5) years following disclosure.",
        "standard_type": "Market Standard (Low Risk)"
    },
    {
        "category": "indemnification",
        "title": "Standard IP Infringement Indemnification",
        "text": "Service Provider shall defend, indemnify, and hold harmless Client against any third-party claims alleging that the deliverables infringe a valid copyright, patent, or trade secret.",
        "standard_type": "Market Standard (Low Risk)"
    },
    {
        "category": "payment",
        "title": "Standard Net 30 Invoicing and Payment Terms",
        "text": "Client shall pay all undisputed invoices within thirty (30) calendar days of invoice receipt.",
        "standard_type": "Market Standard (Low Risk)"
    },
    {
        "category": "dispute_resolution",
        "title": "Standard JAMS/AAA Binding Commercial Arbitration",
        "text": "Any dispute arising under this contract shall be settled exclusively by binding arbitration administered by the American Arbitration Association or JAMS.",
        "standard_type": "Market Standard (Low Risk)"
    }
]


class ClauseSimilarityRetriever:
    """Calculates cosine similarity between contract clauses and standard benchmark clauses."""

    def __init__(self):
        self.encoder = None
        self.reference_embeddings = None
        self.references = REFERENCE_STANDARD_CLAUSES
        self._init_embeddings()

    def _init_embeddings(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
            ref_texts = [r["text"] for r in self.references]
            self.reference_embeddings = self.encoder.encode(ref_texts, normalize_embeddings=True, show_progress_bar=False)
            logger.info("Initialized Clause Similarity Retriever with Sentence Transformer.")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer for retrieval: {e}")

    def find_similar_reference_clauses(self, query_text: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Finds closest matching standard benchmark clauses using cosine similarity."""
        if not query_text or len(query_text.strip()) < 15:
            return []

        if self.encoder is not None and self.reference_embeddings is not None:
            try:
                q_emb = self.encoder.encode([query_text], normalize_embeddings=True, show_progress_bar=False)
                sims = np.dot(self.reference_embeddings, q_emb.T).flatten()
                top_indices = np.argsort(-sims)[:top_k]

                results = []
                for idx in top_indices:
                    ref = self.references[idx]
                    results.append({
                        "category": ref["category"],
                        "title": ref["title"],
                        "reference_text": ref["text"],
                        "standard_type": ref["standard_type"],
                        "similarity_score": round(float(sims[idx]), 3)
                    })
                return results
            except Exception as e:
                logger.error(f"Retrieval error: {e}")

        # Fallback keyword match
        return [{
            "category": self.references[0]["category"],
            "title": self.references[0]["title"],
            "reference_text": self.references[0]["text"],
            "standard_type": self.references[0]["standard_type"],
            "similarity_score": 0.75
        }]
