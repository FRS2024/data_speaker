import React, { useState } from "react";

interface SqlPatchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onApplyPatch: (patchSql: string) => void;
  patchSql?: string;
  rollbackSql?: string;
  incidentTitle?: string;
  impactSummary?: string;
}

const DEFAULT_PATCH_SQL = `-- STEP 1: Release stale idempotent lock keys older than 30m
UPDATE \`production_lake.analytics_core.webhook_locks\`
SET lock_status = 'FORCE_RELEASED', released_at = CURRENT_TIMESTAMP(), release_reason = 'INCIDENT_REMEDY_STORM'
WHERE lock_status = 'ACQUIRED' AND acquired_at < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 MINUTE);

-- STEP 2: Re-queue idempotency payload with randomized exponential jitter
MERGE \`production_lake.analytics_core.fact_subscriptions\` T
USING \`production_lake.staging_lake.stripe_failed_events_quarantine\` S
ON T.subscription_id = S.subscription_id AND S.error_code = 'SCHEMA_LOCK_CONFLICT'
WHEN MATCHED THEN
  UPDATE SET retry_status = 'RETRY_QUEUED', next_attempt_at = TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL CAST(FLOOR(RAND() * 60) AS INT64) SECOND);`;

const DEFAULT_ROLLBACK_SQL = `-- Rollback Plan for Patch #4912
UPDATE \`production_lake.analytics_core.webhook_locks\`
SET lock_status = 'ACQUIRED'
WHERE release_reason = 'INCIDENT_REMEDY_STORM' AND released_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 10 MINUTE);`;

export const SqlPatchModal: React.FC<SqlPatchModalProps> = ({
  isOpen,
  onClose,
  onApplyPatch,
  patchSql = DEFAULT_PATCH_SQL,
  rollbackSql = DEFAULT_ROLLBACK_SQL,
  incidentTitle = "Stripe Webhook Retry Storm Spike",
  impactSummary = "842 paused subscriptions ($42,650 MRR at risk)",
}) => {
  const [activeTab, setActiveTab] = useState<"patch" | "rollback">("patch");
  const [copied, setCopied] = useState(false);
  const [isApplying, setIsApplying] = useState(false);

  if (!isOpen) return null;

  const currentCode = activeTab === "patch" ? patchSql : rollbackSql;

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExecute = async () => {
    setIsApplying(true);
    try {
      await onApplyPatch(currentCode);
      onClose();
    } finally {
      setIsApplying(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop Scrim with Glass Blur */}
      <div
        className="absolute inset-0 bg-surface-container-lowest/80 backdrop-blur-md"
        onClick={onClose}
      />

      {/* Ambient Lighting Glow Behind Modal */}
      <div className="absolute pointer-events-none w-[680px] h-[680px] rounded-full bg-gradient-to-tr from-primary/10 via-secondary/10 to-transparent blur-3xl -z-0 transform -translate-y-4" />

      {/* Centered Modal Dialog */}
      <div className="relative z-10 w-full max-w-[840px] max-h-[92vh] bg-surface-container-low text-on-surface rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-outline-variant/30 animate-in fade-in zoom-in-95 duration-200">
        {/* Top Subtle Luminous Halo Accent Line */}
        <div className="h-0.5 w-full bg-gradient-to-r from-transparent via-primary-container/70 to-transparent" />

        {/* 1. Modal Header */}
        <div className="p-space-lg pb-space-md bg-surface-container-low flex items-start justify-between gap-space-md border-b border-outline-variant/15">
          <div className="flex items-start gap-space-md min-w-0">
            <div className="p-space-xs rounded-xl bg-gradient-to-tr from-primary-container/20 to-secondary-container/30 flex items-center justify-center text-primary shrink-0 shadow-[0_0_20px_rgba(124,167,255,0.25)]">
              <span className="material-symbols-outlined text-[24px]">auto_awesome</span>
            </div>
            <div className="flex flex-col min-w-0">
              <div className="flex flex-wrap items-center gap-space-xs">
                <h2 className="font-headline-md text-headline-md text-on-surface truncate">
                  Generate SQL Patch & Auto-Remediation
                </h2>
                <span className="px-space-xs py-0.5 rounded-full bg-surface-container font-code-tabular text-[11px] text-tertiary flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-tertiary animate-pulse" />
                  <span>Synthesized</span>
                </span>
              </div>
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">
                Incident: <span className="text-on-surface font-medium">{incidentTitle}</span>
                <span className="text-outline mx-1">•</span>
                Impact: <span className="text-error font-medium">{impactSummary}</span>
              </p>
              <div className="flex items-center gap-space-xs mt-space-xs font-code-tabular text-[12px] text-on-surface-variant">
                <span className="material-symbols-outlined text-[15px] text-primary">database</span>
                <span className="text-on-surface">BigQuery</span>
                <span className="text-outline">/</span>
                <span className="text-primary-fixed bg-surface-container px-space-xs py-0.5 rounded">
                  production_lake.analytics_core.fact_subscriptions
                </span>
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            aria-label="Close modal"
            className="w-8 h-8 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface transition-colors shrink-0"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Scrollable Modal Body */}
        <div className="flex-1 overflow-y-auto px-space-lg py-space-md flex flex-col gap-space-md">
          {/* 2. Root Cause Analysis */}
          <div className="p-space-md rounded-xl bg-surface-container flex flex-col gap-space-sm shadow-sm border border-outline-variant/15">
            <div className="flex items-start gap-space-sm">
              <span className="material-symbols-outlined text-primary text-[18px] mt-0.5 shrink-0">
                psychology
              </span>
              <div className="flex flex-col">
                <span className="font-label-caps text-label-caps uppercase text-outline">
                  Autonomous Remediation Synthesis
                </span>
                <p className="font-body-sm text-body-sm text-on-surface leading-relaxed mt-1">
                  Gemini synthesized a safe idempotency lock release and exponential retry reset. The patch adds a deadlock-safe advisory lock bypass and updates transaction status from{" "}
                  <code className="font-code-tabular text-[11px] px-1 py-0.5 rounded bg-surface-container-high text-error">
                    SCHEMA_LOCK_FAIL
                  </code>{" "}
                  to{" "}
                  <code className="font-code-tabular text-[11px] px-1 py-0.5 rounded bg-surface-container-high text-tertiary">
                    RETRY_QUEUED
                  </code>{" "}
                  with backoff jitter.
                </p>
              </div>
            </div>

            {/* Safety Badges */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-space-xs pt-space-xs">
              <div className="p-space-xs rounded-lg bg-surface-container-high flex items-center gap-space-xs text-[11px]">
                <span className="material-symbols-outlined text-tertiary text-[16px] shrink-0">verified_user</span>
                <span className="text-on-surface truncate">0 schema regressions</span>
              </div>
              <div className="p-space-xs rounded-lg bg-surface-container-high flex items-center gap-space-xs text-[11px]">
                <span className="material-symbols-outlined text-primary text-[16px] shrink-0">group_work</span>
                <span className="text-on-surface truncate">842 affected accounts</span>
              </div>
              <div className="p-space-xs rounded-lg bg-surface-container-high flex items-center gap-space-xs text-[11px]">
                <span className="material-symbols-outlined text-secondary text-[16px] shrink-0">speed</span>
                <span className="text-on-surface truncate">~1.2s execution</span>
              </div>
              <div className="p-space-xs rounded-lg bg-surface-container-high flex items-center gap-space-xs text-[11px]">
                <span className="material-symbols-outlined text-tertiary text-[16px] shrink-0">history</span>
                <span className="text-on-surface truncate">Auto rollback plan</span>
              </div>
            </div>
          </div>

          {/* 3. SQL Patch / Rollback Code Preview */}
          <div className="flex flex-col rounded-xl bg-surface-container-lowest overflow-hidden border border-outline-variant/20 shadow-inner">
            <div className="px-space-md py-space-xs bg-surface-container flex items-center justify-between border-b border-outline-variant/15">
              <div className="flex items-center gap-space-xs">
                <button
                  onClick={() => setActiveTab("patch")}
                  className={`px-3 py-1 rounded-full font-code-tabular text-[12px] flex items-center gap-1.5 transition-all ${
                    activeTab === "patch"
                      ? "bg-surface-container-highest text-primary shadow-sm font-medium"
                      : "text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  <span className="material-symbols-outlined text-[14px]">code</span>
                  <span>remedy_patch_v1.sql</span>
                </button>
                <button
                  onClick={() => setActiveTab("rollback")}
                  className={`px-3 py-1 rounded-full font-code-tabular text-[12px] flex items-center gap-1.5 transition-all ${
                    activeTab === "rollback"
                      ? "bg-surface-container-highest text-primary shadow-sm font-medium"
                      : "text-on-surface-variant hover:text-on-surface"
                  }`}
                >
                  <span className="material-symbols-outlined text-[14px]">undo</span>
                  <span>rollback_v1.sql</span>
                </button>
              </div>
              <button
                onClick={handleCopy}
                className="px-2 py-1 rounded text-on-surface-variant hover:text-on-surface text-[12px] font-body-sm flex items-center gap-1 transition-colors"
              >
                <span className="material-symbols-outlined text-[15px]">
                  {copied ? "check" : "content_copy"}
                </span>
                <span>{copied ? "Copied" : "Copy"}</span>
              </button>
            </div>

            <pre className="p-space-md font-code-tabular text-[12px] overflow-x-auto leading-relaxed max-h-56 select-text text-on-surface">
              <code>{currentCode}</code>
            </pre>
          </div>
        </div>

        {/* 5. Modal Footer Action Bar */}
        <div className="p-space-md px-space-lg bg-surface-container border-t border-outline-variant/20 flex flex-wrap items-center justify-between gap-space-md">
          <div className="flex items-center gap-space-sm">
            <img
              alt="Fares"
              className="w-7 h-7 rounded-full object-cover border border-primary/30"
              src="/assets/fares-avatar.png"
            />
            <div className="flex flex-col">
              <span className="text-[12px] font-medium text-on-surface leading-tight">Fares</span>
              <span className="text-[10px] font-code-tabular text-outline">Authorizing Principal</span>
            </div>
          </div>

          <div className="flex items-center gap-space-xs">
            <button
              onClick={onClose}
              className="px-space-md py-1.5 rounded-full hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface font-body-md text-body-md transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleExecute}
              disabled={isApplying}
              className="px-space-lg py-2 rounded-full bg-gradient-to-r from-primary to-primary-container text-surface-container-lowest font-body-md text-body-md font-medium hover:brightness-110 active:scale-95 transition-all shadow-lg flex items-center gap-2 cursor-pointer"
            >
              <span className="material-symbols-outlined text-[18px]">verified</span>
              <span>{isApplying ? "Deploying..." : "Apply & Execute Patch"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
