# Model Card — PIWOT Legal Advisor Clause Classifier

## 1. Model Details
* **Model Name**: PIWOT Hybrid Clause Classifier
* **Model Version**: 1.0.0
* **Architecture**: Hybrid Dense Transformer (`all-MiniLM-L6-v2` embeddings + L2-regularized Logistic Classifier) with fallback to Classical TF-IDF (1-2 grams) + Logistic Regression.
* **Intended Use**: Categorization of commercial legal provisions into 12 core functional categories and automated identification of high-risk clauses.
* **Primary License**: Apache 2.0 / MIT compatible.

---

## 2. Training Data & Category Taxonomy
Trained on curated subsets of authentic commercial contract provisions sourced from **LEDGAR / LexGLUE** and **CUAD** (CC BY 4.0 / CC-BY-NC-SA 4.0):
1. `termination`
2. `governing_law`
3. `confidentiality`
4. `indemnification`
5. `liability`
6. `payment`
7. `intellectual_property`
8. `dispute_resolution`
9. `warranty`
10. `force_majeure`
11. `non_compete`
12. `miscellaneous`

---

## 3. Evaluation & Performance Comparison

| Metric | Classical Baseline (TF-IDF + LogReg) | Transformer DL (`all-MiniLM-L6-v2`) | Delta |
|---|---|---|---|
| **Accuracy** | 56.06% | **80.30%** | **+24.24%** |
| **Macro F1** | 53.04% | **79.73%** | **+26.69%** |
| **Weighted F1** | 56.12% | **80.25%** | **+24.13%** |
| **Inference Latency (CPU)** | ~1.2 ms / clause | ~12.5 ms / clause | +11.3 ms |

---

## 4. Strengths & Limitations

### Strengths
* **High Semantic Generalization**: The dense transformer captures nuanced paraphrasing (e.g. recognizing "EACH PARTY WAIVES TRIAL BY JURY" as `dispute_resolution` even without explicit mention of "arbitration").
* **Local Execution**: Runs entirely on CPU with zero GPU requirement and zero external API dependencies.
* **Graceful Degradation**: Automatically falls back to the TF-IDF vectorizer if PyTorch or Transformer weights are unavailable.

### Limitations
* Highly domain-specific clauses (e.g., specialized maritime charterparties or pharmaceutical patent licensing milestones) may fall into `miscellaneous` if not represented in general commercial templates.
* Short sentence fragments (< 15 characters) are skipped or classified with lower confidence.
