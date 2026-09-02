'use client';

import { useState } from 'react';
import { FileUploader } from "@/components/FileUpload";
import Button from "@/components/Button";
import { ContractTable } from "@/components/ContractTable";
import { ContractAnalysisModal } from "@/components/ContractAnalysisModal";
import { Contract, MLContractAnalysis } from "../types";
import { analyzeContract } from "../Services/api";

export default function Dashboard() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [selectedContract, setSelectedContract] = useState<Contract | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(undefined);

    try {
      // 100% dynamic analysis executed via backend on the uploaded PDF
      const mlResult: MLContractAnalysis = await analyzeContract(file);

      // Extract contracting parties
      const party1 = mlResult.entities.parties[0]?.name;
      const party2 = mlResult.entities.parties[1]?.name;
      const clientDisplayName = party1 && party2 ? `${party1} / ${party2}` : party1 || file.name.replace('.pdf', '');

      // Parse effective and expiry dates
      const effectiveDate = mlResult.entities.effective_date
        ? new Date(mlResult.entities.effective_date)
        : new Date();
      
      const expiryDate = mlResult.entities.expiry_date
        ? new Date(mlResult.entities.expiry_date)
        : new Date(Date.now() + 365 * 24 * 60 * 60 * 1000);

      const newContract: Contract = {
        id: mlResult.document.document_id,
        clientName: clientDisplayName,
        documentName: file.name,
        signedOn: effectiveDate,
        expiryOn: expiryDate,
        email: "legal-audit@piwot.ai",
        status: mlResult.risk.level === 'High' ? 'pending' : 'active',
        analysis: mlResult.summary.summary_sentences.join(" "),
        mlAnalysis: mlResult
      };

      setContracts(prev => [newContract, ...prev]);
      setSelectedContract(newContract);
      setIsModalOpen(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze contract');
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewAnalysis = (contract: Contract) => {
    setSelectedContract(contract);
    setIsModalOpen(true);
  };

  return (
    <div className="min-h-screen w-full bg-canvas py-10 px-6 md:px-12 space-y-8 text-ink">
      
      {/* Top Banner */}
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-hairline">
        <div className="space-y-1">
          <div className="eyebrow">
            DECISION-SUPPORT SYSTEM
          </div>
          <h1 className="font-serif text-3xl md:text-4xl text-ink font-normal tracking-tight">
            Contract Intelligence Dashboard
          </h1>
          <p className="font-sans text-xs md:text-sm text-text-muted">
            Multi-page document parsing, 12-class transformer classification, and explainable risk evaluation.
          </p>
        </div>
        <div className="flex gap-3 items-center">
          <Button href="/FileUploader" variant="primary" size="md">
            Upload PDF
          </Button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Prototype Legal Disclaimer Card */}
        <div className="bg-surface-secondary border border-surface-warm p-4 rounded-md flex items-center justify-between gap-4 text-xs font-serif text-ink">
          <div className="flex items-center gap-2.5">
            <span className="text-base">ℹ️</span>
            <span>
              <strong>Decision-Support Prototype:</strong> All contract parsing, clause classifications, and risk scores are computed dynamically on uploaded documents. This tool does not constitute formal legal advice.
            </span>
          </div>
          <span className="font-mono text-[11px] text-text-muted uppercase px-2 py-0.5 rounded bg-canvas border border-hairline">
            ML 2.0
          </span>
        </div>

        {/* Upload Box Card */}
        <div className="card-cream space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="font-serif text-xl font-normal text-ink">Ingest New Contract Document (.PDF)</h2>
              <p className="font-sans text-xs text-text-muted">Upload any commercial agreement to run multi-page analysis.</p>
            </div>
            <span className="eyebrow">Dynamic Analysis Pipeline</span>
          </div>
          <FileUploader onFileUpload={handleFileUpload} />
        </div>

        {/* Contract Table */}
        <div className="card-cream space-y-6">
          <ContractTable
            contracts={contracts}
            isLoading={isLoading}
            error={error}
            onViewAnalysis={handleViewAnalysis}
          />
        </div>

      </div>

      {/* Detailed Analysis Modal */}
      {selectedContract && selectedContract.mlAnalysis && (
        <ContractAnalysisModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          analysis={selectedContract.mlAnalysis}
          documentName={selectedContract.documentName}
        />
      )}
    </div>
  );
}
