import React, { useRef, useEffect } from "react";

interface FloatingActionDockProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isStreaming: boolean;
  onToggleSql?: () => void;
  onAttachContext?: () => void;
  activeDialect?: string;
  selectedProvider?: string;
  onSelectProvider?: (provider: string) => void;
  providersStatus?: any;
  isSwarmMode?: boolean;
  onToggleSwarmMode?: () => void;
}

export const FloatingActionDock: React.FC<FloatingActionDockProps> = ({
  value,
  onChange,
  onSubmit,
  isStreaming,
  onToggleSql,
  onAttachContext,
  activeDialect = "PostgreSQL / BigQuery",
  selectedProvider = "gemini",
  onSelectProvider,
  providersStatus,
  isSwarmMode = false,
  onToggleSwarmMode,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isDropdownOpen, setIsDropdownOpen] = React.useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Provider display metadata
  const getProviderInfo = (provKey: string) => {
    switch (provKey) {
      case "gemini":
        return {
          title: "Gemini 2.0 Flash",
          subtitle: "Google AI API",
          icon: "auto_awesome",
          color: "text-[#7ca7ff]",
          bg: "bg-[#7ca7ff]/10",
        };
      case "openai":
        return {
          title: "GPT-4o",
          subtitle: "OpenAI API",
          icon: "psychology",
          color: "text-[#10a37f]",
          bg: "bg-[#10a37f]/10",
        };
      case "anthropic":
        return {
          title: "Claude 3.5 Sonnet",
          subtitle: "Anthropic API",
          icon: "neurology",
          color: "text-[#d97706]",
          bg: "bg-[#d97706]/10",
        };
      default:
        return {
          title: "Offline Sandbox",
          subtitle: "Deterministic Mock",
          icon: "memory",
          color: "text-tertiary",
          bg: "bg-tertiary/10",
        };
    }
  };

  const activeInfo = getProviderInfo(selectedProvider);

  // Auto-resize textarea according to text length
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (value.trim().length > 0 && !isStreaming) {
        onSubmit();
      }
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto z-30">
      <div className="relative bg-surface-container/90 backdrop-blur-2xl rounded-2xl p-space-sm sm:p-space-md shadow-2xl border border-outline-variant/25 transition-all duration-300 focus-within:bg-surface-container-high/95 focus-within:border-primary/40 focus-within:ring-1 focus-within:ring-primary/20">
        {/* Ambient Inner Glow Accent */}
        <div className="absolute inset-0 rounded-2xl pointer-events-none bg-gradient-to-b from-primary/5 via-transparent to-secondary/5 opacity-50"></div>

        <div className="relative flex flex-col gap-space-sm">
          {/* Textarea Input Area */}
          <div className="flex items-start gap-space-sm w-full px-space-xs pt-space-xs">
            <span
              className="material-symbols-outlined text-primary text-[22px] mt-1 shrink-0 select-none animate-pulse"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              auto_awesome
            </span>
            <textarea
              ref={textareaRef}
              rows={2}
              value={value}
              onChange={(e) => onChange(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isStreaming}
              placeholder="Ask anything about cohorts, churn rate, LTV velocity, or execute raw SQL..."
              className="w-full bg-transparent text-on-surface placeholder:text-outline font-body-md text-body-md resize-none outline-none leading-relaxed min-h-[52px]"
            />
            {onToggleSql && (
              <button
                type="button"
                onClick={onToggleSql}
                className="shrink-0 p-1.5 rounded-full text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest transition-colors"
                title="Toggle Synthesized SQL View"
              >
                <span className="material-symbols-outlined text-[20px]">code</span>
              </button>
            )}
          </div>

          {/* Bottom Action Bar / Accessories inside Capsule */}
          <div className="flex flex-wrap items-center justify-between gap-space-sm pt-space-xs px-space-xs border-t border-outline-variant/15">
            {/* Left Group: Data Connectors & Attachments */}
            <div className="flex items-center gap-space-xs">
              <button
                type="button"
                onClick={onAttachContext}
                className="flex items-center gap-1.5 px-space-sm py-1.5 rounded-full bg-surface-container-highest/60 hover:bg-surface-container-highest text-on-surface-variant hover:text-on-surface font-body-sm text-body-sm transition-all shadow-sm"
              >
                <span className="material-symbols-outlined text-[16px] text-tertiary">add_circle</span>
                <span>Context</span>
              </button>

              <div className="flex items-center gap-1 px-space-sm py-1.5 rounded-full bg-surface-container-low text-outline font-code-tabular text-[11px]">
                <span className="w-2 h-2 rounded-full bg-tertiary"></span>
                <span className="text-on-surface-variant font-medium">{activeDialect}</span>
              </div>
            </div>

            {/* Right Group: Engine Switcher, Voice & Execution Button */}
            <div className="flex items-center gap-space-xs">
              {/* Engine Switcher Pill Dropdown */}
              <div className="relative" ref={dropdownRef}>
                <button
                  type="button"
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                  className="flex items-center gap-1.5 px-space-sm py-1.5 rounded-full bg-surface-container-highest hover:bg-surface-bright text-on-surface font-body-sm text-body-sm transition-all shadow-sm border border-outline-variant/15"
                >
                  <span className={`material-symbols-outlined text-[16px] ${activeInfo.color}`}>
                    {activeInfo.icon}
                  </span>
                  <span className="font-medium text-[12px]">{activeInfo.title}</span>
                  <span className={`w-1.5 h-1.5 rounded-full ${
                    providersStatus?.providers?.[selectedProvider]?.configured
                      ? "bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]"
                      : selectedProvider === "mock"
                      ? "bg-primary shadow-[0_0_6px_rgba(124,167,255,0.6)]"
                      : "bg-amber-400/80"
                  }`} />
                  <span className="material-symbols-outlined text-[15px] text-outline">
                    {isDropdownOpen ? "arrow_drop_up" : "arrow_drop_down"}
                  </span>
                </button>

                {/* Dropdown Menu */}
                {isDropdownOpen && (
                  <div className="absolute right-0 bottom-full mb-2 w-72 bg-surface-container/95 backdrop-blur-2xl rounded-2xl p-2 shadow-2xl border border-outline-variant/30 z-50 flex flex-col gap-1 animate-in fade-in zoom-in-95 duration-150">
                    <div className="px-2.5 py-1 text-[10px] font-label-caps uppercase tracking-wider text-outline border-b border-outline-variant/20 mb-1 flex items-center justify-between">
                      <span>Reasoning Engine</span>
                      <span>API Status</span>
                    </div>

                    {/* Google AI Gemini */}
                    <button
                      type="button"
                      onClick={() => {
                        onSelectProvider?.("gemini");
                        setIsDropdownOpen(false);
                      }}
                      className={`flex items-center justify-between p-2 rounded-xl text-left transition-all ${
                        selectedProvider === "gemini"
                          ? "bg-primary/15 text-primary border border-primary/30"
                          : "hover:bg-surface-container-high text-on-surface"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-lg bg-[#7ca7ff]/15 flex items-center justify-center text-[#7ca7ff]">
                          <span className="material-symbols-outlined text-[18px]">auto_awesome</span>
                        </div>
                        <div>
                          <div className="font-medium text-[13px] leading-tight">Google Gemini</div>
                          <div className="text-[11px] text-on-surface-variant font-code-tabular">gemini-2.0-flash</div>
                        </div>
                      </div>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium font-code-tabular ${
                        providersStatus?.providers?.gemini?.configured
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                          : "bg-amber-500/15 text-amber-300 border border-amber-500/25"
                      }`}>
                        {providersStatus?.providers?.gemini?.configured ? "Connected" : "Key Needed"}
                      </span>
                    </button>

                    {/* OpenAI GPT-4o */}
                    <button
                      type="button"
                      onClick={() => {
                        onSelectProvider?.("openai");
                        setIsDropdownOpen(false);
                      }}
                      className={`flex items-center justify-between p-2 rounded-xl text-left transition-all ${
                        selectedProvider === "openai"
                          ? "bg-primary/15 text-primary border border-primary/30"
                          : "hover:bg-surface-container-high text-on-surface"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-lg bg-[#10a37f]/15 flex items-center justify-center text-[#10a37f]">
                          <span className="material-symbols-outlined text-[18px]">psychology</span>
                        </div>
                        <div>
                          <div className="font-medium text-[13px] leading-tight">OpenAI</div>
                          <div className="text-[11px] text-on-surface-variant font-code-tabular">gpt-4o</div>
                        </div>
                      </div>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium font-code-tabular ${
                        providersStatus?.providers?.openai?.configured
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                          : "bg-amber-500/15 text-amber-300 border border-amber-500/25"
                      }`}>
                        {providersStatus?.providers?.openai?.configured ? "Connected" : "Key Needed"}
                      </span>
                    </button>

                    {/* Offline Sandbox Mock */}
                    <button
                      type="button"
                      onClick={() => {
                        onSelectProvider?.("mock");
                        setIsDropdownOpen(false);
                      }}
                      className={`flex items-center justify-between p-2 rounded-xl text-left transition-all ${
                        selectedProvider === "mock"
                          ? "bg-primary/15 text-primary border border-primary/30"
                          : "hover:bg-surface-container-high text-on-surface"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-lg bg-tertiary/15 flex items-center justify-center text-tertiary">
                          <span className="material-symbols-outlined text-[18px]">memory</span>
                        </div>
                        <div>
                          <div className="font-medium text-[13px] leading-tight">Deterministic Sandbox</div>
                          <div className="text-[11px] text-on-surface-variant font-code-tabular">Offline / Zero Cost</div>
                        </div>
                      </div>
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-medium font-code-tabular bg-primary/20 text-primary border border-primary/30">
                        Ready
                      </span>
                    </button>
                  </div>
                )}
              </div>

              {/* Swarm Debate Mode Toggle */}
              {onToggleSwarmMode && (
                <button
                  type="button"
                  onClick={onToggleSwarmMode}
                  className={`h-9 px-3 rounded-full flex items-center gap-1.5 transition-all text-xs font-medium border ${
                    isSwarmMode
                      ? "bg-indigo-500/20 text-indigo-300 border-indigo-500/50 shadow-[0_0_12px_rgba(99,102,241,0.25)]"
                      : "bg-surface-container hover:bg-surface-container-high text-on-surface-variant border-outline-variant/20 hover:text-on-surface"
                  }`}
                  title={
                    isSwarmMode
                      ? "Swarm Debate Active: Analyst + Statistician Peer Review"
                      : "Enable Dual-Agent Swarm Debate Mode"
                  }
                >
                  <span
                    className={`material-symbols-outlined text-[17px] ${
                      isSwarmMode ? "text-indigo-400" : "text-on-surface-variant"
                    }`}
                  >
                    groups
                  </span>
                  <span className="hidden sm:inline font-mono">
                    {isSwarmMode ? "Swarm: ON" : "Swarm: OFF"}
                  </span>
                </button>
              )}

              {/* Audio Dictation Trigger */}
              <button
                type="button"
                className="w-9 h-9 rounded-full flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container-highest transition-all"
                title="Audio Reasoning"
              >
                <span className="material-symbols-outlined text-[19px]">mic</span>
              </button>

              {/* Main Submission Pill */}
              <button
                type="button"
                onClick={onSubmit}
                disabled={isStreaming || !value.trim()}
                className={`h-9 px-space-md rounded-full bg-gradient-to-r from-primary to-primary-container text-surface-container-lowest font-body-md text-body-md font-medium flex items-center gap-1.5 transition-all shadow-lg active:scale-95 ${
                  isStreaming || !value.trim()
                    ? "opacity-50 cursor-not-allowed"
                    : "hover:brightness-110 cursor-pointer shadow-[0_0_16px_rgba(124,167,255,0.3)]"
                }`}
              >
                <span>{isStreaming ? "Thinking..." : "Run"}</span>
                <span className="material-symbols-outlined text-[18px]">
                  {isStreaming ? "hourglass_empty" : "arrow_upward"}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
