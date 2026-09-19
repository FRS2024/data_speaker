"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Terminal,
  ChevronDown,
  ChevronRight,
  AlertTriangle,
  CheckCircle2,
  Sparkles,
  BarChart3,
  Loader2,
} from "lucide-react";
import { ChatMessage } from "@/lib/types";

interface ChatPanelProps {
  messages: ChatMessage[];
  isStreaming: boolean;
  onSendMessage: (prompt: string) => void;
  onSelectCode: (code: string, stdout?: string) => void;
  onSelectChartTab: () => void;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({
  messages,
  isStreaming,
  onSendMessage,
  onSelectCode,
  onSelectChartTab,
}) => {
  const [input, setInput] = useState("");
  const [expandedCodeMap, setExpandedCodeMap] = useState<Record<string, boolean>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isStreaming]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    onSendMessage(input.trim());
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleCode = (msgId: string) => {
    setExpandedCodeMap((prev) => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const suggestionChips = [
    "Summarize dataset statistics",
    "Plot a distribution histogram",
    "Identify outliers & anomalies",
    "Calculate correlation matrix",
  ];

  return (
    <div className="flex flex-col h-full bg-studio-surface border-r border-studio-border select-text font-sans">
      {/* Pane Header */}
      <div className="h-9 bg-studio-card/80 border-b border-studio-border px-3 flex items-center justify-between font-mono text-xs text-studio-muted shrink-0">
        <div className="flex items-center space-x-2">
          <Bot className="w-3.5 h-3.5 text-studio-cyan" />
          <span className="font-bold text-studio-highlight">AI ANALYST THREAD</span>
        </div>
        <div className="text-[10px] text-studio-muted">
          {messages.length} TURNS RECORDED
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 font-mono text-xs">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 text-studio-muted space-y-3">
            <div className="p-3 rounded-full bg-studio-card border border-studio-border">
              <Sparkles className="w-6 h-6 text-studio-amber" />
            </div>
            <div className="font-bold text-sm text-studio-highlight">Autonomous Data Analyst Ready</div>
            <p className="text-xs max-w-sm">
              Upload a dataset above or ask questions. The analyst writes, tests, and executes
              Python code inside an isolated sandbox kernel.
            </p>
            <div className="flex flex-wrap gap-2 justify-center max-w-md mt-4">
              {suggestionChips.map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => onSendMessage(chip)}
                  className="px-2.5 py-1 rounded bg-studio-card border border-studio-border text-[11px] text-studio-cyan hover:border-studio-cyan/50 hover:bg-studio-cyan/5 transition"
                >
                  {chip}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${
                msg.role === "user" ? "items-end" : "items-start"
              }`}
            >
              {/* Role & Timestamp Label */}
              <div className="flex items-center space-x-1.5 text-[10px] text-studio-muted mb-1 px-1">
                {msg.role === "user" ? (
                  <>
                    <span>YOU</span>
                    <User className="w-3 h-3 text-studio-amber" />
                  </>
                ) : (
                  <>
                    <Bot className="w-3 h-3 text-studio-cyan" />
                    <span>ANALYST ENGINE</span>
                  </>
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[92%] rounded-lg p-3 border ${
                  msg.role === "user"
                    ? "bg-studio-amber/10 border-studio-amber/30 text-studio-highlight"
                    : "bg-studio-card border-studio-border text-studio-text w-full"
                }`}
              >
                {/* Assistant Execution Status Badges */}
                {msg.role === "assistant" && (
                  <div className="space-y-2 mb-2 pb-2 border-b border-studio-border/50">
                    {/* Status Pill */}
                    <div className="flex flex-wrap items-center gap-1.5">
                      {msg.status === "generating_code" && (
                        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-studio-amber/10 border border-studio-amber/30 text-studio-amber">
                          <Loader2 className="w-3 h-3 animate-spin" />
                          <span>SYNTHESIZING CODE</span>
                        </span>
                      )}
                      {msg.status === "running_sandbox" && (
                        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-studio-cyan/10 border border-studio-cyan/30 text-studio-cyan">
                          <Terminal className="w-3 h-3 animate-pulse" />
                          <span>EXECUTING IN SANDBOX</span>
                        </span>
                      )}
                      {msg.status === "synthesizing_insights" && (
                        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-studio-emerald/10 border border-studio-emerald/30 text-studio-emerald">
                          <Sparkles className="w-3 h-3 animate-pulse" />
                          <span>INTERPRETING RESULTS</span>
                        </span>
                      )}
                      {msg.status === "complete" && (
                        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-studio-emerald/10 border border-studio-emerald/30 text-studio-emerald">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>
                            VERIFIED IN {msg.durationMs ? `${msg.durationMs}ms` : "SANDBOX"}
                          </span>
                        </span>
                      )}
                      {msg.status === "error" && (
                        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-studio-crimson/10 border border-studio-crimson/30 text-studio-crimson">
                          <AlertTriangle className="w-3 h-3" />
                          <span>EXECUTION FAILED</span>
                        </span>
                      )}

                      {/* Reflexion Badges */}
                      {msg.reflexionSteps && msg.reflexionSteps.length > 0 && (
                        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-studio-crimson/20 border border-studio-crimson/40 text-studio-crimson font-bold">
                          <AlertTriangle className="w-3 h-3" />
                          <span>
                            REFLEXION: AUTO-CORRECTED ({msg.reflexionSteps.length} RETRY)
                          </span>
                        </span>
                      )}

                      {/* Charts Generated Badge */}
                      {msg.figures && msg.figures.length > 0 && (
                        <button
                          onClick={onSelectChartTab}
                          className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-studio-amber/20 border border-studio-amber/40 text-studio-amber hover:bg-studio-amber/30 transition"
                        >
                          <BarChart3 className="w-3 h-3" />
                          <span>{msg.figures.length} CHART(S) READY ↗</span>
                        </button>
                      )}
                    </div>

                    {/* Reflexion Error Details if any */}
                    {msg.reflexionSteps && msg.reflexionSteps.length > 0 && (
                      <div className="text-[10px] text-studio-crimson bg-studio-crimson/5 p-2 rounded border border-studio-crimson/20 space-y-1">
                        {msg.reflexionSteps.map((step, idx) => (
                          <div key={idx}>
                            • Attempt {step.attempt}: {step.error} (re-prompted model)
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Executed Code Accordion */}
                    {msg.code && (
                      <div className="mt-1">
                        <button
                          onClick={() => toggleCode(msg.id)}
                          className="flex items-center space-x-1 text-[11px] text-studio-cyan hover:underline"
                        >
                          {expandedCodeMap[msg.id] ? (
                            <ChevronDown className="w-3 h-3" />
                          ) : (
                            <ChevronRight className="w-3 h-3" />
                          )}
                          <span>View Executed Python Code</span>
                        </button>

                        {expandedCodeMap[msg.id] && (
                          <div className="mt-2 bg-studio-bg border border-studio-border rounded p-2.5 text-[11px] overflow-x-auto relative">
                            <button
                              onClick={() => onSelectCode(msg.code || "", msg.stdout)}
                              className="absolute top-2 right-2 text-[10px] px-2 py-0.5 rounded bg-studio-card border border-studio-border text-studio-muted hover:text-studio-highlight"
                            >
                              Inspect in Studio ↗
                            </button>
                            <pre className="text-studio-cyan font-mono">{msg.code}</pre>
                            {msg.stdout && (
                              <div className="mt-2 pt-2 border-t border-studio-border/50">
                                <div className="text-[10px] text-studio-muted uppercase mb-1">
                                  Output (stdout):
                                </div>
                                <pre className="text-studio-muted whitespace-pre-wrap">
                                  {msg.stdout}
                                </pre>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* Conversational Text Content */}
                <div className="whitespace-pre-wrap leading-relaxed">
                  {msg.content || (msg.status ? "..." : "")}
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form
        onSubmit={handleSubmit}
        className="p-3 bg-studio-card border-t border-studio-border shrink-0"
      >
        <div className="relative flex items-center">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isStreaming}
            rows={2}
            placeholder={
              isStreaming
                ? "Autonomous Analyst is executing..."
                : "Ask a question, request calculations, or ask for charts (Enter to send)..."
            }
            className="w-full bg-studio-bg border border-studio-border rounded-lg pl-3 pr-10 py-2 text-xs font-mono text-studio-highlight placeholder-studio-muted focus:outline-none focus:border-studio-amber transition resize-none disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isStreaming}
            className="absolute right-2.5 p-1.5 rounded-md bg-studio-amber text-studio-bg hover:bg-studio-amber/90 transition disabled:opacity-30 disabled:hover:bg-studio-amber"
          >
            {isStreaming ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Send className="w-3.5 h-3.5" />
            )}
          </button>
        </div>
        <div className="flex items-center justify-between text-[10px] text-studio-muted mt-1.5 px-1 font-mono">
          <span>Shift + Enter for new line</span>
          <span className="text-studio-cyan">Interactive IPython Sandbox Connected</span>
        </div>
      </form>
    </div>
  );
};
