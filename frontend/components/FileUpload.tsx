"use client";
import React, { useState } from "react";
import { FileUpload } from "@/ui/file-upload";

export function FileUploader() {
  const [files, setFiles] = useState<File[]>([]);
  
  const handleFileUpload = (files: File[]) => {
    setFiles(files);
    
  };

  return (
    <div className="  flex items-center justify-center bg-neutral-100 dark:bg-neutral-900">
      <div className=" max-w-4xl mx-auto min-h-96 border-2 border-dashed border-neutral-300 dark:border-neutral-700 bg-white dark:bg-black rounded-lg flex flex-col items-center justify-center p-6 space-y-4 w-md">
        <h2 className="text-xl font-semibold text-neutral-700 dark:text-neutral-300">
          Upload Your Files
        </h2>
        <p className="text-sm text-neutral-500 dark:text-neutral-400">
          Drag and drop files here, or click to browse.
        </p>
        <div className="w-full flex justify-center">
          <FileUpload
            onChange={handleFileUpload}
          />
        </div>
        {files.length > 0 && (
          <div className="mt-4 w-full">
            <h3 className="text-lg font-medium text-neutral-700 dark:text-neutral-300">
              Uploaded Files
            </h3>
            <ul className="mt-2 space-y-2">
              {files.map((file, index) => (
                <li
                  key={index}
                  className="text-sm text-neutral-700 dark:text-neutral-400 bg-neutral-100 dark:bg-neutral-800 rounded-lg px-4 py-2"
                >
                  {file.name}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
