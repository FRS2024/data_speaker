import React, { useState, useRef } from "react";
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
      setError(err.message || "Failed to upload and profile dataset.");
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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-surface-container-lowest/80 backdrop-blur-md"
        onClick={onClose}
      />

      {/* Modal Surface */}
      <div className="relative z-10 w-full max-w-lg bg-surface-container-low text-on-surface rounded-2xl shadow-2xl overflow-hidden border border-outline-variant/30 animate-in fade-in zoom-in-95 duration-200">
        <div className="h-0.5 w-full bg-gradient-to-r from-transparent via-primary-container/70 to-transparent" />

        {/* Header */}
        <div className="p-space-md bg-surface-container-low flex items-center justify-between border-b border-outline-variant/15">
          <div className="flex items-center gap-2 text-primary font-medium font-body-md">
            <span className="material-symbols-outlined text-[20px]">upload_file</span>
            <span>Ingest & Profile Tabular Dataset</span>
          </div>
          <button
            onClick={onClose}
            disabled={isUploading}
            className="w-8 h-8 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface transition-colors"
          >
            <span className="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>

        {/* Body */}
        <div className="p-space-lg space-y-space-md">
          <div
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all ${
              isDragging
                ? "border-primary bg-primary/5"
                : "border-outline-variant/40 hover:border-primary/50 bg-surface-container-lowest"
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
              <div className="flex flex-col items-center space-y-2">
                <span className="material-symbols-outlined text-[32px] text-primary animate-spin">
                  sync
                </span>
                <span className="text-body-md font-medium text-on-surface">
                  Profiling Schema & Hydrating Sandbox...
                </span>
                <span className="text-body-sm text-outline">
                  Extracting dimensions, types, null percentages & statistics
                </span>
              </div>
            ) : (
              <>
                <span className="material-symbols-outlined text-[36px] text-primary mb-2">
                  cloud_upload
                </span>
                <p className="text-body-md text-on-surface font-medium mb-1">
                  Drag & drop your dataset here, or click to browse
                </p>
                <p className="text-body-sm text-outline mb-3">
                  CSV, Parquet, Excel (.xlsx), TSV, JSON, SQLite (.db)
                </p>
                <div className="flex items-center gap-1.5 text-[11px] font-code-tabular text-tertiary bg-surface-container-high px-3 py-1 rounded-full border border-outline-variant/20">
                  <span className="material-symbols-outlined text-[14px]">bolt</span>
                  <span>Zero-copy transfer to isolated Python sandbox</span>
                </div>
              </>
            )}
          </div>

          {error && (
            <div className="flex items-start gap-2 text-body-sm text-error bg-error-container/20 border border-error/30 p-3 rounded-xl">
              <span className="material-symbols-outlined text-[18px] shrink-0 mt-0.5">error</span>
              <span>{error}</span>
            </div>
          )}

          <div className="text-[12px] text-on-surface-variant font-code-tabular space-y-1 bg-surface-container p-3 rounded-xl border border-outline-variant/15">
            <div className="font-semibold text-on-surface">Autonomous Ingestion Engine:</div>
            <div>• Auto-detects delimiter (comma, semicolon, tab, pipe) & encoding</div>
            <div>• Extracts privacy-safe profiles (min/max, cardinality, nulls)</div>
            <div>• Automatically initializes immutable baseline snapshot df_v0</div>
          </div>
        </div>
      </div>
    </div>
  );
};
