"use client";

import React from "react";
import { Database, Plus, RefreshCw, Upload, Terminal, ShieldCheck } from "lucide-react";

interface NavbarProps {
  sessionId: string;
  tableCount: number;
  onNewSession: () => void;
  onUploadClick: () => void;
  onResetSession: () => void;
  isResetting?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  sessionId,
  tableCount,
  onNewSession,
  onUploadClick,
  onResetSession,
  isResetting = false,
}) => {
  return (
    <header className="h-12 bg-studio-surface border-b border-studio-border px-4 flex items-center justify-between select-none shrink-0">
      {/* Brand & Studio Title */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2">
          <div className="w-2.5 h-2.5 rounded-full bg-studio-emerald animate-pulse" />
          <span className="font-mono text-sm font-bold tracking-wider text-studio-highlight">
            DATA_SPEAKER
          </span>
          <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-studio-card border border-studio-border text-studio-muted">
            STUDIO v1.0
          </span>
        </div>

        <div className="h-4 w-px bg-studio-border" />

        {/* Active Session Badge */}
        <div className="flex items-center space-x-1.5 font-mono text-xs text-studio-muted">
          <span>SESSION:</span>
          <span className="text-studio-cyan bg-studio-card px-2 py-0.5 rounded border border-studio-border">
            {sessionId || "INITIALIZING..."}
          </span>
        </div>
      </div>

      {/* Action Controls */}
      <div className="flex items-center space-x-2.5 font-mono text-xs">
        {/* Upload Dataset Button */}
        <button
          onClick={onUploadClick}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded bg-studio-amber/10 border border-studio-amber/30 text-studio-amber hover:bg-studio-amber/20 transition"
        >
          <Upload className="w-3.5 h-3.5" />
          <span>INGEST DATA</span>
          {tableCount > 0 && (
            <span className="ml-1 px-1.5 py-0.2 rounded-full bg-studio-amber/30 text-[10px]">
              {tableCount}
            </span>
          )}
        </button>

        {/* Reset Session Kernel */}
        <button
          onClick={onResetSession}
          disabled={isResetting || !sessionId}
          title="Clear variables and reset Python sandbox memory"
          className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded bg-studio-card border border-studio-border text-studio-muted hover:text-studio-highlight hover:border-studio-muted/50 transition disabled:opacity-40"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isResetting ? "animate-spin text-studio-amber" : ""}`} />
          <span>RESET KERNEL</span>
        </button>

        {/* New Session Button */}
        <button
          onClick={onNewSession}
          title="Create brand new analytical session"
          className="flex items-center space-x-1 px-2.5 py-1.5 rounded bg-studio-card border border-studio-border text-studio-muted hover:text-studio-highlight hover:border-studio-muted/50 transition"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>NEW</span>
        </button>

        <div className="h-4 w-px bg-studio-border" />

        {/* Sandbox Status Pill */}
        <div className="flex items-center space-x-1 text-studio-emerald text-[11px] bg-studio-emerald/10 border border-studio-emerald/20 px-2 py-1 rounded">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>SANDBOX ISOLATED</span>
        </div>
      </div>
    </header>
  );
};
