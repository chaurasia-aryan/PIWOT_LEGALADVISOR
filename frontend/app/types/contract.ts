export interface Contract {
  clientName: string;
  documentName: string;
  signedOn: Date;
  expiryOn: Date;
  email: string;
  analysis?: string;
}

export interface ContractTableProps {
  contracts: Contract[];
  isLoading: boolean;
  error?: string;
} 