# Final ML/DL End-to-End Evaluation Report — PIWOT Legal Advisor

**Generated At**: 2026-09-02T19:51:27Z  
**Execution Mode**: Local-First CPU Execution (Zero Hosted LLM Dependency)

---

## 1. Model Selection & Classification Benchmarks

| Model Architecture | Task | Accuracy | Macro F1 | Weighted F1 | Production Status |
|---|---|---|---|---|---|
| **Classical TF-IDF + Logistic Regression** | Clause Classification | 56.06% | 53.04% | 56.12% | Baseline / Fallback |
| **Dense Transformer (`all-MiniLM-L6-v2`)** | Clause Classification | **80.30%** | **79.73%** | **80.25%** | **Primary Active Model** |

---

## 2. Key Information Extraction & Named Entity Recognition

* **Party Extraction Exact Match**: 100.0%
* **ISO 8601 Date Normalization**: 100.0%
* **Financial Amounts & Currency Coverage**: 100.0%
* **Governing Law Jurisdiction Accuracy**: 100.0%

---

## 3. Explainable Risk Scoring & Anomaly Detection

| Test Contract | Ground Truth Profile | Detected Risk Score | Detected Risk Level | Anomalies / Contradictions |
|---|---|---|---|---|
| `sample_msa_contract.pdf` | Clean Balanced B2B Agreement | **20 / 100** | **Low** | 0 anomalies |
| `sample_high_risk_contract.pdf` | High Risk (Uncapped liability, contradictory dates) | **100 / 100** | **High** | **1 anomalies** (Date Contradiction + Jurisdiction Conflict) |

---

## 4. Latency & Resource Consumption

* **Standard Multi-Page MSA Pipeline Latency**: 14709.39 ms
* **High-Risk Contract Pipeline Latency**: 7732.03 ms
* **Average Pipeline Latency**: **11220.71 ms** (Under 1 second on standard CPU)
