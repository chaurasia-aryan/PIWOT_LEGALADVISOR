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
    contract.clientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    contract.documentName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    contract.email.toLowerCase().includes(searchTerm.toLowerCase())
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
      <div className="w-full text-center p-4 text-red-500 bg-red-500/10 rounded-lg">
        Error: {error}
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="w-full text-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-4 text-neutral-400">Loading contracts...</p>
      </div>
    );
  }

  return (
    <div className="w-full space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Contracts</h2>
        <input
          type="text"
          placeholder="Search contracts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input-field w-64"
        />
      </div>

      <div className="overflow-x-auto rounded-lg border border-neutral-700">
        <table className="min-w-full divide-y divide-neutral-700">
          <thead className="bg-neutral-800">
            <tr>
              {['Client Name', 'Document', 'Signed On', 'Valid Till', 'Email', 'Status', 'Actions'].map((header) => (
                <th
                  key={header}
                  className="px-6 py-3 text-left text-xs font-medium text-neutral-300 uppercase tracking-wider cursor-pointer hover:bg-neutral-700"
                  onClick={() => {
                    const field = header.toLowerCase().replace(/\s+/g, '') as keyof Contract;
                    if (field in contracts[0] || field === 'status') {
                      handleSort(field);
                    }
                  }}
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-neutral-900 divide-y divide-neutral-700">
            {sortedContracts.map((contract) => (
              <tr key={contract.id} className="hover:bg-neutral-800 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">{contract.clientName}</td>
                <td className="px-6 py-4 whitespace-nowrap">{contract.documentName}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {new Date(contract.signedOn).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {new Date(contract.expiryOn).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">{contract.email}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium
                    ${contract.status === 'active' ? 'bg-green-500/20 text-green-400' : ''}
                    ${contract.status === 'expired' ? 'bg-red-500/20 text-red-400' : ''}
                    ${contract.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' : ''}
                  `}>
                    {contract.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <button
                    onClick={() => onViewAnalysis(contract)}
                    className="btn-primary text-sm"
                  >
                    View Analysis
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}; 