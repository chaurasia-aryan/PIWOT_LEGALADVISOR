export interface Contract {
  id: string;
  clientName: string;
  documentName: string;
  signedOn: Date;
  expiryOn: Date;
  email: string;
  analysis?: string;
  status: 'active' | 'expired' | 'pending';
}

export interface ContractAnalysis {
  response: string;
  metadata?: {
    expiryDate?: string;
    startDate?: string;
    parties?: string[];
    keyTerms?: string[];
  };
}

export interface FileUploadResponse {
  success: boolean;
  message: string;
  contract?: Contract;
}

export interface ApiError {
  message: string;
  code?: string;
} 