import React, { useState, useMemo } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  warehouseApi,
  warehouseConnectorsQueryOptions,
  warehouseSchemasQueryOptions,
  warehouseTablesQueryOptions,
  warehousePreviewQueryOptions,
} from "@/lib/api";
import {
  WarehouseConnectorType,
  WarehouseConnectorSummary,
  WarehouseConfigResponse,
} from "@/lib/types";
import {
  Database,
  Server,
  KeyRound,
  RefreshCw,
  Play,
  CheckCircle2,
  AlertCircle,
  Loader2,
  ArrowRight,
  HardDrive,
  Cpu,
  Layers,
  Search,
  ExternalLink,
  Code2,
  Sparkles,
  Zap,
  Trash2,
  Check,
  ChevronRight,
  ShieldCheck,
  Table,
} from "lucide-react";

interface WarehouseStudioProps {
  sessionId: string;
  onNavigateToTab?: (tab: string) => void;
}

export const WarehouseStudio: React.FC<WarehouseStudioProps> = ({
  sessionId,
  onNavigateToTab,
}) => {
  const queryClient = useQueryClient();

  // Active connector selection
  const [selectedConnector, setSelectedConnector] = useState<WarehouseConnectorType>("postgres");
  const [selectedSchema, setSelectedSchema] = useState<string>("");
  const [selectedTable, setSelectedTable] = useState<string>("");
  const [tableSearch, setTableSearch] = useState<string>("");
  const [activeTab, setActiveTab] = useState<"preview_sync" | "pushdown_sql">("preview_sync");

  // Ingestion configuration
  const [syncLimit, setSyncLimit] = useState<number>(5000);
  const [customSql, setCustomSql] = useState<string>("");
  const [destTableName, setDestTableName] = useState<string>("");

  // Credentials Vault Drawer state
  const [isConfigDrawerOpen, setIsConfigDrawerOpen] = useState<boolean>(false);
  const [configProfileName, setConfigProfileName] = useState<string>("Default Profile");
  const [configFields, setConfigFields] = useState<Record<string, string>>({});
  const [testResult, setTestResult] = useState<{
    status: "idle" | "testing" | "success" | "mock" | "error";
    message?: string;
    latencyMs?: number;
  }>({ status: "idle" });

  // Sync notification banner
  const [syncFeedback, setSyncFeedback] = useState<{
    status: "idle" | "syncing" | "success" | "error";
    message?: string;
    rows?: number;
    tableName?: string;
  }>({ status: "idle" });

  // 1. Fetch all connectors summary
  const {
    data: connectors = [],
    isLoading: isLoadingConnectors,
    refetch: refetchConnectors,
  } = useQuery(warehouseConnectorsQueryOptions());

  const activeConnectorSummary = useMemo(() => {
    return connectors.find((c) => c.connector_type === selectedConnector);
  }, [connectors, selectedConnector]);

  // 2. Fetch schemas for active connector
  const { data: schemasData, isLoading: isLoadingSchemas } = useQuery(
    warehouseSchemasQueryOptions(selectedConnector)
  );

  const schemas = schemasData?.schemas || [];

  // Automatically default selectedSchema when schemas load
  React.useEffect(() => {
    if (schemas.length > 0 && (!selectedSchema || !schemas.includes(selectedSchema))) {
      setSelectedSchema(schemas[0]);
    }
  }, [schemas, selectedSchema]);

  // 3. Fetch tables for active schema
  const { data: tablesData, isLoading: isLoadingTables } = useQuery(
    warehouseTablesQueryOptions(selectedConnector, selectedSchema)
  );

  const tables = tablesData?.tables || [];

  // Automatically default selectedTable when tables load
  React.useEffect(() => {
    if (tables.length > 0 && (!selectedTable || !tables.includes(selectedTable))) {
      setSelectedTable(tables[0]);
    }
  }, [tables, selectedTable]);

  // Update default SQL when table changes
  React.useEffect(() => {
    if (selectedSchema && selectedTable) {
      setCustomSql(`SELECT *\nFROM "${selectedSchema}"."${selectedTable}"\nLIMIT ${syncLimit};`);
      setDestTableName(`${selectedTable}_synced`);
    }
  }, [selectedSchema, selectedTable, syncLimit]);

  // 4. Fetch table preview
  const { data: previewData, isLoading: isLoadingPreview } = useQuery(
    warehousePreviewQueryOptions(selectedConnector, selectedSchema, selectedTable)
  );

  // Filtered tables by search
  const filteredTables = useMemo(() => {
    if (!tableSearch) return tables;
    return tables.filter((t) => t.toLowerCase().includes(tableSearch.toLowerCase()));
  }, [tables, tableSearch]);

  // Mutations
  const testMutation = useMutation({
    mutationFn: () =>
      warehouseApi.testConnection({
        connector_type: selectedConnector,
        config: configFields,
      }),
    onMutate: () => {
      setTestResult({ status: "testing" });
    },
    onSuccess: (data) => {
      setTestResult({
        status: data.status === "connected" ? "success" : data.status === "mock_mode" ? "mock" : "error",
        message: data.message,
        latencyMs: data.latency_ms,
      });
      refetchConnectors();
    },
    onError: (err: any) => {
      setTestResult({
        status: "error",
        message: err.message || "Failed to test connection",
      });
    },
  });

  const saveConfigMutation = useMutation({
    mutationFn: () =>
      warehouseApi.saveConfig({
        connector_type: selectedConnector,
        name: configProfileName || `${selectedConnector.toUpperCase()} Vault Profile`,
        config: configFields,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["warehouse"] });
      refetchConnectors();
      alert("Credentials securely encrypted and saved to workspace vault!");
    },
    onError: (err: any) => {
      alert(`Save error: ${err.message}`);
    },
  });

  const deleteConfigMutation = useMutation({
    mutationFn: (id: string) => warehouseApi.deleteConfig(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["warehouse"] });
      refetchConnectors();
    },
  });

  const syncMutation = useMutation({
    mutationFn: (params: { isPushdown?: boolean }) => {
      setSyncFeedback({ status: "syncing" });
      return warehouseApi.syncData(selectedConnector, sessionId, {
        schema_name: selectedSchema,
        table_name: params.isPushdown ? destTableName : selectedTable,
        sql_query: params.isPushdown ? customSql : undefined,
        limit: syncLimit,
      });
    },
    onSuccess: (res) => {
      setSyncFeedback({
        status: "success",
        rows: res.rows_synced,
        tableName: res.table_name,
        message: `Successfully synchronized ${res.rows_synced.toLocaleString()} rows into session as version ${res.active_version}!`,
      });
      // Invalidate session cache and schema tables
      queryClient.invalidateQueries({ queryKey: ["session", sessionId] });
      queryClient.invalidateQueries({ queryKey: ["checkpoints", sessionId] });
      queryClient.invalidateQueries({ queryKey: ["schema", sessionId] });
    },
    onError: (err: any) => {
      setSyncFeedback({
        status: "error",
        message: err.message || "Synchronization failed",
      });
    },
  });

  // Connector badge helper
  const getBadgeForConnector = (c: WarehouseConnectorSummary) => {
    if (c.configured || c.mode === "connected") {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          Connected
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
        <Sparkles className="w-3 h-3 text-indigo-400" />
        Demo Sandbox
      </span>
    );
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-100 overflow-y-auto">
      {/* Top Header */}
      <div className="border-b border-slate-800 bg-slate-900/60 px-6 py-4 flex flex-wrap items-center justify-between gap-4 backdrop-blur-md sticky top-0 z-20">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-indigo-500/30 text-indigo-400">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">
                Enterprise Warehouse & Lakehouse Studio
              </h1>
              <span className="px-2 py-0.5 text-xs font-medium rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                Track F
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Synchronize PostgreSQL, BigQuery, Snowflake, and Databricks Lakehouse into session Parquet tables
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => refetchConnectors()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300 bg-slate-800/80 hover:bg-slate-700 transition border border-slate-700"
            title="Refresh connectors and status"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoadingConnectors ? "animate-spin" : ""}`} />
            Refresh
          </button>
          <button
            onClick={() => setIsConfigDrawerOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 transition shadow-sm shadow-indigo-500/20"
          >
            <KeyRound className="w-3.5 h-3.5" />
            Credentials Vault
          </button>
        </div>
      </div>

      {/* Sync Feedback Alert */}
      {syncFeedback.status === "syncing" && (
        <div className="mx-6 mt-4 p-4 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-300 flex items-center justify-between animate-fadeIn">
          <div className="flex items-center gap-3">
            <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
            <div>
              <p className="text-sm font-semibold">Streaming warehouse records into session Parquet...</p>
              <p className="text-xs text-blue-300/80">Profiling columns, registering relations, and saving versioned checkpoint.</p>
            </div>
          </div>
        </div>
      )}

      {syncFeedback.status === "success" && (
        <div className="mx-6 mt-4 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 flex items-center justify-between animate-fadeIn">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <div>
              <p className="text-sm font-semibold">{syncFeedback.message}</p>
              <p className="text-xs text-emerald-300/80">
                Table <span className="font-mono font-bold text-white">{syncFeedback.tableName}</span> is now active and ready for AI conversation, AutoML modeling, and SQL analysis.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {onNavigateToTab && (
              <>
                <button
                  onClick={() => onNavigateToTab("chat")}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-200 transition"
                >
                  Analyze in Chat &rarr;
                </button>
                <button
                  onClick={() => onNavigateToTab("sql")}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition"
                >
                  Query in SQL
                </button>
              </>
            )}
            <button
              onClick={() => setSyncFeedback({ status: "idle" })}
              className="text-slate-400 hover:text-white p-1 text-xs"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {syncFeedback.status === "error" && (
        <div className="mx-6 mt-4 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-rose-400" />
            <p className="text-sm font-medium">{syncFeedback.message}</p>
          </div>
          <button
            onClick={() => setSyncFeedback({ status: "idle" })}
            className="text-slate-400 hover:text-white p-1 text-xs"
          >
            ✕
          </button>
        </div>
      )}

      {/* Connector Quadrant Cards */}
      <div className="px-6 pt-5 pb-3">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
          Analytical Warehouses & Lakehouses
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5">
          {connectors.map((c) => {
            const isSelected = selectedConnector === c.connector_type;
            const iconMap = {
              postgres: <Server className="w-5 h-5 text-blue-400" />,
              bigquery: <Cpu className="w-5 h-5 text-cyan-400" />,
              snowflake: <HardDrive className="w-5 h-5 text-sky-400" />,
              databricks: <Layers className="w-5 h-5 text-amber-400" />,
            };

            return (
              <div
                key={c.connector_type}
                onClick={() => {
                  setSelectedConnector(c.connector_type);
                  setSelectedSchema("");
                  setSelectedTable("");
                }}
                className={`relative p-4 rounded-xl border cursor-pointer transition-all duration-200 flex flex-col justify-between ${
                  isSelected
                    ? "bg-slate-800/90 border-indigo-500/60 ring-2 ring-indigo-500/20 shadow-lg shadow-indigo-500/10"
                    : "bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-850"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-2.5">
                    <div className="p-2 rounded-lg bg-slate-800/80 border border-slate-700/60">
                      {iconMap[c.connector_type] || <Database className="w-5 h-5 text-slate-400" />}
                    </div>
                    {getBadgeForConnector(c)}
                  </div>
                  <h3 className="font-semibold text-slate-100 text-sm mb-1">{c.name}</h3>
                  <p className="text-xs text-slate-400 line-clamp-2 mb-3">{c.description}</p>
                </div>

                <div className="flex items-center justify-between pt-2.5 border-t border-slate-800/80 text-xs">
                  <span className="text-slate-400 text-[11px]">
                    {c.saved_configs.length} saved profile{c.saved_configs.length === 1 ? "" : "s"}
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedConnector(c.connector_type);
                      setIsConfigDrawerOpen(true);
                    }}
                    className="text-indigo-400 hover:text-indigo-300 font-medium flex items-center gap-1"
                  >
                    Configure &rarr;
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Studio Two-Column Workspace */}
      <div className="flex-1 px-6 py-3 grid grid-cols-1 lg:grid-cols-12 gap-5 min-h-[520px]">
        {/* Left Column: Schema Tree & Table List */}
        <div className="lg:col-span-4 bg-slate-900/70 border border-slate-800 rounded-xl flex flex-col overflow-hidden">
          {/* Schema Selector Bar */}
          <div className="p-3.5 border-b border-slate-800 bg-slate-900/90">
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Schema / Database
              </label>
              <span className="text-[11px] text-slate-400 font-mono">
                {schemas.length} available
              </span>
            </div>
            <select
              value={selectedSchema}
              onChange={(e) => setSelectedSchema(e.target.value)}
              disabled={isLoadingSchemas || schemas.length === 0}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 font-medium"
            >
              {isLoadingSchemas ? (
                <option>Loading schemas...</option>
              ) : schemas.length === 0 ? (
                <option>No schemas discovered</option>
              ) : (
                schemas.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))
              )}
            </select>
          </div>

          {/* Table Search Input */}
          <div className="p-3 border-b border-slate-800/80 bg-slate-950/40">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-500" />
              <input
                type="text"
                value={tableSearch}
                onChange={(e) => setTableSearch(e.target.value)}
                placeholder="Filter tables..."
                className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          {/* Table List Scrollable */}
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {isLoadingTables ? (
              <div className="flex flex-col items-center justify-center p-8 text-slate-500 text-xs">
                <Loader2 className="w-5 h-5 animate-spin mb-2" />
                <span>Loading tables...</span>
              </div>
            ) : filteredTables.length === 0 ? (
              <div className="text-center p-8 text-slate-500 text-xs">
                No tables match filter
              </div>
            ) : (
              filteredTables.map((t) => {
                const isSelected = selectedTable === t;
                return (
                  <div
                    key={t}
                    onClick={() => setSelectedTable(t)}
                    className={`flex items-center justify-between px-3 py-2.5 rounded-lg cursor-pointer text-xs transition ${
                      isSelected
                        ? "bg-indigo-600/20 text-indigo-300 font-semibold border border-indigo-500/30"
                        : "text-slate-300 hover:bg-slate-800/60 hover:text-white"
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      <Table className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span className="truncate">{t}</span>
                    </div>
                    {isSelected && (
                      <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 shrink-0" />
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Ingestion Studio (Preview or Pushdown SQL) */}
        <div className="lg:col-span-8 bg-slate-900/70 border border-slate-800 rounded-xl flex flex-col overflow-hidden">
          {/* Subheader with Ingestion Mode Tabs & Row Limit selector */}
          <div className="px-5 py-3 border-b border-slate-800 bg-slate-900/90 flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-1 p-1 bg-slate-950 rounded-lg border border-slate-800 text-xs">
              <button
                onClick={() => setActiveTab("preview_sync")}
                className={`px-3 py-1.5 rounded-md font-medium transition ${
                  activeTab === "preview_sync"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                Table Preview & Import
              </button>
              <button
                onClick={() => setActiveTab("pushdown_sql")}
                className={`px-3 py-1.5 rounded-md font-medium transition flex items-center gap-1.5 ${
                  activeTab === "pushdown_sql"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                <Code2 className="w-3.5 h-3.5" />
                Push-Down SQL Runner
              </button>
            </div>

            {/* Row Limit Selector */}
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-400">Row Cap:</span>
              <div className="flex items-center gap-1 bg-slate-950 rounded-lg p-0.5 border border-slate-800 font-mono text-[11px]">
                {[1000, 5000, 25000, 50000].map((lim) => (
                  <button
                    key={lim}
                    onClick={() => setSyncLimit(lim)}
                    className={`px-2 py-1 rounded transition ${
                      syncLimit === lim
                        ? "bg-slate-800 text-indigo-300 font-bold"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    {lim >= 1000 ? `${lim / 1000}K` : lim}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Mode 1: Table Preview & Sync */}
          {activeTab === "preview_sync" && (
            <div className="flex-1 flex flex-col overflow-hidden p-5">
              {/* Selected Table Metadata Card */}
              <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 mb-4">
                <div>
                  <div className="flex items-center gap-2 text-xs text-slate-400 font-mono mb-1">
                    <span>{activeConnectorSummary?.name}</span>
                    <span>&bull;</span>
                    <span className="text-indigo-400 font-bold">{selectedSchema}</span>
                  </div>
                  <h3 className="text-lg font-bold text-white font-mono flex items-center gap-2">
                    {selectedTable || "Select a table"}
                  </h3>
                </div>

                <button
                  disabled={!selectedTable || syncMutation.isPending}
                  onClick={() => syncMutation.mutate({ isPushdown: false })}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-semibold text-xs text-white bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 disabled:opacity-50 transition shadow-md shadow-indigo-500/20"
                >
                  {syncMutation.isPending ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Streaming Parquet...
                    </>
                  ) : (
                    <>
                      <Zap className="w-4 h-4" />
                      Sync Table to Session Parquet ({syncLimit.toLocaleString()} rows)
                    </>
                  )}
                </button>
              </div>

              {/* Column Schema Badges */}
              {previewData?.columns && (
                <div className="mb-3">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">
                    Schema Columns ({previewData.columns.length})
                  </span>
                  <div className="flex flex-wrap gap-1.5 max-h-20 overflow-y-auto">
                    {previewData.columns.map((c) => (
                      <span
                        key={c.name}
                        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] bg-slate-950 border border-slate-800 text-slate-300 font-mono"
                      >
                        <span className="font-semibold text-white">{c.name}</span>
                        <span className="text-[10px] text-cyan-400 font-medium">({c.dtype})</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Data Preview Table */}
              <div className="flex-1 border border-slate-800 rounded-xl overflow-hidden flex flex-col bg-slate-950/80">
                <div className="px-4 py-2.5 border-b border-slate-800 bg-slate-900/60 text-xs font-medium text-slate-400 flex items-center justify-between">
                  <span>Live Warehouse Preview (Top 50 records)</span>
                  <span className="text-[11px] text-slate-500">
                    Est. Total: ~{previewData?.total_rows_estimate.toLocaleString() || "10,000"} rows
                  </span>
                </div>

                <div className="flex-1 overflow-auto">
                  {isLoadingPreview ? (
                    <div className="flex flex-col items-center justify-center p-12 text-slate-500 text-xs">
                      <Loader2 className="w-6 h-6 animate-spin mb-2" />
                      <span>Fetching live table preview...</span>
                    </div>
                  ) : !previewData?.rows || previewData.rows.length === 0 ? (
                    <div className="p-8 text-center text-slate-500 text-xs">
                      No preview records available
                    </div>
                  ) : (
                    <table className="w-full text-left text-xs font-mono">
                      <thead className="bg-slate-900/90 text-slate-400 sticky top-0 border-b border-slate-800">
                        <tr>
                          {previewData.columns.map((col) => (
                            <th key={col.name} className="px-3.5 py-2.5 font-semibold text-slate-300">
                              {col.name}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 text-slate-300">
                        {previewData.rows.map((row, idx) => (
                          <tr key={idx} className="hover:bg-slate-850/50 transition">
                            {previewData.columns.map((col) => {
                              const val = row[col.name];
                              return (
                                <td key={col.name} className="px-3.5 py-2 whitespace-nowrap">
                                  {val === null || val === undefined ? (
                                    <span className="text-slate-600 italic">null</span>
                                  ) : typeof val === "boolean" ? (
                                    <span className={val ? "text-emerald-400" : "text-rose-400"}>
                                      {String(val)}
                                    </span>
                                  ) : typeof val === "number" ? (
                                    <span className="text-cyan-300">{val}</span>
                                  ) : (
                                    String(val)
                                  )}
                                </td>
                              );
                            })}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Mode 2: Push-Down SQL Runner */}
          {activeTab === "pushdown_sql" && (
            <div className="flex-1 flex flex-col p-5 overflow-hidden">
              <div className="mb-3">
                <div className="flex items-center justify-between mb-1">
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
                    Push-Down Warehouse Query
                  </label>
                  <span className="text-[11px] text-slate-400">
                    Executes directly in {activeConnectorSummary?.name}
                  </span>
                </div>
                <textarea
                  value={customSql}
                  onChange={(e) => setCustomSql(e.target.value)}
                  rows={8}
                  className="w-full bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-700/80 rounded-xl p-3.5 focus:outline-none focus:ring-1 focus:ring-indigo-500 leading-relaxed"
                  placeholder="SELECT * FROM table WHERE condition LIMIT 5000;"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 items-end mb-4">
                <div>
                  <label className="text-xs font-semibold text-slate-400 mb-1 block">
                    Session Table Name (Parquet target)
                  </label>
                  <input
                    type="text"
                    value={destTableName}
                    onChange={(e) => setDestTableName(e.target.value)}
                    placeholder="e.g. q1_high_value_orders"
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>

                <button
                  disabled={!customSql.trim() || syncMutation.isPending}
                  onClick={() => syncMutation.mutate({ isPushdown: true })}
                  className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-xs text-white bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 disabled:opacity-50 transition shadow-md shadow-indigo-500/20"
                >
                  {syncMutation.isPending ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Executing Pushdown Query...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 fill-white" />
                      Execute & Stream to Session Parquet
                    </>
                  )}
                </button>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs text-slate-400 flex items-start gap-2.5">
                <Sparkles className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                <p>
                  Push-down queries delegate heavy filtering, joins, and aggregations directly to your cloud warehouse engine, streaming results into optimized columnar Parquet for instantaneous local exploratory analysis and zero cloud egress friction.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Credentials Drawer Modal */}
      {isConfigDrawerOpen && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/80">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  <KeyRound className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-sm">
                    {activeConnectorSummary?.name} Credentials Vault
                  </h3>
                  <p className="text-xs text-slate-400">
                    Save encrypted connection attributes scoped to this workspace
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsConfigDrawerOpen(false)}
                className="text-slate-400 hover:text-white text-sm p-1 rounded-lg"
              >
                ✕
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-4">
              {/* Profile Label */}
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  Connection Profile Label
                </label>
                <input
                  type="text"
                  value={configProfileName}
                  onChange={(e) => setConfigProfileName(e.target.value)}
                  placeholder="e.g. Production RDS or Supabase DB"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              {/* Fields specific to connector */}
              {selectedConnector === "postgres" && (
                <div className="space-y-3">
                  <div className="grid grid-cols-3 gap-2">
                    <div className="col-span-2">
                      <label className="text-xs font-semibold text-slate-400 block mb-1">Host</label>
                      <input
                        type="text"
                        placeholder="ep-example.neon.tech"
                        value={configFields.host || ""}
                        onChange={(e) => setConfigFields({ ...configFields, host: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-slate-400 block mb-1">Port</label>
                      <input
                        type="text"
                        placeholder="5432"
                        value={configFields.port || "5432"}
                        onChange={(e) => setConfigFields({ ...configFields, port: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-400 block mb-1">Database Name</label>
                    <input
                      type="text"
                      placeholder="neondb or postgres"
                      value={configFields.database || ""}
                      onChange={(e) => setConfigFields({ ...configFields, database: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="text-xs font-semibold text-slate-400 block mb-1">User</label>
                      <input
                        type="text"
                        placeholder="alex"
                        value={configFields.user || ""}
                        onChange={(e) => setConfigFields({ ...configFields, user: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-slate-400 block mb-1">Password</label>
                      <input
                        type="password"
                        placeholder="••••••••"
                        value={configFields.password || ""}
                        onChange={(e) => setConfigFields({ ...configFields, password: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                  </div>
                </div>
              )}

              {selectedConnector === "bigquery" && (
                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-semibold text-slate-400 block mb-1">GCP Project ID</label>
                    <input
                      type="text"
                      placeholder="my-company-analytics-prod"
                      value={configFields.project_id || ""}
                      onChange={(e) => setConfigFields({ ...configFields, project_id: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-400 block mb-1">Service Account Key (JSON)</label>
                    <textarea
                      rows={3}
                      placeholder='{"type": "service_account", ...}'
                      value={configFields.credentials_json || ""}
                      onChange={(e) => setConfigFields({ ...configFields, credentials_json: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs font-mono text-cyan-300"
                    />
                  </div>
                </div>
              )}

              {selectedConnector === "snowflake" && (
                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-semibold text-slate-400 block mb-1">Account Identifier</label>
                    <input
                      type="text"
                      placeholder="xy12345.us-east-1"
                      value={configFields.account || ""}
                      onChange={(e) => setConfigFields({ ...configFields, account: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="text-xs font-semibold text-slate-400 block mb-1">Warehouse</label>
                      <input
                        type="text"
                        placeholder="COMPUTE_WH"
                        value={configFields.warehouse || ""}
                        onChange={(e) => setConfigFields({ ...configFields, warehouse: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-slate-400 block mb-1">Database</label>
                      <input
                        type="text"
                        placeholder="ANALYTICS"
                        value={configFields.database || ""}
                        onChange={(e) => setConfigFields({ ...configFields, database: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="text-xs font-semibold text-slate-400 block mb-1">Username</label>
                      <input
                        type="text"
                        placeholder="ANALYST_USER"
                        value={configFields.user || ""}
                        onChange={(e) => setConfigFields({ ...configFields, user: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-slate-400 block mb-1">Password</label>
                      <input
                        type="password"
                        placeholder="••••••••"
                        value={configFields.password || ""}
                        onChange={(e) => setConfigFields({ ...configFields, password: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                      />
                    </div>
                  </div>
                </div>
              )}

              {selectedConnector === "databricks" && (
                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-semibold text-slate-400 block mb-1">Server Hostname</label>
                    <input
                      type="text"
                      placeholder="dbc-example.cloud.databricks.com"
                      value={configFields.server_hostname || ""}
                      onChange={(e) => setConfigFields({ ...configFields, server_hostname: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-400 block mb-1">HTTP Path</label>
                    <input
                      type="text"
                      placeholder="/sql/1.0/warehouses/ab12cd34ef56"
                      value={configFields.http_path || ""}
                      onChange={(e) => setConfigFields({ ...configFields, http_path: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-slate-400 block mb-1">Personal Access Token (PAT)</label>
                    <input
                      type="password"
                      placeholder="dapi••••••••"
                      value={configFields.access_token || ""}
                      onChange={(e) => setConfigFields({ ...configFields, access_token: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white"
                    />
                  </div>
                </div>
              )}

              {/* Test Result Display */}
              {testResult.status !== "idle" && (
                <div
                  className={`p-3 rounded-xl border text-xs flex items-center justify-between ${
                    testResult.status === "success"
                      ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                      : testResult.status === "mock"
                      ? "bg-indigo-500/10 border-indigo-500/30 text-indigo-300"
                      : testResult.status === "testing"
                      ? "bg-blue-500/10 border-blue-500/30 text-blue-300"
                      : "bg-rose-500/10 border-rose-500/30 text-rose-300"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {testResult.status === "testing" ? (
                      <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
                    ) : testResult.status === "success" ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : testResult.status === "mock" ? (
                      <Sparkles className="w-4 h-4 text-indigo-400" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-rose-400" />
                    )}
                    <span>{testResult.message || "Pinging warehouse..."}</span>
                  </div>
                  {testResult.latencyMs && (
                    <span className="font-mono text-[11px] opacity-80">{testResult.latencyMs}ms</span>
                  )}
                </div>
              )}

              {/* Saved Profiles in Workspace */}
              {activeConnectorSummary && activeConnectorSummary.saved_configs.length > 0 && (
                <div className="pt-2 border-t border-slate-800">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                    Saved Vault Profiles
                  </h4>
                  <div className="space-y-1.5 max-h-32 overflow-y-auto">
                    {activeConnectorSummary.saved_configs.map((cfg) => (
                      <div
                        key={cfg.id}
                        className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-xs"
                      >
                        <div>
                          <p className="font-semibold text-white">{cfg.name}</p>
                          <p className="text-[10px] text-slate-500">
                            Saved {new Date(cfg.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <button
                          onClick={() => deleteConfigMutation.mutate(cfg.id)}
                          className="text-slate-500 hover:text-rose-400 p-1 transition"
                          title="Delete profile"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-3.5 border-t border-slate-800 bg-slate-900/90 flex items-center justify-between">
              <button
                disabled={testMutation.isPending}
                onClick={() => testMutation.mutate()}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-300 bg-slate-800 hover:bg-slate-700 transition"
              >
                {testMutation.isPending ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Zap className="w-3.5 h-3.5" />}
                Test Ping
              </button>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setIsConfigDrawerOpen(false)}
                  className="px-3.5 py-2 rounded-lg text-xs font-medium text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  disabled={saveConfigMutation.isPending}
                  onClick={() => saveConfigMutation.mutate()}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 transition shadow-sm"
                >
                  {saveConfigMutation.isPending ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <ShieldCheck className="w-3.5 h-3.5" />}
                  Save to Vault
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
