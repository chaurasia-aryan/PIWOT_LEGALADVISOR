'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { analyzeContract } from '@/app/services/api';

interface FileUploaderProps {
  onUploadSuccess?: (file: File, analysis: string) => void;
  onUploadError?: (error: Error) => void;
}

export const FileUploader = ({ onUploadSuccess, onUploadError }: FileUploaderProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    if (!file.type.includes('pdf')) {
      setErrorMessage('Please upload a PDF file');
      setUploadStatus('error');
      setTimeout(() => {
        setUploadStatus('idle');
        setErrorMessage('');
      }, 3000);
      return;
    }

    setUploadStatus('uploading');
    setErrorMessage('');

    try {
      const result = await analyzeContract(file, 'Analyze this contract');
      setUploadStatus('success');
      onUploadSuccess?.(file, result.response);
      setTimeout(() => setUploadStatus('idle'), 3000);
    } catch (error) {
      setUploadStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'Upload failed');
      onUploadError?.(error instanceof Error ? error : new Error('Upload failed'));
      setTimeout(() => {
        setUploadStatus('idle');
        setErrorMessage('');
      }, 3000);
    }
  }, [onUploadSuccess, onUploadError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  });

  const getStatusColor = () => {
    switch (uploadStatus) {
      case 'uploading':
        return 'border-yellow-500 bg-yellow-500/10';
      case 'success':
        return 'border-green-500 bg-green-500/10';
      case 'error':
        return 'border-red-500 bg-red-500/10';
      default:
        return isDragActive ? 'border-blue-500 bg-blue-500/10' : 'border-neutral-600';
    }
  };

  const getStatusMessage = () => {
    if (errorMessage) return errorMessage;
    
    switch (uploadStatus) {
      case 'uploading':
        return 'Analyzing...';
      case 'success':
        return 'Analysis complete!';
      case 'error':
        return 'Analysis failed. Please try again.';
      default:
        return isDragActive 
          ? 'Drop your PDF file here'
          : 'Drag and drop a PDF file here, or click to select';
    }
  };

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`w-full p-8 border-2 border-dashed rounded-lg cursor-pointer transition-all duration-200 ${getStatusColor()} hover:border-blue-400 hover:bg-blue-500/5`}
        onDragEnter={() => setIsDragging(true)}
        onDragLeave={() => setIsDragging(false)}
      >
        <input {...getInputProps()} />
        <div className="text-center">
          <p className="text-lg font-medium mb-2">{getStatusMessage()}</p>
          <p className="text-sm text-neutral-400">Supported format: PDF</p>
        </div>
      </div>
    </div>
  );
}; 