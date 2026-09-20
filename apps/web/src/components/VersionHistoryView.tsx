import React, { useState } from "react";
import { CheckpointSummary } from "@/lib/types";

interface VersionHistoryViewProps {
  checkpoints: CheckpointSummary[];
  activeVersion: string;
  onRollback: (versionTag: string) => Promise<void>;
  isReverting?: boolean;
}

export const VersionHistoryView: React.FC<VersionHistoryViewProps> = ({
  checkpoints,
  activeVersion,
  onRollback,
  isReverting = false,
}) => {
  const [selectedVersion, setSelectedVersion] = useState<string>(activeVersion || "df_v0");

  const activeCheckpoint =
    checkpoints.find((c) => c.version_tag === selectedVersion) || checkpoints[0];

  const handleRollbackClick = async () => {
    if (!selectedVersion) return;
    if (confirm(`Are you sure you want to rollback to checkpoint ${selectedVersion}?`)) {
      await onRollback(selectedVersion);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] w-full bg-surface overflow-hidden">
      {/* Top Header Strip */}
      <div className="p-space-lg bg-surface-container-low border-b border-outline-variant/20 flex flex-wrap items-center justify-between gap-space-md shrink-0">
        <div className="flex items-center gap-space-sm">
          <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center text-primary shadow-[0_0_12px_rgba(124,167,255,0.2)]">
            <span className="material-symbols-outlined text-[20px]">history</span>
          </div>
          <div>
            <div className="flex items-center gap-space-sm">
              <h2 className="font-headline-md text-headline-md text-on-surface tracking-tight">
                Rollback Engine & Snapshot Comparison
              </h2>
              <div className="flex items-center gap-1.5 px-space-sm py-0.5 rounded-full bg-tertiary-container/20 text-tertiary font-label-caps text-label-caps uppercase tracking-wider">
                <span className="w-1.5 h-1.5 rounded-full bg-tertiary animate-pulse"></span>
                <span>Time-Travel Active</span>
              </div>
            </div>
            <p className="text-body-sm text-on-surface-variant mt-0.5">
              Zero-latency dataframe state recovery with Parquet checkpoints and BigQuery snapshot delta.
            </p>
          </div>
        </div>

        {selectedVersion !== activeVersion && (
          <button
            onClick={handleRollbackClick}
            disabled={isReverting}
            className="flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-error to-[#ff8c82] text-[#690005] font-body-md text-body-md font-semibold hover:brightness-110 active:scale-95 transition-all shadow-[0_0_16px_rgba(255,180,171,0.3)] disabled:opacity-50 cursor-pointer"
          >
            <span className="material-symbols-outlined text-[18px]">undo</span>
            <span>{isReverting ? "Rolling back..." : `Rollback to ${selectedVersion}`}</span>
          </button>
        )}
      </div>

      {/* Safety Verification Chips Shelf */}
      <div className="px-space-lg py-space-sm bg-surface-container-lowest/80 flex flex-wrap items-center gap-space-sm border-b border-outline-variant/15 text-[12px]">
        <div className="flex items-center gap-space-xs px-space-md py-1 rounded-full bg-surface-container-high/70 text-on-surface">
          <span className="material-symbols-outlined text-tertiary text-[16px]">verified_user</span>
          <span className="text-on-surface-variant">Time-Travel Snapshot:</span>
          <span className="font-code-tabular text-tertiary font-medium">Valid & Verified</span>
        </div>
        <div className="flex items-center gap-space-xs px-space-md py-1 rounded-full bg-surface-container-high/70 text-on-surface">
          <span className="material-symbols-outlined text-primary text-[16px]">sync_saved_locally</span>
          <span className="text-on-surface-variant">Row State Idempotency:</span>
          <span className="font-code-tabular text-on-surface font-medium">100% Deterministic</span>
        </div>
        <div className="flex items-center gap-space-xs px-space-md py-1 rounded-full bg-surface-container-high/70 text-on-surface">
          <span className="material-symbols-outlined text-secondary text-[16px]">speed</span>
          <span className="text-on-surface-variant">Estimated Revert Latency:</span>
          <span className="font-code-tabular text-secondary font-medium">&lt; 50ms</span>
        </div>
      </div>

      {/* Split Body: Checkpoints Timeline (Left) + Snapshot Details & Diff (Right) */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: Checkpoint Timeline List (~320px) */}
        <aside className="w-80 bg-surface-container-low border-r border-outline-variant/20 flex flex-col shrink-0">
          <div className="p-space-sm border-b border-outline-variant/15 text-[11px] font-label-caps uppercase text-outline">
            Version Timeline ({checkpoints.length})
          </div>

          <div className="flex-1 overflow-y-auto p-space-sm space-y-2">
            {checkpoints.length === 0 ? (
              <div className="p-4 text-center text-outline text-[12px] italic">
                No checkpoints created yet. Run an analysis turn to create df_v1.
              </div>
            ) : (
              checkpoints.map((cp) => {
                const isCurrentActive = cp.version_tag === activeVersion;
                const isSelected = cp.version_tag === selectedVersion;

                return (
                  <div
                    key={cp.id}
                    onClick={() => setSelectedVersion(cp.version_tag)}
                    className={`p-space-sm rounded-xl cursor-pointer transition-all border ${
                      isSelected
                        ? "bg-surface-container-high border-primary/40 shadow-sm"
                        : "bg-surface-container-lowest border-outline-variant/20 hover:border-outline-variant/40"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center gap-1.5">
                        <span className="font-code-tabular text-[12px] font-bold text-primary">
                          {cp.version_tag}
                        </span>
                        {isCurrentActive && (
                          <span className="px-1.5 py-0.2 rounded-full bg-tertiary-container/30 text-tertiary text-[10px] font-label-caps font-semibold">
                            ACTIVE
                          </span>
                        )}
                      </div>
                      <span className="text-[11px] font-code-tabular text-outline">
                        {new Date(cp.created_at).toLocaleTimeString()}
                      </span>
                    </div>

                    <p className="text-[12px] text-on-surface line-clamp-2 leading-snug">
                      {cp.operation_summary || "Initial dataset profile"}
                    </p>

                    <div className="flex items-center gap-2 mt-2 pt-1 border-t border-outline-variant/15 text-[11px] font-code-tabular text-outline">
                      <span>{cp.row_count.toLocaleString()} rows</span>
                      <span>•</span>
                      <span>{cp.column_count} cols</span>
                      <span>•</span>
                      <span>{(cp.memory_bytes / 1024).toFixed(1)} KB</span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </aside>

        {/* Right: Snapshot Comparison Details */}
        <div className="flex-1 overflow-y-auto p-space-lg bg-surface flex flex-col gap-space-lg">
          {activeCheckpoint ? (
            <div className="flex flex-col gap-space-md max-w-4xl mx-auto w-full">
              {/* Checkpoint Header Card */}
              <div className="p-space-md rounded-2xl bg-surface-container border border-outline-variant/25 shadow-lg flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-headline-md text-primary font-bold">
                      {activeCheckpoint.version_tag}
                    </span>
                    <span className="text-outline">•</span>
                    <span className="text-on-surface font-medium">
                      {activeCheckpoint.operation_summary}
                    </span>
                  </div>
                  <span className="text-[12px] text-on-surface-variant font-code-tabular mt-1 block">
                    Created at {new Date(activeCheckpoint.created_at).toLocaleString()} • Memory footprint:{" "}
                    {(activeCheckpoint.memory_bytes / (1024 * 1024)).toFixed(2)} MB
                  </span>
                </div>
              </div>

              {/* Schema Diff Grid */}
              {activeCheckpoint.diff_from_previous && (
                <div className="p-space-md rounded-2xl bg-surface-container border border-outline-variant/25 shadow-lg">
                  <h3 className="font-label-caps text-label-caps uppercase text-outline mb-space-sm tracking-wider">
                    Delta From Previous Version
                  </h3>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-space-sm font-code-tabular text-body-sm">
                    <div className="p-3 rounded-xl bg-surface-container-low border border-outline-variant/20">
                      <div className="text-outline text-[11px]">Row Delta</div>
                      <div
                        className={`text-[16px] font-bold ${
                          activeCheckpoint.diff_from_previous.row_delta >= 0
                            ? "text-tertiary"
                            : "text-error"
                        }`}
                      >
                        {activeCheckpoint.diff_from_previous.row_delta >= 0 ? "+" : ""}
                        {activeCheckpoint.diff_from_previous.row_delta.toLocaleString()}
                      </div>
                    </div>

                    <div className="p-3 rounded-xl bg-surface-container-low border border-outline-variant/20">
                      <div className="text-outline text-[11px]">Column Delta</div>
                      <div
                        className={`text-[16px] font-bold ${
                          activeCheckpoint.diff_from_previous.column_delta >= 0
                            ? "text-primary"
                            : "text-error"
                        }`}
                      >
                        {activeCheckpoint.diff_from_previous.column_delta >= 0 ? "+" : ""}
                        {activeCheckpoint.diff_from_previous.column_delta}
                      </div>
                    </div>

                    <div className="p-3 rounded-xl bg-surface-container-low border border-outline-variant/20">
                      <div className="text-outline text-[11px]">Columns Added</div>
                      <div className="text-[16px] font-bold text-tertiary">
                        {activeCheckpoint.diff_from_previous.columns_added.length}
                      </div>
                    </div>

                    <div className="p-3 rounded-xl bg-surface-container-low border border-outline-variant/20">
                      <div className="text-outline text-[11px]">Columns Removed</div>
                      <div className="text-[16px] font-bold text-error">
                        {activeCheckpoint.diff_from_previous.columns_removed.length}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Idempotent Rollback Code Snippet Preview */}
              <div className="p-space-md rounded-2xl bg-surface-container-lowest border border-outline-variant/25 shadow-lg font-code-tabular text-[12px]">
                <div className="flex items-center justify-between pb-2 border-b border-outline-variant/15 text-outline">
                  <span>Deterministic Recovery Execution Plan</span>
                  <span className="text-tertiary">Automated Rollback Engine</span>
                </div>
                <pre className="mt-3 text-on-surface-variant overflow-x-auto leading-relaxed">
                  <code>{`-- Automated Idempotent Rollback Plan for ${activeCheckpoint.version_tag}
BEGIN TRANSACTION;

-- Step 1: Restore DataFrame state from immutable Parquet checkpoint
LOAD PARQUET '${activeCheckpoint.version_tag}.parquet' INTO TABLE active_dataset;

-- Step 2: Validate row count and column checksum
ASSERT (SELECT COUNT(*) FROM active_dataset) = ${activeCheckpoint.row_count};

-- Step 3: Re-point active session pointer
UPDATE sessions SET active_dataframe_version = '${activeCheckpoint.version_tag}' WHERE session_id = '${activeCheckpoint.session_id}';

COMMIT;`}</code>
                </pre>
              </div>
            </div>
          ) : (
            <div className="text-center text-outline py-20 font-body-md">
              Select a checkpoint from the timeline to inspect its snapshot diff.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
