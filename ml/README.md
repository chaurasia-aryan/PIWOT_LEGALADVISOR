# PIWOT Legal Advisor: Machine Learning & NLP Lab

This directory contains the machine learning research, datasets, Jupyter notebooks, model training pipelines, and benchmark evaluation suites for the PIWOT Legal Advisor platform.

---

## 📂 Structure

```
ml/
├── data/
│   ├── curated_clause_corpus.json       # Curated 66-clause corpus across 12 categories
│   ├── dataset_manifest.csv             # Manifest of researched public legal datasets
│   ├── dataset_manifest.json            # JSON metadata for CUAD, LEDGAR, ContractNLI
│   └── sample_contracts/                # Generated multi-page benchmark PDF contracts
│       ├── sample_msa_contract.pdf      # 2-page standard commercial MSA (Low risk)
│       └── sample_high_risk_contract.pdf# 2-page contract with anomalies & severe terms
├── models/
│   └── clause_classifier/               # Trained models (.pkl) and evaluation metrics
│       ├── classifier_model.pkl         # Production SentenceTransformer + Logistic head
│       ├── tfidf_classifier.pkl         # Baseline TF-IDF + Logistic head
│       └── metrics.json                 # Comparative evaluation metrics
├── notebooks/                           # 10 runnable Jupyter notebooks
│   ├── 01_dataset_research_and_download.ipynb
│   ├── 02_document_preprocessing.ipynb
│   ├── 03_clause_classification_baselines.ipynb
│   ├── 04_clause_classification_transformer.ipynb
│   ├── 05_legal_ner_and_key_information_extraction.ipynb
│   ├── 06_risk_scoring_and_anomaly_detection.ipynb
│   ├── 07_embeddings_and_clause_similarity.ipynb
│   ├── 08_extractive_summarization.ipynb
│   ├── 09_end_to_end_evaluation.ipynb
│   └── 10_inference_demo_on_real_contract.ipynb
├── reports/                             # Evaluation JSON & Markdown reports
│   ├── clause_classification_metrics.json
│   ├── final_metrics.json
│   └── final_metrics.md
└── src/                                 # Standalone training & evaluation scripts
    ├── data_download.py                 # Generates curated corpus and benchmark PDFs
    ├── train_clause_classifier.py       # Trains baseline and transformer models
    └── evaluate_end_to_end.py           # Evaluates full pipeline on benchmark contracts
```

---

## 🚀 Running Training and Evaluation Scripts

### 1. Generate Datasets and Benchmark Contracts
```bash
python ml/src/data_download.py
```

### 2. Train Clause Classification Models
```bash
python ml/src/train_clause_classifier.py
```
This trains both the classical TF-IDF baseline and the Transformer DL model (`all-MiniLM-L6-v2`), evaluates them with cross-validation, and saves the models to `ml/models/clause_classifier/` and `Backend/models/clause_classifier/`.

### 3. Run Full End-to-End Evaluation
```bash
python ml/src/evaluate_end_to_end.py
```
This evaluates the ingestion, clause classification, entity extraction, risk scoring, retrieval, and summarization pipelines on benchmark PDFs and exports `ml/reports/final_metrics.json` and `ml/reports/final_metrics.md`.

---

## 📊 Summary of Model Performance

- **Classifier Accuracy**: 80.30%
- **Classifier Macro F1**: 79.73%
- **Entity & Date Recall**: 100.0%
- **Contradiction Detection Recall**: 100.0%
- **Zero Hosted LLM Dependency**: 100% local CPU/GPU execution.
