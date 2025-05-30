'use client';

import { useState, useEffect } from 'react';
import { FileUploader } from "@/components/FileUpload";
import Button from "@/components/Button";
import { ContractTable } from "@/components/ContractTable";
import { Contract } from "../types/contract";
import { analyzeContract } from "../Services/api";

export default function Dashboard() {
	const [contracts, setContracts] = useState<Contract[]>([]);
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState<string | undefined>();

	// For demo purposes, using sample data
	useEffect(() => {
		const sampleContracts: Contract[] = [
			{
				clientName: "Tech Corp",
				documentName: "Service Agreement",
				signedOn: new Date("2024-01-01"),
				expiryOn: new Date("2024-12-31"),
				email: "contact@techcorp.com"
			}
		];
		setContracts(sampleContracts);
	}, []);

	const handleFileUpload = async (file: File) => {
		setIsLoading(true);
		setError(undefined);
		
		try {
			const result = await analyzeContract(file, "Please analyze this contract");
			
			// Create a new contract entry with the analysis
			const newContract: Contract = {
				clientName: "New Client",
				documentName: file.name,
				signedOn: new Date(),
				expiryOn: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1 year from now
				email: "pending@example.com",
				analysis: result.response
			};

			setContracts(prev => [...prev, newContract]);
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to analyze contract');
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div className="min-h-screen w-full bg-neutral-900 p-4 space-y-6">
			<div className="flex justify-between items-center mb-6">
				<h1 className="text-2xl font-bold text-white">Contract Dashboard</h1>
				<Button buttonText="Add Contract" path="/AddContract" />
			</div>

			<div className="bg-neutral-800 p-6 rounded-lg shadow-lg">
				<h2 className="text-xl text-white mb-4">Upload New Contract</h2>
				<FileUploader onFileUpload={handleFileUpload} />
			</div>

			<ContractTable
				contracts={contracts}
				isLoading={isLoading}
				error={error}
			/>
		</div>
	);
}
