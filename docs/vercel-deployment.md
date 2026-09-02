# Vercel Production Deployment Guide

This guide details how to deploy the **PIWOT Legal Advisor** full-stack application (Next.js 15 Frontend + Serverless Backend) to **Vercel** with working document parsing, 12-class clause classification, risk quantification, and extractive summarization.

---

## 🏗️ Architecture on Vercel

```
                               ┌──────────────────────────────────────────────┐
                               │             Vercel Cloud Edge                │
                               │                                              │
Client Browser ───────────────►│  Next.js 15 App Router (Anthropic Design UI) │
                               │  ├─ / (Homepage Band Rhythm)                 │
                               │  ├─ /Dashboard (Contract Intelligence)       │
                               │  ├─ /FileUploader (PDF Dropzone)             │
                               │  └─ /AddContract (Manual Metadata Entry)     │
                               │                                              │
                               │  Serverless Route Handlers                   │
                               │  ├─ GET  /api/health                         │
                               │  └─ POST /api/analyze                        │
                               └──────────────────────┬───────────────────────┘
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       │                                                             │
                       ▼                                                             ▼
         [Default: Zero-Config Mode]                              [Optional: High-Compute Mode]
      Vercel Serverless Intelligence Engine                     Remote Python Backend Proxy
      • In-memory PDF text extraction (`pdf-parse`)             • Target: Render / Railway / EC2
      • 12-class legal taxonomy classification                  • PyMuPDF + SentenceTransformer
      • 0–100 explainable risk & anomaly scoring                • Enabled via `PYTHON_BACKEND_URL`
      • Extractive TextRank summarizer with page citations      
      • ISO 8601 NER metadata extraction
```

---

## 🚀 Option 1: Deploy via Vercel Dashboard (1-Click Git Import)

1. **Push your repository to GitHub / GitLab / Bitbucket**:
   ```bash
   git add .
   git commit -m "feat: complete Anthropic UI redesign and Vercel serverless integration"
   git push origin main
   ```

2. **Open Vercel Dashboard**:
   - Navigate to [https://vercel.com/new](https://vercel.com/new).
   - Select your repository (`PIWOT_LEGALADVISOR`).

3. **Configure Project Settings**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `./` (or `frontend` if deploying frontend folder directly)
   - **Build Command**: `cd frontend && npm run build` (automatic via `vercel.json`)
   - **Output Directory**: `frontend/.next` (automatic via `vercel.json`)

4. **Environment Variables (Optional)**:
   | Variable | Value | Purpose |
   | :--- | :--- | :--- |
   | `PYTHON_BACKEND_URL` | `https://your-python-backend.onrender.com` | *(Optional)* If you host the heavy PyTorch/SentenceTransformers backend externally. If omitted, the built-in Vercel Serverless Intelligence Engine runs natively. |
   | `NEXT_PUBLIC_API_URL` | *Leave empty* | Automatically uses relative `/api` on Vercel. |

5. **Click "Deploy"**:
   - Vercel will install dependencies, compile the 15 routes, and provide your live URL (e.g. `https://piwot-legal-advisor.vercel.app`).

---

## ⚡ Option 2: Deploy via Vercel CLI

1. **Log in to Vercel CLI**:
   ```bash
   vercel login
   ```

2. **Deploy Preview**:
   ```bash
   vercel
   ```

3. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

## 🔍 Verifying the Live Vercel Deployment

Once deployed, run these verification steps on your live URL:

1. **Health Check**:
   ```bash
   curl https://your-deployment-url.vercel.app/api/health
   ```
   *Expected Response:*
   ```json
   {
     "status": "healthy",
     "mode": "vercel-serverless",
     "engine": "PIWOT Legal Advisor 2.0 (Hybrid Serverless & Remote ML Proxy)",
     "categories": 12,
     "timestamp": "2026-09-02T15:15:00.000Z"
   }
   ```

2. **Live Document Ingestion**:
   - Open `https://your-deployment-url.vercel.app/Dashboard` in your browser.
   - Drag and drop a commercial contract PDF into the upload card.
   - The analysis modal will automatically display:
     - Document statistics (Pages, Sections, Character count)
     - Extractive summary sentences with source page citations `[P. 1]`
     - Risk evaluation matrix with weighted severity scores
     - 12-class segmented legal clauses with standard benchmark references
     - Extracted contracting parties, effective/expiry dates, monetary sums, and governing laws.
