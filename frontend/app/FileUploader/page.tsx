'use client';

import React from "react";
import { useRouter } from "next/navigation";
import { FileUploader } from "@/components/FileUpload";
import Link from "next/link";

const Page = () => {
  const router = useRouter();

  const handleUpload = async () => {
    router.push('/Dashboard');
  };

  return (
    <div className="min-h-screen bg-canvas py-12 px-6 md:px-12 text-ink">
      <div className="max-w-3xl mx-auto space-y-8">
        
        {/* Breadcrumb & Header */}
        <div className="space-y-2 border-b border-hairline pb-6">
          <div className="eyebrow">
            <Link href="/" className="hover:text-ink">OVERVIEW</Link> <span className="mx-1">/</span> UPLOAD
          </div>
          <h1 className="font-serif text-3xl sm:text-4xl font-normal text-ink">
            Ingest Contract Document
          </h1>
          <p className="font-serif text-base text-text-muted leading-relaxed">
            Upload your commercial agreement in PDF format. The document will be analyzed locally using our 12-class transformer model and explainable risk rules.
          </p>
        </div>

        {/* Upload Card */}
        <div className="card-cream space-y-6">
          <FileUploader onFileUpload={handleUpload} />

          <div className="border-t border-hairline pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-mono text-text-muted">
            <div>
              <span className="font-bold text-ink block">01 / PRIVACY</span>
              100% in-memory local processing.
            </div>
            <div>
              <span className="font-bold text-ink block">02 / MULTI-PAGE</span>
              OCR fallback for scanned pages.
            </div>
            <div>
              <span className="font-bold text-ink block">03 / EXPLAINABLE</span>
              0–100 risk score with quotes.
            </div>
          </div>
        </div>

        {/* Action Link */}
        <div className="text-center pt-4">
          <Link
            href="/Dashboard"
            className="text-sm font-sans font-medium text-ink underline hover:text-text-muted transition"
          >
            ← Return to Dashboard
          </Link>
        </div>

      </div>
    </div>
  );
};

export default Page;