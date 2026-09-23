import React, { useRef, useEffect } from "react";
import { ChatMessage, SwarmPhaseEvent } from "@/lib/types";
import { FloatingActionDock } from "./FloatingActionDock";
import { SwarmWorkflowStepper } from "./SwarmWorkflowStepper";
import { StatisticalPeerReviewCard } from "./StatisticalPeerReviewCard";
import { TurnAudioPlayer } from "./TurnAudioPlayer";
import Plot from "react-plotly.js";

interface ActiveChatViewProps {
  messages: ChatMessage[];
  promptValue: string;
  onPromptChange: (val: string) => void;
  onSubmitPrompt: () => void;
  isStreaming: boolean;
  sessionId?: string;
  onOpenPatchModal?: () => void;
  onNavigateTab?: (tab: string) => void;
  selectedProvider?: string;
  onSelectProvider?: (provider: string) => void;
  providersStatus?: any;
  activeSwarmPhase?: SwarmPhaseEvent | null;
  isSwarmMode?: boolean;
  onToggleSwarmMode?: () => void;
}

export const ActiveChatView: React.FC<ActiveChatViewProps> = ({
  messages,
  promptValue,
  onPromptChange,
  onSubmitPrompt,
  isStreaming,
  sessionId = "default",
  onOpenPatchModal,
  onNavigateTab,
  selectedProvider,
  onSelectProvider,
  providersStatus,
  activeSwarmPhase,
  isSwarmMode = false,
  onToggleSwarmMode,
}) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isStreaming]);

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] w-full bg-surface relative overflow-hidden">
      {/* Messages Scroll Area */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-space-md sm:px-space-xl py-space-lg flex flex-col gap-space-lg max-w-5xl mx-auto w-full"
      >
        {/* Sticky/Top Swarm Stepper if Swarm mode enabled or active */}
        {(isSwarmMode || activeSwarmPhase) && (
          <div className="sticky top-0 z-10 pb-1">
            <SwarmWorkflowStepper currentPhase={activeSwarmPhase} isStreaming={isStreaming} />
          </div>
        )}

        {messages.map((msg) => {
          if (msg.role === "user") {
            return (
              <div
                key={msg.id}
                className="flex items-start gap-space-sm self-end max-w-[85%] animate-in fade-in slide-in-from-bottom-2 duration-200"
              >
                <div className="flex flex-col items-end gap-1">
                  <span className="font-label-caps text-label-caps text-outline">
                    Fares (You)
                  </span>
                  <div className="p-space-md rounded-2xl rounded-tr-none bg-surface-container-high text-on-surface font-body-md text-body-md shadow-md leading-relaxed">
                    {msg.content}
                  </div>
                </div>
                <img
                  alt="Fares"
                  className="w-8 h-8 rounded-full object-cover shrink-0 mt-3 border border-primary/20"
                  src="/assets/fares-avatar.png"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src =
                      "https://lh3.googleusercontent.com/aida-public/AB6AXuD3oGy_JtI9L39Rh0ZQjW6_1atfTh0851i8WrMZSIJqy8RVSYn29DT7-4qKnUIEi6YiPRaOuE5WMhwYJb314V2St3KPtSarppuKUxR0-JLtyyHgszshSv5QwOspA9Tfq9D-Zwh1xyvgbKaXdN-9E6E5PAjSPVslSm6lvo-22sWNYfikdyoavQb8ZRxeUloQTrwEGwt9F-GmhCfIJ5WzSWwrkGdh8Py13KiZvH3LxqTWDI72LoxsaP8i";
                  }}
                />
              </div>
            );
          }

          // Assistant Turn
          return (
            <div
              key={msg.id}
              className="flex items-start gap-space-sm self-start max-w-[95%] animate-in fade-in duration-200"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary via-secondary to-tertiary flex items-center justify-center shrink-0 shadow-lg mt-1">
                <span
                  className="material-symbols-outlined text-[18px] text-surface-container-lowest"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  auto_awesome
                </span>
              </div>

              <div className="flex flex-col gap-space-sm flex-1 min-w-0">
                <div className="flex items-center gap-space-sm">
                  <span className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider">
                    Gemini Autonomous Analysis
                  </span>
                  {msg.durationMs && (
                    <span className="font-code-tabular text-[11px] px-2 py-0.5 rounded-full bg-surface-container text-tertiary">
                      {(msg.durationMs / 1000).toFixed(2)}s execution
                    </span>
                  )}
                  {msg.activeVersion && (
                    <span className="font-code-tabular text-[11px] px-2 py-0.5 rounded-full bg-surface-container text-primary">
                      {msg.activeVersion}
                    </span>
                  )}
                </div>

                {/* Reflexion Recovery Loop Steps if any */}
                {msg.reflexionSteps && msg.reflexionSteps.length > 0 && (
                  <div className="p-space-sm rounded-xl bg-surface-container-low border border-outline-variant/30 flex flex-col gap-1.5 text-[12px] font-code-tabular">
                    <span className="text-secondary font-medium flex items-center gap-1">
                      <span className="material-symbols-outlined text-[15px]">sync_problem</span>
                      Reflexion Loop Active ({msg.reflexionSteps.length} auto-corrections)
                    </span>
                    {msg.reflexionSteps.map((step, idx) => (
                      <div
                        key={idx}
                        className="pl-3 border-l-2 border-secondary/40 text-on-surface-variant text-[11px]"
                      >
                        Attempt #{step.attempt}: {step.error} → Auto-correcting
                      </div>
                    ))}
                  </div>
                )}

                {/* Status Indicator while generating/running */}
                {msg.status && msg.status !== "complete" && (
                  <div className="flex items-center gap-2 text-tertiary font-code-tabular text-[12px] animate-pulse">
                    <span className="w-2 h-2 rounded-full bg-tertiary"></span>
                    <span>
                      {msg.status === "generating_code"
                        ? "Synthesizing vector queries & pandas pipeline..."
                        : msg.status === "running_sandbox"
                        ? "Executing code in isolated sandbox kernel..."
                        : msg.status === "synthesizing_insights"
                        ? "Synthesizing executive data insights..."
                        : "Reasoning..."}
                    </span>
                  </div>
                )}

                {/* Executed Code Accordion */}
                {msg.code && (
                  <details className="rounded-xl bg-surface-container-lowest border border-outline-variant/20 overflow-hidden group">
                    <summary className="px-space-md py-2 text-[12px] font-code-tabular text-on-surface-variant hover:text-on-surface cursor-pointer select-none flex items-center justify-between bg-surface-container-low">
                      <div className="flex items-center gap-1.5">
                        <span className="material-symbols-outlined text-[15px] text-primary">
                          terminal
                        </span>
                        <span>View Executed Python Pipeline</span>
                      </div>
                      <span className="text-[11px] text-tertiary">Sandbox Verified</span>
                    </summary>
                    <pre className="p-space-md font-code-tabular text-[12px] overflow-x-auto text-on-surface leading-relaxed border-t border-outline-variant/15">
                      <code>{msg.code}</code>
                    </pre>
                  </details>
                )}

                {/* Standard Output if present */}
                {msg.stdout && (
                  <div className="p-space-sm rounded-xl bg-surface-container-lowest border border-outline-variant/15 font-code-tabular text-[12px] text-on-surface-variant max-h-40 overflow-y-auto">
                    <div className="text-outline text-[10px] uppercase mb-1">STDOUT:</div>
                    <pre className="whitespace-pre-wrap">{msg.stdout}</pre>
                  </div>
                )}

                {/* Interactive Figures */}
                {msg.figures && msg.figures.length > 0 && (
                  <div className="flex flex-col gap-space-sm my-2">
                    {msg.figures.map((fig, fIdx) => (
                      <div
                        key={fIdx}
                        className="rounded-2xl bg-surface-container-lowest border border-outline-variant/20 p-space-sm shadow-xl min-h-[360px]"
                      >
                        <Plot
                          data={fig.data || []}
                          layout={{
                            ...fig.layout,
                            autosize: true,
                            paper_bgcolor: "#0e0e0f",
                            plot_bgcolor: "#131314",
                            font: { color: "#e5e2e3", family: "Geist, sans-serif" },
                          }}
                          config={{ responsive: true, displaylogo: false }}
                          className="w-full h-full"
                          style={{ width: "100%", height: "100%" }}
                        />
                      </div>
                    ))}
                  </div>
                )}

                {/* Statistical Peer Review Card & Debate History */}
                {(msg.criticReview || (msg.debateHistory && msg.debateHistory.length > 0)) && (
                  <StatisticalPeerReviewCard
                    criticReview={msg.criticReview}
                    debateHistory={msg.debateHistory}
                  />
                )}

                {/* Natural Insights Content */}
                {msg.content && (
                  <div className="p-space-md rounded-2xl rounded-tl-none bg-surface-container text-on-surface font-body-md text-body-md shadow-md leading-relaxed whitespace-pre-wrap flex flex-col gap-2">
                    {msg.content}
                  </div>
                )}

                {/* Voice Audio Narration Player */}
                {msg.status === "complete" && msg.content && (
                  <TurnAudioPlayer
                    sessionId={sessionId}
                    turnId={msg.id}
                    content={msg.content}
                  />
                )}

                {/* Quick Action Pills on Response */}
                {msg.status === "complete" && (
                  <div className="flex flex-wrap gap-2 pt-1">
                    {onNavigateTab && (
                      <button
                        onClick={() => onNavigateTab("table")}
                        className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container hover:bg-surface-container-high text-primary text-[12px] font-body-sm transition-colors border border-outline-variant/20"
                      >
                        <span className="material-symbols-outlined text-[15px]">table_chart</span>
                        <span>Inspect in Data Grid</span>
                      </button>
                    )}
                    {onOpenPatchModal && (
                      <button
                        onClick={onOpenPatchModal}
                        className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container hover:bg-surface-container-high text-secondary text-[12px] font-body-sm transition-colors border border-outline-variant/20"
                      >
                        <span className="material-symbols-outlined text-[15px]">auto_fix_high</span>
                        <span>SQL Auto-Remediation</span>
                      </button>
                    )}
                    {onNavigateTab && (
                      <button
                        onClick={() => onNavigateTab("history")}
                        className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface text-[12px] font-body-sm transition-colors border border-outline-variant/20"
                      >
                        <span className="material-symbols-outlined text-[15px]">history</span>
                        <span>View Checkpoint</span>
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Floating Bottom Action Dock */}
      <div className="p-space-md bg-gradient-to-t from-surface via-surface/90 to-transparent shrink-0">
        <FloatingActionDock
          value={promptValue}
          onChange={onPromptChange}
          onSubmit={onSubmitPrompt}
          isStreaming={isStreaming}
          selectedProvider={selectedProvider}
          onSelectProvider={onSelectProvider}
          providersStatus={providersStatus}
          isSwarmMode={isSwarmMode}
          onToggleSwarmMode={onToggleSwarmMode}
        />
      </div>
    </div>
  );
};
