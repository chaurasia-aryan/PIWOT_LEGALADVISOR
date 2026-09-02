"""
PIWOT Legal Advisor — Extractive Contract Summarization Service
Implements a non-LLM graph-based TextRank sentence extraction algorithm
preserving exact source sentence offsets and page references.
"""

import re
import numpy as np
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer


class ExtractiveContractSummarizer:
    """Extracts the most salient sentences across multi-page contracts using TextRank."""

    def __init__(self, max_summary_sentences: int = 5):
        self.max_summary_sentences = max_summary_sentences

    def split_into_sentences(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Splits document text into individual sentences with page tracking."""
        sentences = []
        for p in pages:
            page_num = p["page"]
            text = p["text"]
            if not text:
                continue

            # Split on sentence boundaries (e.g. . ! ? followed by space/newline)
            raw_sents = re.split(r'(?<=[.!?])\s+', text)
            for s in raw_sents:
                clean_s = s.strip()
                # Discard short titles or numbering artifacts
                if len(clean_s) > 30 and not clean_s.isupper() and not clean_s.startswith("Page "):
                    sentences.append({
                        "text": clean_s,
                        "page": page_num,
                        "char_count": len(clean_s)
                    })
        return sentences

    def summarize(self, pages: List[Dict[str, Any]], num_sentences: int = 5) -> Dict[str, Any]:
        """Generates an extractive summary using TextRank graph centrality."""
        all_sentences = self.split_into_sentences(pages)

        if not all_sentences:
            return {
                "summary_sentences": ["No extractable sentence content found in contract."],
                "source_pages": [1],
                "method": "extractive_textrank"
            }

        if len(all_sentences) <= num_sentences:
            return {
                "summary_sentences": [s["text"] for s in all_sentences],
                "source_pages": sorted(list(set(s["page"] for s in all_sentences))),
                "method": "extractive_textrank"
            }

        try:
            # Build TF-IDF similarity matrix
            sent_texts = [s["text"] for s in all_sentences]
            vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
            tfidf_mat = vectorizer.fit_transform(sent_texts)

            # Cosine similarity graph
            sim_matrix = (tfidf_mat * tfidf_mat.T).toarray()
            np.fill_diagonal(sim_matrix, 0)

            # Power iteration / PageRank on adjacency matrix
            # Damping factor d = 0.85
            d = 0.85
            n = sim_matrix.shape[0]
            scores = np.ones(n) / n

            row_sums = sim_matrix.sum(axis=1, keepdims=True)
            row_sums[row_sums == 0] = 1.0
            norm_matrix = sim_matrix / row_sums

            for _ in range(30):
                scores = (1 - d) / n + d * np.dot(norm_matrix.T, scores)

            # Prioritize first sentence (usually parties/scope) + top scored sentences
            top_indices = list(np.argsort(-scores)[:num_sentences])
            if 0 not in top_indices:
                top_indices[-1] = 0

            # Sort indices chronologically to preserve narrative flow
            top_indices.sort()

            selected_sentences = [all_sentences[i]["text"] for i in top_indices]
            selected_pages = sorted(list(set(all_sentences[i]["page"] for i in top_indices)))

            return {
                "summary_sentences": selected_sentences,
                "source_pages": selected_pages,
                "method": "extractive_textrank"
            }
        except Exception as e:
            # Fallback to first N sentences
            fallback_sents = [s["text"] for s in all_sentences[:num_sentences]]
            return {
                "summary_sentences": fallback_sents,
                "source_pages": [all_sentences[0]["page"]],
                "method": "chronological_fallback"
            }
