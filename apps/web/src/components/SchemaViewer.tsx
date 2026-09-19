"use client";

import React, { useState } from "react";
import { Table, Database, Layers, Hash, HardDrive, AlertCircle } from "lucide-react";
import { DataFrameProfile } from "@/lib/types";

interface SchemaViewerProps {
  profiles: DataFrameProfile[];
  activeVersion: string;
}

export const SchemaViewer: React.FC<SchemaViewerProps> = ({
  profiles,
  activeVersion,
}) => {
  const [selectedTableIndex, setSelectedTableIndex] = useState(0);

  if (!profiles || profiles.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center text-studio-muted font-mono space-y-3">
        <Database className="w-10 h-10 text-studio-muted/50" />
        <div className="text-sm font-bold text-studio-highlight">No Datasets Ingested</div>
        <p className="text-xs max-w-sm">
          Use the <strong>INGEST DATA</strong> button in the top navigation bar to upload CSV,
          Parquet, Excel, JSON, or SQLite datasets.
        </p>
      </div>
    );
  }

  const currentProfile = profiles[selectedTableIndex] || profiles[0];

  return (
    <div className="flex flex-col h-full bg-studio-bg font-mono text-xs overflow-hidden select-text">
      {/* Table Selector Tabs (if multi-table/multi-file) */}
      {profiles.length > 1 && (
        <div className="flex items-center space-x-1 px-4 py-2 border-b border-studio-border bg-studio-surface shrink-0 overflow-x-auto">
          {profiles.map((p, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedTableIndex(idx)}
              className={`px-3 py-1 rounded text-xs transition whitespace-nowrap ${
                selectedTableIndex === idx
                  ? "bg-studio-card border border-studio-amber text-studio-amber"
                  : "text-studio-muted hover:text-studio-highlight"
              }`}
            >
              {p.table_name}
            </button>
          ))}
        </div>
      )}

      {/* Dataset Summary Cards */}
      <div className="grid grid-cols-4 gap-3 p-4 border-b border-studio-border bg-studio-surface/50 shrink-0">
        <div className="p-3 bg-studio-card border border-studio-border rounded">
          <div className="flex items-center space-x-1.5 text-studio-muted text-[10px] uppercase mb-1">
            <Layers className="w-3 h-3 text-studio-amber" />
            <span>Table Identifier</span>
          </div>
          <div className="text-sm font-bold text-studio-highlight truncate">
            {currentProfile.table_name}
          </div>
          <div className="text-[10px] text-studio-cyan mt-0.5">
            Aliased in sandbox as `df`
          </div>
        </div>

        <div className="p-3 bg-studio-card border border-studio-border rounded">
          <div className="flex items-center space-x-1.5 text-studio-muted text-[10px] uppercase mb-1">
            <Hash className="w-3 h-3 text-studio-emerald" />
            <span>Total Rows</span>
          </div>
          <div className="text-sm font-bold text-studio-highlight">
            {currentProfile.row_count.toLocaleString()}
          </div>
          <div className="text-[10px] text-studio-muted mt-0.5">
            Active version: {activeVersion}
          </div>
        </div>

        <div className="p-3 bg-studio-card border border-studio-border rounded">
          <div className="flex items-center space-x-1.5 text-studio-muted text-[10px] uppercase mb-1">
            <Table className="w-3 h-3 text-studio-cyan" />
            <span>Columns Count</span>
          </div>
          <div className="text-sm font-bold text-studio-highlight">
            {currentProfile.column_count}
          </div>
          <div className="text-[10px] text-studio-muted mt-0.5">
            {currentProfile.columns.filter((c) => c.dtype.toLowerCase().includes("int") || c.dtype.toLowerCase().includes("float")).length} numerical
          </div>
        </div>

        <div className="p-3 bg-studio-card border border-studio-border rounded">
          <div className="flex items-center space-x-1.5 text-studio-muted text-[10px] uppercase mb-1">
            <HardDrive className="w-3 h-3 text-studio-amber" />
            <span>Memory Footprint</span>
          </div>
          <div className="text-sm font-bold text-studio-highlight">
            {currentProfile.memory_footprint_mb} MB
          </div>
          <div className="text-[10px] text-studio-emerald mt-0.5">
            In-Memory Arrow/Pandas
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Column Schema Specification */}
        <div>
          <div className="text-xs font-bold text-studio-highlight uppercase tracking-wider mb-2 flex items-center space-x-2">
            <span>Columns Schema & Distribution</span>
            <span className="text-[10px] text-studio-muted">
              ({currentProfile.columns.length} columns)
            </span>
          </div>

          <div className="border border-studio-border rounded overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead className="bg-studio-card text-[10px] uppercase text-studio-muted border-b border-studio-border select-none">
                <tr>
                  <th className="px-3 py-2">Column Name</th>
                  <th className="px-3 py-2">Data Type</th>
                  <th className="px-3 py-2">Missingness</th>
                  <th className="px-3 py-2">Cardinality</th>
                  <th className="px-3 py-2">Sample Values</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-studio-border/50">
                {currentProfile.columns.map((col, idx) => (
                  <tr
                    key={idx}
                    className="hover:bg-studio-card/50 transition font-mono"
                  >
                    <td className="px-3 py-2 text-studio-highlight font-bold">
                      {col.name}
                    </td>
                    <td className="px-3 py-2">
                      <span className="px-1.5 py-0.5 rounded text-[10px] bg-studio-card border border-studio-border text-studio-cyan">
                        {col.dtype}
                      </span>
                    </td>
                    <td className="px-3 py-2">
                      <div className="flex items-center space-x-2">
                        <div className="w-16 h-1.5 bg-studio-card rounded-full overflow-hidden">
                          <div
                            className={`h-full ${
                              col.null_percentage > 0 ? "bg-studio-amber" : "bg-studio-emerald"
                            }`}
                            style={{ width: `${Math.min(col.null_percentage, 100)}%` }}
                          />
                        </div>
                        <span className="text-[10px] text-studio-muted">
                          {col.null_percentage}%
                        </span>
                      </div>
                    </td>
                    <td className="px-3 py-2 text-studio-muted">
                      {col.cardinality.toLocaleString()}
                    </td>
                    <td className="px-3 py-2 text-studio-muted text-[11px] truncate max-w-xs">
                      {col.sample_values.map((v, i) => (
                        <span
                          key={i}
                          className="inline-block mr-1 px-1.5 py-0.2 rounded bg-studio-card text-studio-text border border-studio-border/50 text-[10px]"
                        >
                          {String(v)}
                        </span>
                      ))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 5-Row Markdown Head Preview */}
        <div>
          <div className="text-xs font-bold text-studio-highlight uppercase tracking-wider mb-2 flex items-center space-x-2">
            <span>First 5 Rows Preview</span>
            <span className="text-[10px] text-studio-emerald">
              (Live Dataset Snapshot)
            </span>
          </div>

          <div className="border border-studio-border rounded bg-studio-surface p-3 overflow-x-auto">
            <pre className="text-[11px] font-mono text-studio-text whitespace-pre leading-relaxed">
              {currentProfile.head_preview_markdown}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};
