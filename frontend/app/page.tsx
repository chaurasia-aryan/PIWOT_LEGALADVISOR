'use client';

import { useState } from 'react';
import { FileUploader } from '@/components/FileUploader';
import { ContractTable } from '@/components/ContractTable';
import { Button } from '@/components/Button';
import { Contract } from './types';

export default function Dashboard() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [selectedContract, setSelectedContract] = useState<Contract | null>(null);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [error, setError] = useState<string>();

  const handleUploadSuccess = (file: File, analysis: string) => {
    const newContract: Contract = {
      id: `${Date.now()}-${file.name}`,
      clientName: 'Unknown',
      documentName: file.name,
      signedOn: new Date(),
      expiryOn: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
      email: 'unknown@example.com',
      analysis,
      status: 'pending',
    };
    setContracts(prev => [newContract, ...prev]);
    setError(undefined);
  };

  const handleViewAnalysis = (contract: Contract) => {
    setSelectedContract(contract);
    setShowAnalysis(true);
  };

  return (
    <div className="space-y-10 max-w-5xl mx-auto">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
        <h1 className="text-4xl font-extrabold tracking-tight">Contract Dashboard</h1>
        <Button href="#" variant="primary" size="md">
          Add New Contract
        </Button>
      </div>

      <div className="card">
        <h2 className="text-2xl font-semibold mb-4">Upload Contract</h2>
        <FileUploader
          onUploadSuccess={handleUploadSuccess}
          onUploadError={(error) => setError(error.message)}
        />
        {error && <div className="mt-4 text-red-400 text-center">{error}</div>}
      </div>

      <ContractTable
        contracts={contracts}
        isLoading={false}
        error={undefined}
        onViewAnalysis={handleViewAnalysis}
      />

      {showAnalysis && selectedContract && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
          <div className="bg-neutral-900 rounded-xl p-8 max-w-2xl w-full max-h-[80vh] overflow-y-auto shadow-2xl border border-neutral-700">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-2xl font-bold">Contract Analysis</h3>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setShowAnalysis(false)}
              >
                Close
              </Button>
            </div>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-neutral-300">Document Details</h4>
                <p className="text-sm text-neutral-400">
                  {selectedContract.documentName} - {selectedContract.clientName}
                </p>
              </div>
              <div>
                <h4 className="font-medium text-neutral-300">Analysis</h4>
                <p className="text-sm text-neutral-400 whitespace-pre-wrap">
                  {selectedContract.analysis || 'No analysis available'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
