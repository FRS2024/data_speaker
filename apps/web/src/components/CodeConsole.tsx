"use client";

import React, { useState } from "react";
import Editor from "@monaco-editor/react";
import { Terminal, Copy, Check, Play, Clock, Code2 } from "lucide-react";

interface CodeConsoleProps {
  code: string;
  stdout: string;
  onExecuteManual?: (code: string) => void;
  isExecuting?: boolean;
}

export const CodeConsole: React.FC<CodeConsoleProps> = ({
  code,
  stdout,
  onExecuteManual,
  isExecuting = false,
}) => {
  const [currentCode, setCurrentCode] = useState(code);
  const [copied, setCopied] = useState(false);

  // Synchronize when active code prop changes
  React.useEffect(() => {
    setCurrentCode(code);
  }, [code]);

  const handleCopy = () => {
    if (!currentCode) return;
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleRun = () => {
    if (onExecuteManual && currentCode) {
      onExecuteManual(currentCode);
    }
  };

  return (
    <div className="flex flex-col h-full bg-studio-bg font-mono text-xs overflow-hidden">
      {/* Editor Toolbar */}
      <div className="h-10 bg-studio-surface border-b border-studio-border px-4 flex items-center justify-between shrink-0 select-none">
        <div className="flex items-center space-x-2">
          <Code2 className="w-4 h-4 text-studio-cyan" />
          <span className="text-xs font-bold text-studio-highlight">
            MONACO PYTHON KERNEL EDITOR
          </span>
          <span className="text-[10px] text-studio-muted px-1.5 py-0.5 rounded bg-studio-card border border-studio-border">
            PYTHON 3.12 • IPYTHON
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopy}
            disabled={!currentCode}
            className="flex items-center space-x-1 px-2.5 py-1 rounded bg-studio-card border border-studio-border text-studio-muted hover:text-studio-highlight transition disabled:opacity-40"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-studio-emerald" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "COPIED" : "COPY"}</span>
          </button>

          {onExecuteManual && (
            <button
              onClick={handleRun}
              disabled={isExecuting || !currentCode}
              className="flex items-center space-x-1.5 px-3 py-1 rounded bg-studio-emerald/20 border border-studio-emerald/40 text-studio-emerald hover:bg-studio-emerald/30 transition disabled:opacity-40"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>{isExecuting ? "RUNNING..." : "RUN IN SANDBOX"}</span>
            </button>
          )}
        </div>
      </div>

      {/* Monaco Editor Canvas */}
      <div className="flex-1 w-full relative">
        <Editor
          height="100%"
          language="python"
          theme="vs-dark"
          value={currentCode || "# No code executed in this session yet.\n# Ask the AI Analyst or write custom code here."}
          onChange={(val) => setCurrentCode(val || "")}
          options={{
            minimap: { enabled: false },
            fontSize: 12,
            fontFamily: "JetBrains Mono, monospace",
            lineNumbers: "on",
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            padding: { top: 12, bottom: 12 },
          }}
        />
      </div>

      {/* Bottom Terminal Output Console */}
      <div className="h-44 bg-studio-surface border-t border-studio-border flex flex-col shrink-0 select-text">
        <div className="h-7 bg-studio-card px-3 flex items-center justify-between text-[10px] text-studio-muted border-b border-studio-border select-none">
          <div className="flex items-center space-x-1.5">
            <Terminal className="w-3 h-3 text-studio-emerald" />
            <span className="font-bold text-studio-highlight">SANDBOX STDOUT LOGS</span>
          </div>
          <div className="flex items-center space-x-1 text-studio-emerald">
            <span>● CGroup Isolated</span>
          </div>
        </div>

        <div className="flex-1 p-3 overflow-y-auto font-mono text-[11px] leading-relaxed text-studio-text whitespace-pre-wrap">
          {stdout ? (
            <span>{stdout}</span>
          ) : (
            <span className="text-studio-muted italic">
              Ready. Sandbox output logs will stream here during execution.
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
