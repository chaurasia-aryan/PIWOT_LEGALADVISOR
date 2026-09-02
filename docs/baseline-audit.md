# Baseline Repository Audit — PIWOT Legal Advisor

## 1. Executive Summary

This document establishes the architectural baseline of the **PIWOT Legal Advisor** repository prior to the ML/DL upgrade. The purpose is to document the existing frontend and backend implementations, security vulnerabilities, legacy integrations, and compatibility considerations.

---

## 2. Codebase Structure & Components

### 2.1 Backend (`/Backend`)
* **Framework**: Flask (Python 3.12 compatible) with `flask_cors` and `python-dotenv`.
* **Legacy Flow**:
  1. Receives file upload via `POST /analyze` under form-data key `resume` along with `input_text`.
  2. Uses `PyMuPDF` (`fitz`) to load **only page index 0** (`pdf_document.load_page(0)`).
  3. Renders that first page into a PNG pixmap in-memory.
  4. Encodes PNG to base64 and passes it to `google.generativeai` (`gemini-1.5-flash`).
  5. Strips markdown asterisks (`*`) and returns a raw string: `{"response": "..."}`.
* **Limitations Identified**:
  * Multi-page documents are truncated to page 1.
  * Dependency on external hosted LLM (`gemini-1.5-flash`) for all intelligence.
  * No structured extraction (no clause classification, no risk quantification, no normalized dates/amounts).
  * No OCR fallback for scanned contracts.
  * Legacy naming conventions (`resume` field from resume parser templates).

### 2.2 Frontend (`/frontend`)
* **Framework**: Next.js 15+ (App Router), React 19, TypeScript, Tailwind CSS, Axios.
* **Key Routes & Pages**:
  * `/Dashboard` (`app/Dashboard/page.tsx`): Main dashboard featuring contract statistics, dropzone upload component (`components/FileUpload.tsx`), and a contract registry table (`components/ContractTable.tsx`).
  * `/AddContract` (`app/AddContract/page.tsx`): Manual contract metadata entry form.
  * `/Services/*`: Modular service pages (`collaboration-tools`, `document-signing`, `smart-contract-parsing`, `summary-generation`).
  * `/Inbox` & `/Messages`: Placeholder messaging routes.
* **API Client (`app/Services/api.ts`)**:
  * `analyzeContract(file, inputText)`: Calls `http://localhost:5000/analyze` via multipart form data (`resume`, `input_text`).
  * Expected response: `ContractAnalysis` object.

---

## 3. Security Audit & Remediation

| Issue | Severity | Status | Remediation |
|---|---|---|---|
| Hardcoded Gemini API Key in `Backend/app.py:30` | **Critical** | **Resolved** | Removed static key; replaced with `os.getenv("GEMINI_API_KEY", "")`. Created `.env.example`. |
| Unignored `.env` files in root | **Medium** | **Resolved** | Created root `.gitignore` ignoring `.env*`, build artifacts, and dataset caches. |
| Insecure File Upload Handling | **Low** | **In Progress** | Target pipeline will implement MIME validation, file size limits (16MB), and path sanitization. |

---

## 4. Current vs. Target API Contract

### Legacy API Contract (`POST /analyze`)
```json
// Request: multipart/form-data with "resume": <PDF file>, "input_text": <string>
// Response (HTTP 200):
{
  "response": "Summary of contract terms..."
}
```

### Target ML/DL API Contract (`POST /api/analyze`)
```json
{
  "document": {
    "document_id": "doc_12345",
    "filename": "service_agreement.pdf",
    "page_count": 4,
    "char_count": 8420,
    "chunk_count": 14,
    "ocr_used": false
  },
  "summary": {
    "extractive_summary": ["Sentence 1...", "Sentence 2..."],
    "source_pages": [1, 2]
  },
  "risk": {
    "score": 68,
    "level": "Medium",
    "reasons": [
      {
        "factor": "Uncapped Liability Clause",
        "severity": "High",
        "weight": 25,
        "evidence": "Total liability shall be unlimited...",
        "page": 3
      }
    ]
  },
  "clauses": [
    {
      "chunk_id": "c_1",
      "type": "termination",
      "confidence": 0.94,
      "text": "Either party may terminate upon 30 days notice...",
      "page_start": 2,
      "page_end": 2,
      "risk_level": "Low"
    }
  ],
  "entities": {
    "parties": ["Company A Inc.", "Vendor Corp"],
    "effective_date": "2024-01-15",
    "expiry_date": "2025-01-14",
    "payment_amounts": ["$50,000 USD", "$5,000 USD/month"],
    "jurisdiction": "State of California",
    "arbitration_venue": "San Francisco, CA"
  },
  "inconsistencies": [],
  "similar_reference_clauses": []
}
```

---

## 5. Migration Strategy & Compatibility

1. **Preserve Frontend Routes**: Retain existing dashboard and navigation while upgrading `ContractTable` and `FileUpload` to render rich structured ML insights.
2. **Backward Compatibility**: Provide a backward-compatible adapter in `Backend/app.py` for `/analyze` while exposing the canonical `/api/analyze` and `/api/health` endpoints.
3. **Local-First ML Architecture**: Replace the single-page image extraction with full-document parsing, classical and transformer-based clause classification, deterministic + NER information extraction, and explainable rule/anomaly risk scoring.
