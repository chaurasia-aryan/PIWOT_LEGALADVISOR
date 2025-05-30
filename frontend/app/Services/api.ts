import axios from 'axios';
import { ContractAnalysis } from '../types';

const API_BASE_URL = 'http://localhost:5000';

export const analyzeContract = async (file: File, inputText: string): Promise<ContractAnalysis> => {
  try {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('input_text', inputText);

    const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.message || 'Failed to analyze contract');
    }
    throw new Error('Failed to analyze contract');
  }
};

export const getContracts = async (): Promise<Contract[]> => {
  try {
    const response = await api.get<Contract[]>('/contracts');
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.message || 'Failed to fetch contracts');
    }
    throw new Error('Failed to fetch contracts');
  }
};

export const uploadContract = async (file: File): Promise<FileUploadResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<FileUploadResponse>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.message || 'Failed to upload contract');
    }
    throw new Error('Failed to upload contract');
  }
}; 