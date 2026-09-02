'use client';

import { useState } from 'react';
import { Contract } from '@/app/types';

interface ContractTableProps {
  contracts: Contract[];
  isLoading: boolean;
  error?: string;
  onViewAnalysis: (contract: Contract) => void;
}

export const ContractTable = ({ contracts, isLoading, error, onViewAnalysis }: ContractTableProps) => {
  const [sortField, setSortField] = useState<keyof Contract>('signedOn');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [searchTerm, setSearchTerm] = useState('');

  const handleSort = (field: keyof Contract) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const filteredContracts = contracts.filter(contract => 
    (contract.clientName || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (contract.documentName || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (contract.email || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedContracts = [...filteredContracts].sort((a, b) => {
    const aValue = a[sortField];
    const bValue = b[sortField];

    if (aValue instanceof Date && bValue instanceof Date) {
      return sortDirection === 'asc' 
        ? aValue.getTime() - bValue.getTime()
        : bValue.getTime() - aValue.getTime();
    }

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortDirection === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    }

    return 0;
  });

  if (error) {
    return (
      <div className="w-full text-center p-4 text-accent-clay bg-accent-coral/30 border border-accent-clay/40 rounded-sm font-sans text-sm">
        Error: {error}
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="w-full text-center p-12 bg-surface-secondary border border-surface-warm rounded-md space-y-3">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-ink mx-auto"></div>
        <p className="font-sans font-medium text-ink text-base">Processing Contract with Local ML Pipeline...</p>
        <p className="font-mono text-xs uppercase tracking-wider text-text-muted">Multi-page OCR • SentenceTransformer • Risk Scorer</p>
      </div>
    );
  }

  return (
    <div className="w-full space-y-4">
      
      {/* Table Header & Search */}
      <div className="flex justify-between items-center flex-wrap gap-4 pb-2 border-b border-hairline">
        <div>
          <h2 className="font-serif text-2xl text-ink font-normal">Analyzed Contracts</h2>
          <p className="font-sans text-xs text-text-muted">Repository of parsed and risk-evaluated commercial agreements</p>
        </div>
        <div className="relative">
          <input
            type="text"
            placeholder="Search by party or document..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field w-72"
          />
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-md border border-hairline bg-canvas">
        <table className="min-w-full divide-y divide-hairline">
          <thead className="bg-surface-secondary">
            <tr>
              {[
                { label: 'Contracting Parties', field: 'clientName' as keyof Contract },
                { label: 'Document Name', field: 'documentName' as keyof Contract },
                { label: 'Effective Date', field: 'signedOn' as keyof Contract },
                { label: 'Valid Until', field: 'expiryOn' as keyof Contract },
                { label: 'Risk Assessment', field: 'status' as keyof Contract },
                { label: 'Actions', field: null },
              ].map(({ label, field }) => (
                <th
                  key={label}
                  onClick={() => field && handleSort(field)}
                  className={`px-6 py-3.5 text-left font-mono text-xs uppercase tracking-wider text-text-muted ${field ? 'cursor-pointer hover:text-ink select-none' : ''}`}
                >
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-canvas divide-y divide-hairline font-sans">
            {sortedContracts.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-12 text-text-muted text-sm font-serif">
                  No contracts uploaded yet. Upload a PDF agreement above to run local ML analysis.
                </td>
              </tr>
            ) : (
              sortedContracts.map((contract, idx) => (
                <tr key={contract.id || idx} className="hover:bg-surface-secondary/70 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-ink">
                    {contract.clientName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-serif text-ink">
                    {contract.documentName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap font-mono text-xs text-text-muted">
                    {new Date(contract.signedOn).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap font-mono text-xs text-text-muted">
                    {new Date(contract.expiryOn).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {contract.mlAnalysis?.risk ? (
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-sm font-mono text-xs uppercase tracking-wide ${
                        contract.mlAnalysis.risk.level === 'High'
                          ? 'bg-accent-coral/60 text-accent-deep border border-accent-clay/40'
                          : contract.mlAnalysis.risk.level === 'Medium'
                          ? 'bg-surface-manilla/70 text-ink border border-surface-kraft/40'
                          : 'bg-accent-cactus/40 text-[#3e5e54] border border-accent-cactus/70'
                      }`}>
                        {contract.mlAnalysis.risk.level} ({contract.mlAnalysis.risk.score}/100)
                      </span>
                    ) : (
                      <span className="font-mono text-xs text-text-muted uppercase px-2 py-0.5 rounded bg-surface-secondary">
                        {contract.status}
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button
                      onClick={() => onViewAnalysis(contract)}
                      className="inline-flex items-center bg-ink text-canvas hover:opacity-90 font-sans text-xs font-medium px-3.5 py-1.5 rounded-sm transition"
                    >
                      View Analysis
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};