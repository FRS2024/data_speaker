import React from "react";
import { FloatingActionDock } from "./FloatingActionDock";

interface ZeroStateCanvasProps {
  promptValue: string;
  onPromptChange: (val: string) => void;
  onSubmitPrompt: () => void;
  isStreaming: boolean;
  onSelectSuggestedPrompt: (prompt: string) => void;
  onOpenSchemaCatalog?: () => void;
  tableCount?: number;
  selectedProvider?: string;
  onSelectProvider?: (provider: string) => void;
  providersStatus?: any;
  isSwarmMode?: boolean;
  onToggleSwarmMode?: () => void;
  onOpenWarehouse?: () => void;
}

export const ZeroStateCanvas: React.FC<ZeroStateCanvasProps> = ({
  promptValue,
  onPromptChange,
  onSubmitPrompt,
  isStreaming,
  onSelectSuggestedPrompt,
  onOpenSchemaCatalog,
  tableCount = 14,
  selectedProvider,
  onSelectProvider,
  providersStatus,
  isSwarmMode = false,
  onToggleSwarmMode,
  onOpenWarehouse,
}) => {
  const suggestedQueries = [
    {
      badge: "Predictive",
      badgeColor: "bg-secondary-container/40 text-secondary",
      icon: "trending_down",
      title: "Predict Q4 Churn Rate with LTV correlation",
      desc: "Evaluates 90-day retention curve across 42,000 active workspace tenants.",
      prompt: "Predict Q4 customer churn probability with high-confidence LTV correlation metrics across enterprise tiers.",
    },
    {
      badge: "Anomaly Detection",
      badgeColor: "bg-error-container/30 text-error",
      icon: "radar",
      title: "Anomaly detection in Stripe payment webhooks",
      desc: "Isolates webhook latency spikes and failed idempotent settlement retries.",
      prompt: "Detect statistical anomalies in incoming Stripe webhook payload latency over the past 48 hours.",
    },
    {
      badge: "Revenue",
      badgeColor: "bg-primary-container/20 text-primary",
      icon: "finance_mode",
      title: "Breakdown ARR by Enterprise Region & Tier",
      desc: "Cross-tabulates North America, EMEA, and APAC Net Dollar Retention.",
      prompt: "Generate an ARR breakdown grouped by Enterprise Region, contract duration, and upgrade velocity.",
    },
    {
      badge: "Performance",
      badgeColor: "bg-tertiary-container/30 text-tertiary",
      icon: "speed",
      title: "Optimize slow PostgreSQL query on orders_v2",
      desc: "EXPLAIN ANALYZE scan path, index coverage, and buffer hit ratio.",
      prompt: "Analyze query execution plan for orders_v2 and suggest optimal compound indexing.",
    },
  ];

  return (
    <div className="flex flex-col w-full relative min-h-[calc(100vh-4rem)] overflow-hidden select-none">
      {/* Ambient Radiant Backdrops & Fluid Aura */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[18%] left-1/2 -translate-x-1/2 -translate-y-1/2 w-[720px] h-[520px] bg-gradient-to-tr from-secondary-container/20 via-primary-container/15 to-transparent blur-[120px] rounded-full opacity-60"></div>
        <div className="absolute top-[42%] right-[14%] w-[480px] h-[380px] bg-gradient-to-br from-tertiary-container/10 via-primary/10 to-transparent blur-[100px] rounded-full opacity-40"></div>
        <div className="absolute bottom-[-5%] left-[10%] w-[560px] h-[320px] bg-gradient-to-r from-secondary/10 via-transparent to-transparent blur-[90px] rounded-full opacity-30"></div>
      </div>

      {/* Top Action Strip / Branch & Schema Meta Bar */}
      <div className="w-full px-space-lg py-space-sm flex items-center justify-between z-10">
        <div className="flex items-center gap-space-sm">
          <div className="flex items-center gap-space-xs px-space-sm py-1 rounded-full bg-surface-container-low text-on-surface-variant font-code-tabular text-code-tabular shadow-sm">
            <span className="material-symbols-outlined text-[15px] text-primary">alt_route</span>
            <span className="text-on-surface">branch:</span>
            <span className="text-primary font-medium">main-production-db</span>
            <span className="material-symbols-outlined text-[14px] text-outline">expand_more</span>
          </div>
          {onOpenSchemaCatalog && (
            <button
              onClick={onOpenSchemaCatalog}
              className="hidden sm:flex items-center gap-space-xs px-space-sm py-1 rounded-full bg-surface-container-low text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all text-body-sm font-body-sm shadow-sm"
              type="button"
            >
              <span className="material-symbols-outlined text-[15px] text-tertiary">dataset</span>
              <span>Schema Catalog ({tableCount} tables)</span>
            </button>
          )}
          {onOpenWarehouse && (
            <button
              onClick={onOpenWarehouse}
              className="hidden sm:flex items-center gap-space-xs px-space-sm py-1 rounded-full bg-amber-500/10 text-amber-300 hover:bg-amber-500/20 border border-amber-500/20 transition-all text-body-sm font-body-sm shadow-sm"
              type="button"
            >
              <span className="material-symbols-outlined text-[15px] text-amber-400">cloud_sync</span>
              <span>Warehouse Studio</span>
            </button>
          )}
        </div>

        <div className="flex items-center gap-space-sm font-label-caps text-label-caps">
          <div className="flex items-center gap-space-xs px-space-sm py-1 rounded-full bg-surface-container text-tertiary shadow-sm">
            <span className="w-1.5 h-1.5 rounded-full bg-tertiary animate-ping"></span>
            <span className="uppercase tracking-wider">Analytics Core v2.4 Active</span>
          </div>
        </div>
      </div>

      {/* Main Center-Stage Viewport */}
      <div className="flex-1 flex flex-col justify-center items-center px-space-md sm:px-space-lg max-w-5xl mx-auto w-full z-10 py-space-lg">
        {/* Hero Header / Ambient Branding */}
        <div className="flex flex-col items-center text-center space-y-space-md mb-space-lg max-w-2xl">
          {/* Luminous Gemini Spark Badge */}
          <div className="inline-flex items-center gap-space-xs px-space-md py-1.5 rounded-full bg-surface-container-high/70 backdrop-blur-md shadow-md text-primary font-label-caps text-label-caps uppercase tracking-widest border border-primary/20">
            <span
              className="material-symbols-outlined text-[16px] text-primary"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              auto_awesome
            </span>
            <span>Ambient Intelligence Platform • Gemini Core</span>
          </div>

          {/* Hero Headline */}
          <h1 className="font-display-hero text-3xl sm:text-4xl md:text-display-hero text-on-surface tracking-tight leading-tight">
            What insights are we uncovering today,{" "}
            <span className="bg-gradient-to-r from-primary via-secondary to-primary-container bg-clip-text text-transparent">
              Fares
            </span>
            ?
          </h1>

          <p className="font-body-lg text-body-md sm:text-body-lg text-on-surface-variant max-w-xl">
            Synthesize cross-lake telemetry across BigQuery, Snowflake, and Postgres through zero-latency dialogue or hybrid SQL reasoning.
          </p>
        </div>

        {/* Floating Conversational Prompt Bar */}
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
          onOpenWarehouse={onOpenWarehouse}
        />

        {/* Curated Prompt Starters */}
        <div className="w-full max-w-3xl mt-space-lg">
          <div className="flex items-center justify-between mb-space-sm px-space-xs">
            <span className="font-label-caps text-label-caps uppercase text-outline tracking-wider">
              Suggested Inquiries
            </span>
            <button
              onClick={() => onSelectSuggestedPrompt(suggestedQueries[0].prompt)}
              className="font-label-caps text-label-caps text-primary hover:underline flex items-center gap-0.5"
              type="button"
            >
              <span>Explore Templates</span>
              <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-space-sm">
            {suggestedQueries.map((item, idx) => (
              <div
                key={idx}
                onClick={() => onSelectSuggestedPrompt(item.prompt)}
                className="group cursor-pointer p-space-md rounded-2xl bg-surface-container-low hover:bg-surface-container-high transition-all shadow-sm flex flex-col justify-between border border-outline-variant/15 hover:border-primary/30"
              >
                <div>
                  <div className="flex items-start justify-between gap-space-sm mb-space-xs">
                    <div className="flex items-center gap-2">
                      <span className={`p-1 rounded-md ${item.badgeColor}`}>
                        <span className="material-symbols-outlined text-[16px]">{item.icon}</span>
                      </span>
                      <span className="font-label-caps text-label-caps uppercase text-outline">
                        {item.badge}
                      </span>
                    </div>
                    <span className="material-symbols-outlined text-outline group-hover:text-primary transition-colors text-[18px]">
                      arrow_outward
                    </span>
                  </div>
                  <p className="font-body-md text-body-md text-on-surface font-medium leading-snug">
                    {item.title}
                  </p>
                </div>
                <span className="font-body-sm text-body-sm text-on-surface-variant mt-space-xs line-clamp-1">
                  {item.desc}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Floating Context Dock / Live Metric Highlights */}
      <div className="w-full px-space-lg pb-space-md pt-space-xs z-10 shrink-0">
        <div className="max-w-4xl mx-auto flex flex-wrap items-center justify-center gap-space-md py-space-sm px-space-md rounded-full bg-surface-container-lowest/80 backdrop-blur-md shadow-xl text-on-surface-variant font-code-tabular text-body-sm border border-outline-variant/20">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-tertiary"></span>
            <span className="text-on-surface-variant">BigQuery sync:</span>
            <span className="text-on-surface font-medium">2m ago</span>
          </div>
          <span className="text-outline-variant">•</span>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px] text-primary">analytics</span>
            <span className="text-on-surface-variant">Corpus:</span>
            <span className="text-on-surface font-medium">1.4M rows analyzed</span>
          </div>
          <span className="text-outline-variant">•</span>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px] text-secondary">memory</span>
            <span className="text-on-surface-variant">Engine Cache:</span>
            <span className="text-tertiary font-medium">98.4% hit rate</span>
          </div>
          <span className="text-outline-variant hidden sm:inline">•</span>
          <div className="hidden sm:flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px] text-tertiary">bolt</span>
            <span className="text-on-surface-variant">p95 Execution:</span>
            <span className="text-on-surface font-medium">18ms</span>
          </div>
        </div>
      </div>
    </div>
  );
};
