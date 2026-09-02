'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { FileUploader } from '@/components/FileUpload';

export default function Home() {
  const router = useRouter();

  const handleQuickUpload = async () => {
    // Navigate to dashboard which handles the full analysis state
    router.push('/Dashboard');
  };

  return (
    <div className="w-full flex flex-col">
      
      {/* 1. HERO BAND (Warm Ivory Canvas #faf9f5) */}
      <section className="bg-canvas text-ink py-20 md:py-28 px-6 md:px-12 border-b border-hairline">
        <div className="max-w-4xl mx-auto space-y-6 text-left">
          <div className="eyebrow">
            LOCAL-FIRST CONTRACT INTELLIGENCE
          </div>
          
          <h1 className="font-sans font-bold text-4xl sm:text-6xl md:text-7xl tracking-tight leading-[1.08] text-ink">
            Legal precision without cloud latency or data exposure.
          </h1>

          <p className="font-serif text-lg sm:text-2xl text-ink leading-relaxed font-normal pt-2">
            PIWOT Legal Advisor executes full multi-page PDF ingestion, 12-class transformer clause classification, ISO 8601 entity normalization, and 0–100 explainable risk scoring—completely locally on your machine with zero external API dependencies.
          </p>

          <div className="pt-6 flex flex-wrap items-center gap-4">
            <Link
              href="/Dashboard"
              className="inline-flex items-center justify-center bg-ink text-canvas font-sans font-medium px-8 py-3.5 rounded-sm hover:opacity-90 transition-opacity text-base"
            >
              Open Dashboard
            </Link>
            <Link
              href="/FileUploader"
              className="inline-flex items-center justify-center bg-canvas text-ink font-sans font-medium px-8 py-3.5 rounded-sm border border-ink hover:bg-surface-secondary transition-colors text-base"
            >
              Upload PDF Contract
            </Link>
          </div>
        </div>
      </section>

      {/* 2. ARCHITECTURAL FEATURE BAND (True Black #000000 Full-Bleed) */}
      <section className="bg-inverse text-canvas py-24 px-6 md:px-12">
        <div className="max-w-6xl mx-auto space-y-12">
          
          <div className="space-y-3">
            <div className="font-mono text-xs uppercase tracking-wider text-text-secondary">
              CORE SYSTEM CAPABILITIES
            </div>
            <h2 className="font-serif text-3xl sm:text-5xl font-normal text-canvas tracking-tight">
              An engineering-first legal intelligence pipeline.
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            
            {/* Card 1 */}
            <div className="bg-[#141413] border border-[#3d3d3a] rounded-md p-8 space-y-3">
              <div className="font-mono text-xs text-accent-cactus uppercase">01 / INGESTION & OCR</div>
              <h3 className="font-sans font-bold text-xl text-canvas">Multi-Page PDF Extraction & OCR</h3>
              <p className="font-serif text-base text-text-secondary leading-relaxed font-normal">
                PyMuPDF extracts digital text streams across all pages while an automated Tesseract fallback triggers for scanned pages. Normalizes legal numbering and generates chunk boundaries.
              </p>
            </div>

            {/* Card 2 */}
            <div className="bg-[#141413] border border-[#3d3d3a] rounded-md p-8 space-y-3">
              <div className="font-mono text-xs text-accent-sky uppercase">02 / NLP CLASSIFICATION</div>
              <h3 className="font-sans font-bold text-xl text-canvas">Transformer Clause Classifier</h3>
              <p className="font-serif text-base text-text-secondary leading-relaxed font-normal">
                Fine-tuned SentenceTransformer (<code className="text-xs bg-[#242422] px-1.5 py-0.5 rounded">all-MiniLM-L6-v2</code>) classifying clauses across 12 legal categories with 80.30% Accuracy and 79.73% Macro F1.
              </p>
            </div>

            {/* Card 3 */}
            <div className="bg-[#141413] border border-[#3d3d3a] rounded-md p-8 space-y-3">
              <div className="font-mono text-xs text-accent-clay uppercase">03 / RISK QUANTIFICATION</div>
              <h3 className="font-sans font-bold text-xl text-canvas">Explainable Risk & Anomaly Engine</h3>
              <p className="font-serif text-base text-text-secondary leading-relaxed font-normal">
                Deterministic 0–100 risk scoring flagging uncapped liability, non-compete overreach (&gt;24 months), unilateral termination, and cross-clause chronological date contradictions.
              </p>
            </div>

            {/* Card 4 */}
            <div className="bg-[#141413] border border-[#3d3d3a] rounded-md p-8 space-y-3">
              <div className="font-mono text-xs text-accent-fig uppercase">04 / ZERO-LLM SUMMARIZATION</div>
              <h3 className="font-sans font-bold text-xl text-canvas">TextRank Extractive Summarizer</h3>
              <p className="font-serif text-base text-text-secondary leading-relaxed font-normal">
                Graph-based centrality ranking that extracts the highest-information sentences directly from the source contract text with verified page citations.
              </p>
            </div>

          </div>

        </div>
      </section>

      {/* 3. INTERACTIVE BENCHMARK & QUICK UPLOAD (Cream Canvas #faf9f5) */}
      <section className="bg-canvas text-ink py-20 px-6 md:px-12 border-b border-hairline">
        <div className="max-w-5xl mx-auto space-y-10">
          
          <div className="text-center space-y-3">
            <div className="eyebrow">TRY IN REAL TIME</div>
            <h2 className="font-serif text-3xl sm:text-4xl text-ink font-normal">
              Analyze a commercial contract in seconds.
            </h2>
            <p className="font-sans text-sm text-text-muted max-w-xl mx-auto">
              Upload any PDF agreement to run multi-page OCR, clause segmentation, entity extraction, and risk quantification locally.
            </p>
          </div>

          <div className="card-cream max-w-2xl mx-auto">
            <FileUploader onFileUpload={handleQuickUpload} />
          </div>

          <div className="text-center">
            <Link
              href="/Dashboard"
              className="text-sm font-sans font-medium text-ink underline hover:text-text-muted transition"
            >
              Or view pre-loaded benchmark contracts in the Dashboard →
            </Link>
          </div>

        </div>
      </section>

      {/* 4. FOOTER BAND (True Black #000000 Full-Bleed) */}
      <footer className="bg-inverse text-canvas py-16 px-6 md:px-12">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-8 border-b border-[#3d3d3a] pb-12">
          <div>
            <span className="font-sans font-bold text-xl text-canvas">
              PIWOT <span className="text-text-secondary font-mono font-normal mx-0.5">\</span> LEGAL ADVISOR
            </span>
            <p className="font-serif text-sm text-text-secondary mt-2">
              An offline, privacy-first legal decision-support system.
            </p>
          </div>
          <div className="flex gap-6 text-sm font-sans text-text-secondary">
            <Link href="/Dashboard" className="hover:text-canvas transition">Dashboard</Link>
            <Link href="/FileUploader" className="hover:text-canvas transition">Uploader</Link>
            <Link href="https://github.com/chaurasia-aryan/PIWOT_LEGALADVISOR" target="_blank" className="hover:text-canvas transition">GitHub Repository</Link>
          </div>
        </div>
        <div className="max-w-6xl mx-auto pt-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-xs font-mono text-text-tertiary">
          <div>⚖️ Decision-Support Prototype. Does not constitute formal legal advice.</div>
          <div>MIT License • Local CPU/GPU Architecture</div>
        </div>
      </footer>

    </div>
  );
}
