import React, { useState, useEffect } from "react";
import Editor from "@monaco-editor/react";
import { VirtualDataTable } from "./VirtualDataTable";
import { SchemaResponse, DatasetDataResponse, SqlQueryResponse } from "@/lib/types";
import { executeSql, saveSqlCheckpoint } from "@/lib/api";

interface SqlWorkspaceProps {
  sessionId?: string;
  schema?: SchemaResponse;
  datasetData?: DatasetDataResponse;
  onExecuteSql?: (sql: string) => void;
  isExecuting?: boolean;
}

const DEFAULT_SQL = `-- Direct DuckDB & BigQuery OLAP Query
SELECT
  *
FROM df_active
LIMIT 100;`;

export const SqlWorkspace: React.FC<SqlWorkspaceProps> = ({
  sessionId = "",
  schema,
  datasetData,
  onExecuteSql,
  isExecuting = false,
}) => {
  const [activeTab, setActiveTab] = useState("query.sql");
  const [sqlCode, setSqlCode] = useState(DEFAULT_SQL);
  const [schemaFilter, setSchemaFilter] = useState("");
  const [copilotDismissed, setCopilotDismissed] = useState(false);
  const [isRunningDuckDB, setIsRunningDuckDB] = useState(false);
  const [queryResult, setQueryResult] = useState<SqlQueryResponse | null>(null);
  const [queryError, setQueryError] = useState<string | null>(null);
  const [isSavingCheckpoint, setIsSavingCheckpoint] = useState(false);
  const [checkpointStatus, setCheckpointStatus] = useState<string | null>(null);

  const tables = schema?.profiles || [];
  const filteredTables = tables.filter((t) =>
    t.table_name.toLowerCase().includes(schemaFilter.toLowerCase())
  );

  // Set intelligent starter SQL based on available tables
  useEffect(() => {
    if (tables.length > 0 && sqlCode === DEFAULT_SQL) {
      const firstTbl = tables[0].table_name;
      setSqlCode(`-- Direct DuckDB OLAP Query on ${firstTbl}\nSELECT\n  *\nFROM "${firstTbl}"\nLIMIT 100;`);
    }
  }, [tables]);

  const handleRunDuckDB = async () => {
    if (!sessionId) return;
    setIsRunningDuckDB(true);
    setQueryError(null);
    try {
      const res = await executeSql(sessionId, sqlCode, 10000);
      if (res.status === "error") {
        setQueryError(res.error || "Execution failed");
      } else {
        setQueryResult(res);
      }
    } catch (e: any) {
      setQueryError(e.message || "Execution failed");
    } finally {
      setIsRunningDuckDB(false);
    }
  };

  const handleSaveAsVersion = async () => {
    if (!sessionId || !sqlCode) return;
    setIsSavingCheckpoint(true);
    setCheckpointStatus(null);
    try {
      const res = await saveSqlCheckpoint(sessionId, sqlCode, undefined, "Saved from SQL Studio query");
      setCheckpointStatus(`Created ${res.version_tag} (${res.row_count} rows)`);
      setTimeout(() => setCheckpointStatus(null), 4000);
    } catch (e: any) {
      setCheckpointStatus(`Error: ${e.message}`);
    } finally {
      setIsSavingCheckpoint(false);
    }
  };

  const handleApplyCopilot = () => {
    setSqlCode((prev) =>
      prev.includes("LIMIT")
        ? prev
        : `${prev}\n-- Optimized with Gemini Copilot:\nLIMIT 1000;`
    );
    setCopilotDismissed(true);
  };

  // Determine which columns and rows to show in VirtualDataTable
  const displayColumns = queryResult?.columns?.length
    ? queryResult.columns.map((c) => ({ name: c.name, type: c.type }))
    : datasetData?.columns && datasetData.columns.length > 0
    ? datasetData.columns
    : [
        { name: "cohort_month", type: "DATE" },
        { name: "active_subscribers", type: "INT64" },
        { name: "total_mrr", type: "NUMERIC" },
        { name: "arpu", type: "NUMERIC" },
        { name: "mom_growth_pct", type: "FLOAT" },
      ];

  const displayRows = queryResult?.rows !== undefined
    ? queryResult.rows
    : datasetData?.rows && datasetData.rows.length > 0
    ? datasetData.rows
    : [
        {
          cohort_month: "2024-03-01",
          active_subscribers: 14820,
          total_mrr: 412850.0,
          arpu: 27.85,
          mom_growth_pct: 14.2,
        },
      ];

  const displayTotal = queryResult?.total_rows !== undefined
    ? queryResult.total_rows
    : datasetData?.total_rows || displayRows.length;

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] w-full bg-surface overflow-hidden">
      {/* Top Action / Dialect Bar */}
      <div className="h-12 px-space-md bg-surface-container-lowest border-b border-outline-variant/20 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low text-on-surface-variant font-code-tabular text-[12px] border border-outline-variant/30">
            <span className="material-symbols-outlined text-[15px] text-tertiary">database</span>
            <span className="text-on-surface font-medium">DuckDB Embedded OLAP</span>
            <span className="text-outline">|</span>
            <span className="text-tertiary">Zero-Copy In-Memory</span>
          </div>

          {queryResult && (
            <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-mono text-[11px] border border-emerald-500/20">
              <span>{queryResult.execution_time_ms}ms</span>
              <span>•</span>
              <span>{queryResult.total_rows.toLocaleString()} rows returned</span>
            </div>
          )}

          {checkpointStatus && (
            <div className="px-2.5 py-0.5 rounded-full bg-primary/10 text-primary font-mono text-[11px] border border-primary/20">
              {checkpointStatus}
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          {/* Direct DuckDB Execution */}
          <button
            onClick={handleRunDuckDB}
            disabled={isRunningDuckDB || !sessionId}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-tertiary text-on-tertiary font-body-sm text-[12px] font-semibold transition shadow ${
              isRunningDuckDB ? "opacity-60 cursor-not-allowed" : "hover:brightness-110 active:scale-95"
            }`}
          >
            <span className="material-symbols-outlined text-[16px]">
              {isRunningDuckDB ? "hourglass_empty" : "flash_on"}
            </span>
            <span>{isRunningDuckDB ? "Querying..." : "Run DuckDB"}</span>
          </button>

          {/* Save as DataFrame Checkpoint */}
          <button
            onClick={handleSaveAsVersion}
            disabled={isSavingCheckpoint || !sessionId}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-container-high border border-outline-variant/30 text-on-surface hover:bg-surface-variant font-body-sm text-[12px] font-medium transition"
            title="Materialize query results into a new dataset checkpoint (df_vX)"
          >
            <span className="material-symbols-outlined text-[16px] text-tertiary">bookmark_add</span>
            <span>{isSavingCheckpoint ? "Saving..." : "Save as Version"}</span>
          </button>

          {/* Send to AI Analyst */}
          <button
            onClick={() => onExecuteSql?.(sqlCode)}
            disabled={isExecuting}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-primary text-on-primary font-body-sm text-[12px] font-semibold transition ${
              isExecuting ? "opacity-60 cursor-not-allowed" : "hover:brightness-110 active:scale-95"
            }`}
          >
            <span className="material-symbols-outlined text-[16px]">smart_toy</span>
            <span>Send to AI</span>
          </button>
        </div>
      </div>

      {/* Editor Tabs Strip */}
      <div className="bg-surface-container-lowest px-space-md flex items-center gap-1 overflow-x-auto border-b border-outline-variant/15 shrink-0">
        <div
          onClick={() => setActiveTab("query.sql")}
          className="flex items-center gap-2 px-3.5 py-2 rounded-t font-code-tabular text-[12px] cursor-pointer relative bg-surface-container-low text-primary"
        >
          <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary shadow-[0_0_8px_rgba(174,198,255,0.8)]" />
          <span className="material-symbols-outlined text-[15px] text-primary">code</span>
          <span className="font-medium">query.sql</span>
          <span className="w-1.5 h-1.5 rounded-full bg-primary-container"></span>
        </div>
      </div>

      {/* Main Split Body: Schema Catalog (Left) + Editor & Results (Right) */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar: Schema & Table Catalog (~280px) */}
        <aside className="w-72 bg-surface-container-low border-r border-outline-variant/20 flex flex-col shrink-0">
          <div className="p-space-sm">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container text-on-surface-variant focus-within:text-on-surface transition-all text-body-sm">
              <span className="material-symbols-outlined text-[16px] text-outline">search</span>
              <input
                className="w-full bg-transparent text-on-surface placeholder:text-outline focus:outline-none text-[12px]"
                placeholder="Filter tables, columns..."
                value={schemaFilter}
                onChange={(e) => setSchemaFilter(e.target.value)}
              />
            </div>
          </div>

          <div className="flex-1 overflow-y-auto px-space-sm space-y-1">
            <div className="text-[11px] font-label-caps uppercase text-outline px-2 py-1">
              DuckDB Catalog ({filteredTables.length || 1})
            </div>

            {filteredTables.length > 0 ? (
              filteredTables.map((t, idx) => (
                <div key={idx} className="space-y-0.5">
                  <div
                    onClick={() =>
                      setSqlCode(`SELECT * FROM "${t.table_name}" LIMIT 100;`)
                    }
                    title="Click to query this table"
                    className="flex items-center gap-1.5 px-2 py-1.5 rounded-md hover:bg-surface-container text-on-surface cursor-pointer text-[12px] font-code-tabular font-medium transition"
                  >
                    <span className="material-symbols-outlined text-[16px] text-tertiary">table_rows</span>
                    <span className="truncate">{t.table_name}</span>
                    <span className="ml-auto text-[10px] text-outline">
                      {t.row_count ? `${t.row_count.toLocaleString()}r` : ""}
                    </span>
                  </div>
                  <div className="pl-5 space-y-0.5">
                    {t.columns.slice(0, 10).map((col, cIdx) => (
                      <div
                        key={cIdx}
                        onClick={() =>
                          setSqlCode((prev) => `${prev.trim()}\n-- filter: ${col.name}\n`)
                        }
                        className="flex items-center justify-between px-1.5 py-0.5 text-[11px] font-code-tabular text-on-surface-variant hover:text-on-surface cursor-pointer"
                      >
                        <span className="truncate">{col.name}</span>
                        <span className="text-outline text-[10px] uppercase">{col.dtype}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div className="px-3 py-4 text-center text-xs text-outline font-mono">
                No tables in catalog. Upload datasets or sync from warehouse.
              </div>
            )}
          </div>
        </aside>

        {/* Right Pane: Split Vertical (Top: Monaco Editor, Bottom: Table Results) */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Upper Section: Monaco SQL Editor */}
          <div className="h-1/2 flex flex-col border-b border-outline-variant/20 relative">
            {/* Copilot Suggestion Toast */}
            {!copilotDismissed && (
              <div className="bg-surface-container px-space-md py-1.5 border-b border-outline-variant/15 flex items-center justify-between gap-2 shrink-0 animate-fade-in">
                <div className="flex items-center gap-2 overflow-hidden text-body-sm text-[12px]">
                  <span className="material-symbols-outlined text-primary text-[16px] shrink-0">
                    auto_awesome
                  </span>
                  <span className="text-on-surface-variant truncate">
                    <strong className="text-on-surface">Gemini Copilot:</strong> Add{" "}
                    <code className="px-1.5 py-0.5 rounded bg-surface-container-high text-primary font-code-tabular text-[11px]">
                      LIMIT 1000
                    </code>{" "}
                    to optimize scan latency.
                  </span>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <button
                    onClick={handleApplyCopilot}
                    className="px-2.5 py-1 rounded-full bg-primary text-on-primary hover:opacity-90 transition-all font-body-sm text-[11px] font-medium"
                  >
                    Apply
                  </button>
                  <button
                    onClick={() => setCopilotDismissed(true)}
                    className="w-5 h-5 rounded-full flex items-center justify-center text-outline hover:text-on-surface transition-colors"
                  >
                    <span className="material-symbols-outlined text-[14px]">close</span>
                  </button>
                </div>
              </div>
            )}

            {/* Error Message if query failed */}
            {queryError && (
              <div className="bg-red-500/10 border-b border-red-500/30 px-4 py-2 text-xs font-mono text-red-400 flex items-center gap-2 shrink-0">
                <span className="material-symbols-outlined text-[16px]">error</span>
                <span>{queryError}</span>
              </div>
            )}

            {/* Monaco SQL Editor Component */}
            <div className="flex-1 w-full relative">
              <Editor
                height="100%"
                defaultLanguage="sql"
                theme="vs-dark"
                value={sqlCode}
                onChange={(val) => setSqlCode(val || "")}
                options={{
                  minimap: { enabled: false },
                  fontSize: 13,
                  fontFamily: "'JetBrains Mono', monospace",
                  lineNumbers: "on",
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  background: "#0e0e0f",
                }}
              />
            </div>
          </div>

          {/* Lower Section: TanStack Virtual Results Grid */}
          <div className="flex-1 flex flex-col min-h-0 bg-surface-container-lowest">
            <VirtualDataTable
              columns={displayColumns}
              data={displayRows}
              totalRows={displayTotal}
              tableName={queryResult ? "duckdb_results" : "query_results"}
              isLoading={isRunningDuckDB || isExecuting}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
