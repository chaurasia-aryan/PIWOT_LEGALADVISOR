import axios from 'axios';
import { MLContractAnalysis } from '../types';

// Default to NEXT_PUBLIC_API_URL if specified, otherwise relative path for Vercel Serverless
const getBaseUrl = () => {
  if (typeof window !== 'undefined') {
    return process.env.NEXT_PUBLIC_API_URL || '';
  }
  return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
};

const apiClient = axios.create({
  baseURL: getBaseUrl(),
  timeout: 45000,
});

export const checkBackendHealth = async (): Promise<boolean> => {
  try {
    const res = await apiClient.get('/api/health');
    return res.status === 200 && res.data.status === 'healthy';
  } catch {
    // Fallback check to relative /api/health
    try {
      const fallbackRes = await axios.get('/api/health');
      return fallbackRes.status === 200 && fallbackRes.data.status === 'healthy';
    } catch {
      return false;
    }
  }
};

export const analyzeContract = async (
  file: File,
  inputText: string = 'Full multi-page contract review'
): Promise<MLContractAnalysis> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('resume', file); // legacy compatibility
  formData.append('input_text', inputText);

  try {
    // Primary attempt
    const response = await apiClient.post<MLContractAnalysis>('/api/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (primaryError) {
    // If primary failed (e.g. remote backend offline), fallback to local /api/analyze route
    try {
      const fallbackRes = await axios.post<MLContractAnalysis>('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return fallbackRes.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const errorMsg = error.response?.data?.error || error.response?.data?.message || error.message;
        throw new Error(errorMsg || 'Failed to analyze contract');
      }
      throw new Error(
        primaryError instanceof Error ? primaryError.message : 'An unexpected error occurred during contract analysis.'
      );
    }
  }
};