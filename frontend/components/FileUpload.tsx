"use client";
import React, { useState, useCallback } from "react";
import { useDropzone, FileRejection } from 'react-dropzone';

interface FileUploadProps {
  onFileUpload?: (file: File) => Promise<void>;
}

export const FileUploader = ({ onFileUpload }: FileUploadProps) => {
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');

  const onDrop = useCallback(async (acceptedFiles: File[], fileRejections: FileRejection[]) => {
    const file = acceptedFiles[0] || (fileRejections && fileRejections.length > 0 ? fileRejections[0].file : null);
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf') && !file.type.includes('pdf')) {
      console.warn('Please upload a PDF file');
      return;
    }

    setUploadStatus('uploading');
    try {
      if (onFileUpload) {
        await onFileUpload(file);
      }
      setUploadStatus('success');
      setTimeout(() => setUploadStatus('idle'), 3000);
    } catch (err) {
      console.error('File upload error:', err);
      setUploadStatus('error');
      setTimeout(() => setUploadStatus('idle'), 3000);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false
  });

  const getBorderColor = () => {
    if (uploadStatus === 'uploading') return 'border-ink bg-surface-secondary-hover';
    if (uploadStatus === 'success') return 'border-accent-olive bg-surface-secondary';
    if (uploadStatus === 'error') return 'border-accent-clay bg-surface-secondary';
    return isDragActive ? 'border-ink bg-surface-secondary-hover' : 'border-hairline hover:border-text-muted bg-surface-secondary';
  };

  const getStatusMessage = () => {
    switch (uploadStatus) {
      case 'uploading':
        return 'Processing multi-page contract on local CPU...';
      case 'success':
        return 'Contract analysis complete!';
      case 'error':
        return 'Analysis encountered an error. Please try again.';
      default:
        return isDragActive
          ? 'Drop PDF contract here'
          : 'Drag & drop your PDF contract here, or click to browse';
    }
  };

  return (
    <div
      {...getRootProps()}
      className={`w-full p-10 border border-dashed rounded-md cursor-pointer transition-all duration-150 text-center ${getBorderColor()}`}
    >
      <input {...getInputProps()} />
      <div className="space-y-2">
        <div className="text-2xl">📄</div>
        <p className="font-sans font-medium text-ink text-base">
          {getStatusMessage()}
        </p>
        <p className="font-mono text-xs uppercase tracking-wider text-text-muted">
          Supported Format: .PDF • Multi-Page Ingestion with OCR
        </p>
      </div>
    </div>
  );
};
