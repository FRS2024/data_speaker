"use client";

import React, { useEffect, useState } from "react";
import { Table, BarChart3, Code2, AlertCircle } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { ChatPanel } from "@/components/ChatPanel";
import { SchemaViewer } from "@/components/SchemaViewer";
import { PlotlyStudio } from "@/components/PlotlyStudio";
import { CodeConsole } from "@/components/CodeConsole";
import { FileUploadModal } from "@/components/FileUploadModal";
import { useChatStream } from "@/hooks/useChatStream";
import { createSession, fetchSchema, resetSession } from "@/lib/api";
import { DataFrameProfile, FileUploadResponse } from "@/lib/types";

export default function Home() {
  const [sessionId, setSessionId] = useState<string>("");
  const [profiles, setProfiles] = useState<DataFrameProfile[]>([]);
  const [activeVersion, setActiveVersion] = useState<string>("df_v0");
  const [activeTab, setActiveTab] = useState<"schema" | "charts" | "code">("schema");
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [isExecutingManual, setIsExecutingManual] = useState(false);

  const {
    messages,
    isStreaming,
    activeFigures,
    activeCode,
    activeStdout,
    sendMessage,
    setMessages,
  } = useChatStream();

  // 1. Initialize session on load
  useEffect(() => {
    async function init() {
      try {
        const sess = await createSession("Studio Workspace Session");
        setSessionId(sess.session_id);
      } catch (err) {
        console.error("Failed to initialize session:", err);
      }
    }
    init();
  }, []);

  // 2. Automatically switch to Charts tab when new figures are generated
  useEffect(() => {
    if (activeFigures.length > 0) {
      setActiveTab("charts");
    }
  }, [activeFigures.length]);

  // 3. Handle dataset upload success
  const handleUploadSuccess = (res: FileUploadResponse) => {
    if (res.profiles && res.profiles.length > 0) {
      setProfiles(res.profiles);
      setActiveTab("schema");
    }
  };

  // 4. Handle create new session
  const handleNewSession = async () => {
    try {
      const sess = await createSession("New Analytical Workspace");
      setSessionId(sess.session_id);
      setProfiles([]);
      setActiveVersion("df_v0");
      setMessages([]);
      setActiveTab("schema");
    } catch (err) {
      console.error("Failed to create new session:", err);
    }
  };

  // 5. Handle kernel reset
  const handleResetKernel = async () => {
    if (!sessionId) return;
    setIsResetting(true);
    try {
      await resetSession(sessionId);
      const schemaData = await fetchSchema(sessionId);
      setProfiles(schemaData.profiles || []);
      setActiveVersion(schemaData.active_version || "df_v0");
    } catch (err) {
      console.error("Failed to reset session kernel:", err);
    } finally {
      setIsResetting(false);
    }
  };

  // 6. Handle manual Python execution from Monaco editor
  const handleExecuteManual = async (customCode: string) => {
    if (!sessionId || isExecutingManual) return;
    setIsExecutingManual(true);
    try {
      const res = await fetch(`/api/v1/sessions/${sessionId}/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: customCode, timeout: 60 }),
      });
      const data = await res.json();
      if (data.figures && data.figures.length > 0) {
        setActiveTab("charts");
      }
    } catch (err) {
      console.error("Manual execution failed:", err);
    } finally {
      setIsExecutingManual(false);
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-studio-bg overflow-hidden font-sans text-studio-text">
      {/* Top Studio Navbar */}
      <Navbar
        sessionId={sessionId}
        tableCount={profiles.length}
        onNewSession={handleNewSession}
        onUploadClick={() => setIsUploadOpen(true)}
        onResetSession={handleResetKernel}
        isResetting={isResetting}
      />

      {/* Main Split-Pane Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column: Conversational AI Analyst (42% width) */}
        <div className="w-[42%] h-full flex flex-col shrink-0">
          <ChatPanel
            messages={messages}
            isStreaming={isStreaming}
            onSendMessage={(prompt) => sendMessage(sessionId, prompt)}
            onSelectCode={(code, stdout) => {
              setActiveTab("code");
            }}
            onSelectChartTab={() => setActiveTab("charts")}
          />
        </div>

        {/* Right Column: Tabbed Data Studio Workspace (58% width) */}
        <div className="flex-1 h-full flex flex-col overflow-hidden bg-studio-surface">
          {/* Workspace Tab Bar */}
          <div className="h-9 bg-studio-card/90 border-b border-studio-border px-3 flex items-center justify-between font-mono text-xs select-none shrink-0">
            <div className="flex items-center space-x-1">
              <button
                onClick={() => setActiveTab("schema")}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded transition ${
                  activeTab === "schema"
                    ? "bg-studio-surface border border-studio-border text-studio-amber font-bold"
                    : "text-studio-muted hover:text-studio-highlight"
                }`}
              >
                <Table className="w-3.5 h-3.5" />
                <span>DATASET SCHEMA</span>
                {profiles.length > 0 && (
                  <span className="text-[10px] px-1 rounded bg-studio-card">
                    {profiles.length}
                  </span>
                )}
              </button>

              <button
                onClick={() => setActiveTab("charts")}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded transition ${
                  activeTab === "charts"
                    ? "bg-studio-surface border border-studio-border text-studio-amber font-bold"
                    : "text-studio-muted hover:text-studio-highlight"
                }`}
              >
                <BarChart3 className="w-3.5 h-3.5" />
                <span>VISUALIZATIONS</span>
                {activeFigures.length > 0 && (
                  <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-studio-amber text-studio-bg font-bold">
                    {activeFigures.length}
                  </span>
                )}
              </button>

              <button
                onClick={() => setActiveTab("code")}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded transition ${
                  activeTab === "code"
                    ? "bg-studio-surface border border-studio-border text-studio-cyan font-bold"
                    : "text-studio-muted hover:text-studio-highlight"
                }`}
              >
                <Code2 className="w-3.5 h-3.5" />
                <span>PYTHON KERNEL & CONSOLE</span>
              </button>
            </div>

            <div className="text-[10px] text-studio-muted font-mono">
              IPYTHON KERNEL RUNNER • ZERO RAW DATA LEAKAGE
            </div>
          </div>

          {/* Tab Workspace Content */}
          <div className="flex-1 overflow-hidden">
            {activeTab === "schema" && (
              <SchemaViewer profiles={profiles} activeVersion={activeVersion} />
            )}
            {activeTab === "charts" && <PlotlyStudio figures={activeFigures} />}
            {activeTab === "code" && (
              <CodeConsole
                code={activeCode}
                stdout={activeStdout}
                onExecuteManual={handleExecuteManual}
                isExecuting={isExecutingManual}
              />
            )}
          </div>
        </div>
      </div>

      {/* Dataset File Upload Dropzone Modal */}
      <FileUploadModal
        isOpen={isUploadOpen}
        sessionId={sessionId}
        onClose={() => setIsUploadOpen(false)}
        onUploadSuccess={handleUploadSuccess}
      />
    </div>
  );
}
