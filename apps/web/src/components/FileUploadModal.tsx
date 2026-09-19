"use client";

import React, { useState, useRef } from "react";
import { X, UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import { uploadDataset } from "@/lib/api";
import { FileUploadResponse } from "@/lib/types";

interface FileUploadModalProps {
  isOpen: boolean;
  sessionId: string;
  onClose: () => void;
  onUploadSuccess: (result: FileUploadResponse) => void;
}

export const FileUploadModal: React.FC<FileUploadModalProps> = ({
  isOpen,
  sessionId,
  onClose,
  onUploadSuccess,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    const file = files[0];
    setError(null);
    setIsUploading(true);

    try {
      const response = await uploadDataset(sessionId, file);
      onUploadSuccess(response);
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to upload and ingest file.");
    } finally {
      setIsUploading(false);
    }
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => {
    setIsDragging(false);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4">
      <div className="w-full max-w-lg bg-studio-surface border border-studio-border rounded-lg shadow-2xl overflow-hidden font-mono">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-studio-border bg-studio-card">
          <div className="flex items-center space-x-2 text-sm text-studio-highlight font-bold">
            <UploadCloud className="w-4 h-4 text-studio-amber" />
            <span>INGEST NEW DATASET</span>
          </div>
          <button
            onClick={onClose}
            disabled={isUploading}
            className="text-studio-muted hover:text-studio-highlight transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-4">
          <div
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-lg p-8 flex flex-col items-center justify-center text-center cursor-pointer transition ${
              isDragging
                ? "border-studio-amber bg-studio-amber/5"
                : "border-studio-border hover:border-studio-muted bg-studio-bg"
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.tsv,.parquet,.xlsx,.xls,.json,.jsonl,.db,.sqlite,.sqlite3"
              className="hidden"
              onChange={(e) => handleFiles(e.target.files)}
              disabled={isUploading}
            />

            {isUploading ? (
              <div className="flex flex-col items-center space-y-3">
                <Loader2 className="w-8 h-8 text-studio-amber animate-spin" />
                <div className="text-xs text-studio-highlight">
                  PROFILING SCHEMA & HYDRATING SANDBOX...
                </div>
                <div className="text-[11px] text-studio-muted">
                  Extracting dimensions, types, null percentages & statistics
                </div>
              </div>
            ) : (
              <>
                <FileText className="w-10 h-10 text-studio-muted mb-3" />
                <p className="text-xs text-studio-highlight font-bold mb-1">
                  Drag and drop your file here, or click to browse
                </p>
                <p className="text-[11px] text-studio-muted mb-3">
                  CSV, TSV, Parquet, Excel (.xlsx), JSON, or SQLite (.db)
                </p>
                <div className="flex items-center space-x-2 text-[10px] text-studio-muted/80 bg-studio-card px-2.5 py-1 rounded border border-studio-border">
                  <span>⚡ Zero-copy transfer to isolated Python sandbox</span>
                </div>
              </>
            )}
          </div>

          {error && (
            <div className="flex items-start space-x-2 text-xs text-studio-crimson bg-studio-crimson/10 border border-studio-crimson/20 p-3 rounded">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <div className="text-[11px] text-studio-muted space-y-1">
            <div className="font-bold text-studio-highlight">Supported Formats:</div>
            <div>• Tabular Delimited: CSV (auto-delimiter & encoding), TSV</div>
            <div>• Columnar & Spreadsheet: Apache Parquet, Microsoft Excel (.xlsx)</div>
            <div>• Relational & Structured: SQLite databases, JSON/NDJSON records</div>
          </div>
        </div>
      </div>
    </div>
  );
};
