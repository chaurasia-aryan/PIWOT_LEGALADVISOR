# Legal Dataset Research & Acquisition Strategy — PIWOT Legal Advisor

## 1. Overview

Building a locally runnable, reliable ML/DL legal contract analysis engine requires curated, permissively licensed datasets across three core tasks:
1. **Clause Classification**: Categorizing contract paragraphs into standard legal categories (Termination, Indemnification, Governing Law, Liability, Payment, etc.).
2. **Legal Named Entity & Key Information Extraction (NER/KEI)**: Identifying contracting parties, effective/expiry dates, monetary values, payment terms, and jurisdictions.
3. **Risk Scoring & Anomaly Detection**: Detecting high-risk provisions (e.g. uncapped liability, one-sided termination) and contradictory contractual terms.

---

## 2. Investigated Datasets & Benchmark Evaluation

### 2.1 CUAD (Contract Understanding Atticus Dataset)
* **Provider**: The Atticus Project & Stanford Law (Hendrycks et al.)
* **Source**: `https://huggingface.co/datasets/atticus_project/cuad`
* **License**: **Creative Commons Attribution 4.0 International (CC BY 4.0)**
* **Domain**: 510 commercial contracts curated from SEC EDGAR filings with 13,000+ expert annotations across 41 legal categories.
* **Role in PIWOT**: Serves as the ground-truth benchmark for contract clause spans, risk factor triggers (e.g. Uncapped Liability, Non-Compete, Exclusivity), and multi-page contract validation.

### 2.2 LEDGAR / LexGLUE
* **Provider**: Tuggener et al. / Chalkidis et al. (ACL 2022)
* **Source**: `https://huggingface.co/datasets/lex_glue`
* **License**: **CC-BY-NC-SA 4.0**
* **Domain**: 80,000+ contract provisions from SEC filings categorized into standard provision types.
* **Role in PIWOT**: Primary corpus for training and evaluating supervised clause classifiers (TF-IDF + Linear baseline vs. Legal-BERT / Transformer fine-tuning). We focus on the top 12–16 primary commercial categories:
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

### 2.3 ContractNLI
* **Provider**: Stanford NLP (Koreeda & Manning)
* **Source**: `https://huggingface.co/datasets/koreeda/contract_nli`
* **License**: **CC BY 4.0**
* **Domain**: 607 NDAs annotated for Natural Language Inference (Entailment, Contradiction, Neutral) across 17 contractual obligations.
* **Role in PIWOT**: Validates rule-based inconsistency checks, contradiction logic, and missing obligation detection.

### 2.4 Legal NER Corpus
* **Provider**: Hugging Face / LegalBench
* **License**: **CC BY 4.0**
* **Domain**: Commercial contracts annotated for entities (Parties, Dates, Jurisdictions, Monetary Values, Legislation).
* **Role in PIWOT**: Supplements deterministic regex engines with semantic entity boundaries for party names and governing law courts.

---

## 3. Dataset Acquisition & Synthesis Pipeline

To ensure 100% reproducibility and self-contained execution without reliance on live remote network downloads during deployment, the dataset pipeline builds:
1. A curated benchmark split of authentic legal clauses across all 12 key categories (`ml/data/curated_clause_corpus.json`).
2. Multi-page sample contracts with ground-truth entities and risk flags (`ml/data/sample_contracts/`).
3. Automated dataset download and loading routines in `ml/src/data_download.py` and `ml/notebooks/01_dataset_research_and_download.ipynb`.
