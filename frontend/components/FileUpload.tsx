"use client";
import React, { useState, useCallback } from "react";
import { useDropzone } from 'react-dropzone';

interface FileUploaderProps {
  onFileUpload: (file: File) => Promise<void>;
}

export const FileUploader = ({ onFileUpload }: FileUploaderProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    if (!file.type.includes('pdf')) {
      alert('Please upload a PDF file');
      return;
    }

    setUploadStatus('uploading');
    try {
      await onFileUpload(file);
      setUploadStatus('success');
      setTimeout(() => setUploadStatus('idle'), 3000);
    } catch (error) {
      setUploadStatus('error');
      setTimeout(() => setUploadStatus('idle'), 3000);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  });

  const getStatusColor = () => {
    switch (uploadStatus) {
      case 'uploading':
        return 'border-yellow-500';
      case 'success':
        return 'border-green-500';
      case 'error':
        return 'border-red-500';
      default:
        return isDragging ? 'border-blue-500' : 'border-gray-600';
    }
  };

  const getStatusMessage = () => {
    switch (uploadStatus) {
      case 'uploading':
        return 'Uploading...';
      case 'success':
        return 'Upload successful!';
      case 'error':
        return 'Upload failed. Please try again.';
      default:
        return 'Drag and drop a PDF file here, or click to select';
    }
  };

  return (
    <div
      {...getRootProps()}
      className={`w-full p-8 border-2 border-dashed rounded-lg cursor-pointer transition-colors duration-200 ${getStatusColor()} hover:border-blue-400`}
      onDragEnter={() => setIsDragging(true)}
      onDragLeave={() => setIsDragging(false)}
    >
      <input {...getInputProps()} />
      <div className="text-center">
        <p className="text-white mb-2">{getStatusMessage()}</p>
        <p className="text-sm text-gray-400">Supported format: PDF</p>
      </div>
    </div>
  );
};
