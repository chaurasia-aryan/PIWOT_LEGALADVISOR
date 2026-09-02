'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { analyzeContract } from '@/app/Services/api';

interface FileUploaderProps {
  onUploadSuccess?: (file: File, analysis: string) => void;
  onUploadError?: (error: Error) => void;
}

export const FileUploader = ({ onUploadSuccess, onUploadError }: FileUploaderProps) => {
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    if (!file.name.toLowerCase().endsWith('.pdf') && !file.type.includes('pdf')) {
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
      onUploadSuccess?.(file, result.response || result.summary?.summary_sentences?.join(" ") || "Analysis completed.");
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

  const getBorderColor = () => {
    if (uploadStatus === 'uploading') return 'border-ink bg-surface-secondary-hover';
    if (uploadStatus === 'success') return 'border-accent-olive bg-surface-secondary';
    if (uploadStatus === 'error') return 'border-accent-clay bg-surface-secondary';
    return isDragActive ? 'border-ink bg-surface-secondary-hover' : 'border-hairline hover:border-text-muted bg-surface-secondary';
  };

  const getStatusMessage = () => {
    if (errorMessage) return errorMessage;
    
    switch (uploadStatus) {
      case 'uploading':
        return 'Processing multi-page contract on local CPU...';
      case 'success':
        return 'Contract analysis complete!';
      case 'error':
        return 'Analysis failed. Please try again.';
      default:
        return isDragActive 
          ? 'Drop your PDF file here'
          : 'Drag & drop your PDF file here, or click to browse';
    }
  };

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`w-full p-10 border border-dashed rounded-md cursor-pointer transition-all duration-150 text-center ${getBorderColor()}`}
      >
        <input {...getInputProps()} />
        <div className="space-y-2">
          <div className="text-2xl">📄</div>
          <p className="font-sans font-medium text-ink text-base">{getStatusMessage()}</p>
          <p className="font-mono text-xs uppercase tracking-wider text-text-muted">Supported format: PDF • Local ML Pipeline</p>
        </div>
      </div>
    </div>
  );
};