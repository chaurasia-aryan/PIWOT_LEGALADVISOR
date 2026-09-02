'use client';

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Button from "@/components/Button";

const Page = () => {
  const router = useRouter();
  const [clientName, setClientName] = useState("");
  const [docName, setDocName] = useState("");
  const [effectiveDate, setEffectiveDate] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => {
      router.push("/Dashboard");
    }, 1200);
  };

  return (
    <div className="min-h-screen bg-canvas py-12 px-6 md:px-12 text-ink">
      <div className="max-w-xl mx-auto space-y-8">
        
        {/* Breadcrumb & Header */}
        <div className="space-y-2 border-b border-hairline pb-6">
          <div className="eyebrow">
            <Link href="/" className="hover:text-ink">OVERVIEW</Link> <span className="mx-1">/</span> MANUAL ENTRY
          </div>
          <h1 className="font-serif text-3xl font-normal text-ink">
            Register Contract Record
          </h1>
          <p className="font-serif text-sm text-text-muted leading-relaxed">
            Record manual contractual entries into your legal repository for metadata indexing.
          </p>
        </div>

        {/* Form Card */}
        <div className="card-cream space-y-6">
          {submitted ? (
            <div className="text-center py-8 space-y-2">
              <div className="text-2xl">✓</div>
              <h3 className="font-serif text-xl text-ink font-normal">Contract Record Registered</h3>
              <p className="font-sans text-xs text-text-muted">Redirecting to Dashboard...</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-1.5">
                <label htmlFor="client-name" className="eyebrow block">
                  Contracting Entity / Client Name
                </label>
                <input
                  id="client-name"
                  type="text"
                  required
                  placeholder="e.g. Apex Global Solutions LLC"
                  value={clientName}
                  onChange={(e) => setClientName(e.target.value)}
                  className="input-field w-full"
                />
              </div>

              <div className="space-y-1.5">
                <label htmlFor="doc-name" className="eyebrow block">
                  Document Agreement Title
                </label>
                <input
                  id="doc-name"
                  type="text"
                  required
                  placeholder="e.g. Master Services Agreement 2024"
                  value={docName}
                  onChange={(e) => setDocName(e.target.value)}
                  className="input-field w-full"
                />
              </div>

              <div className="space-y-1.5">
                <label htmlFor="effective-date" className="eyebrow block">
                  Effective Date (ISO 8601)
                </label>
                <input
                  id="effective-date"
                  type="date"
                  value={effectiveDate}
                  onChange={(e) => setEffectiveDate(e.target.value)}
                  className="input-field w-full"
                />
              </div>

              <div className="pt-2 flex justify-between items-center">
                <Link
                  href="/Dashboard"
                  className="text-xs font-sans text-text-muted hover:text-ink transition"
                >
                  Cancel
                </Link>
                <Button variant="primary" size="md">
                  Save Record
                </Button>
              </div>
            </form>
          )}
        </div>

      </div>
    </div>
  );
};

export default Page;
