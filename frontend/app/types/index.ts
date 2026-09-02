export interface RiskReason {
  type: string;
  severity: 'Low' | 'Medium' | 'High';
  weight: number;
  title: string;
  description: string;
  evidence: string;
  page: number;
}

export interface InconsistencyIssue {
  type: string;
  severity: 'Low' | 'Medium' | 'High';
  weight: number;
  title: string;
  description: string;
  evidence: string;
  page: number;
}

export interface RiskReport {
  score: number;
  level: 'Low' | 'Medium' | 'High';
  total_risk_factors: number;
  reasons: RiskReason[];
  inconsistencies: InconsistencyIssue[];
}

export interface SimilarStandardClause {
  category: string;
  title: string;
  reference_text: string;
  standard_type: string;
  similarity_score: number;
}

export interface ClauseChunk {
  chunk_id: string;
  page_start: number;
  page_end: number;
  section: string;
  category: string;
  confidence: number;
  risk_level: 'Low' | 'Medium' | 'High';
  text: string;
  char_count: number;
  similar_standard_clauses?: SimilarStandardClause[];
}

export interface ContractParty {
  name: string;
  role: string;
}

export interface ExtractedEntities {
  parties: ContractParty[];
  effective_date: string | null;
  expiry_date: string | null;
  notice_period: string | null;
  monetary_amounts: string[];
  percentages: string[];
  payment_terms: string[];
  governing_jurisdiction: string | null;
  all_jurisdictions: string[];
  dispute_venues: string[];
}

export interface ExtractiveSummary {
  summary_sentences: string[];
  source_pages: number[];
  method: string;
}

export interface DocumentMetadata {
  document_id: string;
  filename: string;
  page_count: number;
  char_count: number;
  chunk_count: number;
  ocr_used: boolean;
}

export interface MLContractAnalysis {
  document: DocumentMetadata;
  summary: ExtractiveSummary;
  risk: RiskReport;
  clauses: ClauseChunk[];
  entities: ExtractedEntities;
  inconsistencies: InconsistencyIssue[];
  metadata: {
    classifier_backend: string;
    latency_ms: number;
    disclaimer: string;
  };
  response?: string;
}

export interface Contract {
  id: string;
  clientName: string;
  documentName: string;
  signedOn: Date;
  expiryOn: Date;
  email: string;
  status: 'active' | 'expired' | 'pending';
  analysis?: string;
  mlAnalysis?: MLContractAnalysis;
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