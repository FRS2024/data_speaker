import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  diagnosticsApi,
  diagnosticsHealthQueryOptions,
  diagnosticsCorrelationsQueryOptions,
  diagnosticsAnomaliesQueryOptions,
  schemaQueryOptions,
  checkpointsQueryOptions,
} from "@/lib/api";
import {
  DataHealthResponse,
  CorrelationMatrixResponse,
  AnomalyReportResponse,
  AutoMLTrainResponse,
  HygieneRecommendation,
} from "@/lib/types";
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  Cpu,
  Flame,
  Info,
  Layers,
  Play,
  RotateCw,
  Sparkles,
  Zap,
  TrendingUp,
  ShieldCheck,
  Check,
  Copy,
  Table as TableIcon,
} from "lucide-react";

interface DiagnosticsStudioProps {
  sessionId: string;
  onVersionCreated?: () => void;
}

export const DiagnosticsStudio: React.FC<DiagnosticsStudioProps> = ({
  sessionId,
  onVersionCreated,
}) => {
  const queryClient = useQueryClient();
  const [activeSubTab, setActiveSubTab] = useState<"health" | "correlations" | "anomalies" | "automl">("health");
  const [correlationMethod, setCorrelationMethod] = useState<"pearson" | "spearman">("pearson");
  const [selectedTarget, setSelectedTarget] = useState<string>("");
  const [copiedCode, setCopiedCode] = useState(false);
  const [applyingId, setApplyingId] = useState<string | null>(null);

  // Queries
  const {
    data: health,
    isLoading: isHealthLoading,
    refetch: refetchHealth,
  } = useQuery(diagnosticsHealthQueryOptions(sessionId));

  const {
    data: correlations,
    isLoading: isCorrLoading,
    refetch: refetchCorrelations,
  } = useQuery({
    ...diagnosticsCorrelationsQueryOptions(sessionId),
    enabled: activeSubTab === "correlations",
  });

  const {
    data: anomalies,
    isLoading: isAnomaliesLoading,
    refetch: refetchAnomalies,
  } = useQuery({
    ...diagnosticsAnomaliesQueryOptions(sessionId),
    enabled: activeSubTab === "anomalies",
  });

  const { data: schemaData } = useQuery(schemaQueryOptions(sessionId));

  // AutoML Mutation
  const autoMlMutation = useMutation({
    mutationFn: (payload: { target_column: string }) =>
      diagnosticsApi.trainAutoML(sessionId, payload),
  });

  // Apply Hygiene Mutation
  const applyHygieneMutation = useMutation({
    mutationFn: (rec: HygieneRecommendation) =>
      diagnosticsApi.applyHygiene(sessionId, {
        recommendation_id: rec.id,
        action: rec.suggested_action,
        column: rec.column,
        parameters: rec.parameters,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["diagnostics", "health", sessionId] });
      queryClient.invalidateQueries({ queryKey: ["checkpoints", sessionId] });
      queryClient.invalidateQueries({ queryKey: ["schema", sessionId] });
      queryClient.invalidateQueries({ queryKey: ["session", sessionId] });
      if (onVersionCreated) onVersionCreated();
    },
    onSettled: () => {
      setApplyingId(null);
    },
  });

  const handleApplyHygiene = (rec: HygieneRecommendation) => {
    setApplyingId(rec.id);
    applyHygieneMutation.mutate(rec);
  };

  const handleCopyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  // Populate initial target column from schema
  React.useEffect(() => {
    if (schemaData && schemaData.length > 0 && !selectedTarget) {
      const primary = schemaData[0];
      if (primary.columns && primary.columns.length > 0) {
        // Default to last column or target-like name
        const candidate =
          primary.columns.find((c) =>
            ["target", "label", "churn", "price", "status", "class", "outcome"].includes(
              c.name.toLowerCase()
            )
          )?.name || primary.columns[primary.columns.length - 1].name;
        setSelectedTarget(candidate);
      }
    }
  }, [schemaData, selectedTarget]);

  return (
    <div className="flex flex-col h-full bg-[#0a0d14] text-slate-200 overflow-hidden">
      {/* Studio Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-cyan-500/20 to-indigo-500/20 border border-cyan-500/30 text-cyan-400">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              Diagnostics & AutoML Studio
              <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                Track B
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Autonomous data health scoring, statistical hygiene, Isolation Forest anomalies & ML baselines
            </p>
          </div>
        </div>

        {/* Sub-tab Navigation */}
        <div className="flex items-center gap-1.5 p-1 bg-slate-950/70 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveSubTab("health")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeSubTab === "health"
                ? "bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            Health & Hygiene
          </button>
          <button
            onClick={() => setActiveSubTab("correlations")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeSubTab === "correlations"
                ? "bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <TrendingUp className="w-3.5 h-3.5" />
            Correlations
          </button>
          <button
            onClick={() => setActiveSubTab("anomalies")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeSubTab === "anomalies"
                ? "bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Flame className="w-3.5 h-3.5" />
            Anomaly Explorer
          </button>
          <button
            onClick={() => setActiveSubTab("automl")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeSubTab === "automl"
                ? "bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 border border-cyan-500/30 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            AutoML Trainer
          </button>
        </div>
      </div>

      {/* Main Studio Body */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* SUBTAB 1: HEALTH & HYGIENE */}
        {activeSubTab === "health" && (
          <div className="space-y-6 max-w-7xl mx-auto">
            {isHealthLoading ? (
              <div className="flex items-center justify-center p-20 text-slate-400">
                <RotateCw className="w-6 h-6 animate-spin text-cyan-400 mr-3" />
                Computing comprehensive dataset health score...
              </div>
            ) : health ? (
              <>
                {/* Health Score Banner */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  {/* Gauge Card */}
                  <div className="md:col-span-1 p-5 rounded-2xl bg-slate-900/50 border border-slate-800 flex flex-col items-center justify-center relative overflow-hidden">
                    <div className="text-center mb-2">
                      <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">
                        Dataset Health Score
                      </span>
                    </div>
                    <div className="relative flex items-center justify-center w-32 h-32 my-2">
                      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        <circle
                          cx="50"
                          cy="50"
                          r="42"
                          className="stroke-slate-800"
                          strokeWidth="8"
                          fill="transparent"
                        />
                        <circle
                          cx="50"
                          cy="50"
                          r="42"
                          stroke={
                            health.overall_score >= 80
                              ? "#10b981"
                              : health.overall_score >= 60
                              ? "#f59e0b"
                              : "#ef4444"
                          }
                          strokeWidth="8"
                          strokeDasharray={264}
                          strokeDashoffset={264 - (264 * health.overall_score) / 100}
                          strokeLinecap="round"
                          fill="transparent"
                          className="transition-all duration-1000 ease-out"
                        />
                      </svg>
                      <div className="absolute flex flex-col items-center">
                        <span className="text-3xl font-extrabold text-white tracking-tight">
                          {health.overall_score}
                        </span>
                        <span
                          className={`text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded ${
                            health.status === "healthy"
                              ? "text-emerald-400 bg-emerald-500/10"
                              : health.status === "warning"
                              ? "text-amber-400 bg-amber-500/10"
                              : "text-rose-400 bg-rose-500/10"
                          }`}
                        >
                          {health.status}
                        </span>
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-400 text-center mt-1">
                      {health.breakdown.total_rows.toLocaleString()} rows •{" "}
                      {health.columns.length} columns
                    </p>
                  </div>

                  {/* 3 Metric Cards */}
                  <div className="md:col-span-3 grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800 flex flex-col justify-between">
                      <div className="flex items-center justify-between text-slate-400 text-xs">
                        <span>Completeness</span>
                        <CheckCircle2 className="w-4 h-4 text-cyan-400" />
                      </div>
                      <div className="my-2">
                        <div className="text-2xl font-bold text-white">
                          {health.breakdown.completeness_score}%
                        </div>
                        <p className="text-xs text-slate-400">
                          {health.breakdown.missing_cells.toLocaleString()} null cells (
                          {(
                            (health.breakdown.missing_cells /
                              Math.max(health.breakdown.total_cells, 1)) *
                            100
                          ).toFixed(1)}
                          %)
                        </p>
                      </div>
                      <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div
                          className="bg-cyan-500 h-full rounded-full"
                          style={{ width: `${health.breakdown.completeness_score}%` }}
                        />
                      </div>
                    </div>

                    <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800 flex flex-col justify-between">
                      <div className="flex items-center justify-between text-slate-400 text-xs">
                        <span>Uniqueness</span>
                        <Layers className="w-4 h-4 text-emerald-400" />
                      </div>
                      <div className="my-2">
                        <div className="text-2xl font-bold text-white">
                          {health.breakdown.uniqueness_score}%
                        </div>
                        <p className="text-xs text-slate-400">
                          {health.breakdown.duplicate_rows.toLocaleString()} duplicate rows
                        </p>
                      </div>
                      <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div
                          className="bg-emerald-500 h-full rounded-full"
                          style={{ width: `${health.breakdown.uniqueness_score}%` }}
                        />
                      </div>
                    </div>

                    <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800 flex flex-col justify-between">
                      <div className="flex items-center justify-between text-slate-400 text-xs">
                        <span>Outlier Free</span>
                        <Flame className="w-4 h-4 text-purple-400" />
                      </div>
                      <div className="my-2">
                        <div className="text-2xl font-bold text-white">
                          {health.breakdown.outlier_score}%
                        </div>
                        <p className="text-xs text-slate-400">
                          Quality consistency: {health.breakdown.consistency_score}%
                        </p>
                      </div>
                      <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div
                          className="bg-purple-500 h-full rounded-full"
                          style={{ width: `${health.breakdown.outlier_score}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Smart Hygiene Recommendations Section */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h2 className="text-sm font-bold text-white flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-cyan-400" />
                      Smart Hygiene Recommendations ({health.recommendations.length})
                    </h2>
                    <button
                      onClick={() => refetchHealth()}
                      className="text-xs text-slate-400 hover:text-cyan-400 flex items-center gap-1 transition"
                    >
                      <RotateCw className="w-3.5 h-3.5" /> Refresh Analysis
                    </button>
                  </div>

                  {health.recommendations.length === 0 ? (
                    <div className="p-6 rounded-xl bg-slate-900/30 border border-slate-800 text-center text-sm text-slate-400">
                      ✨ Great work! No urgent data hygiene defects detected. Your dataset is clean and ready for modeling.
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {health.recommendations.map((rec) => (
                        <div
                          key={rec.id}
                          className={`p-4 rounded-xl border transition-all flex flex-col justify-between ${
                            rec.severity === "critical"
                              ? "bg-rose-950/20 border-rose-800/40 hover:border-rose-700/60"
                              : rec.severity === "warning"
                              ? "bg-amber-950/20 border-amber-800/40 hover:border-amber-700/60"
                              : "bg-slate-900/40 border-slate-800 hover:border-slate-700"
                          }`}
                        >
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span
                                className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full border ${
                                  rec.severity === "critical"
                                    ? "bg-rose-500/10 border-rose-500/20 text-rose-400"
                                    : rec.severity === "warning"
                                    ? "bg-amber-500/10 border-amber-500/20 text-amber-400"
                                    : "bg-slate-800 border-slate-700 text-slate-300"
                                }`}
                              >
                                {rec.severity}
                              </span>
                              <span className="text-[11px] text-slate-400 font-mono">
                                {rec.category}
                              </span>
                            </div>
                            <h3 className="text-sm font-semibold text-white">{rec.title}</h3>
                            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                              {rec.description}
                            </p>
                            <pre className="mt-2.5 p-2 bg-slate-950/80 rounded border border-slate-800 text-[11px] font-mono text-cyan-300 overflow-x-auto">
                              <code>{rec.python_code}</code>
                            </pre>
                          </div>

                          <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between">
                            <span className="text-[11px] text-slate-400">
                              Creates new <code className="text-cyan-400 font-mono">df_vX</code> checkpoint
                            </span>
                            <button
                              onClick={() => handleApplyHygiene(rec)}
                              disabled={applyingId === rec.id}
                              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-sm transition disabled:opacity-50"
                            >
                              {applyingId === rec.id ? (
                                <>
                                  <RotateCw className="w-3.5 h-3.5 animate-spin" />
                                  Applying...
                                </>
                              ) : (
                                <>
                                  <Zap className="w-3.5 h-3.5" />
                                  1-Click Apply
                                </>
                              )}
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Column Health Breakdown Table */}
                <div className="space-y-3">
                  <h2 className="text-sm font-bold text-white flex items-center gap-2">
                    <TableIcon className="w-4 h-4 text-cyan-400" />
                    Column Health Breakdown ({health.columns.length})
                  </h2>
                  <div className="rounded-xl border border-slate-800 overflow-hidden bg-slate-900/30">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-950/60 text-slate-400 font-medium border-b border-slate-800">
                        <tr>
                          <th className="py-2.5 px-4">Column</th>
                          <th className="py-2.5 px-4">Type</th>
                          <th className="py-2.5 px-4">Missing</th>
                          <th className="py-2.5 px-4">Unique Ratio</th>
                          <th className="py-2.5 px-4">Outliers</th>
                          <th className="py-2.5 px-4">Health Score</th>
                          <th className="py-2.5 px-4 text-right">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 font-mono">
                        {health.columns.map((c) => (
                          <tr key={c.name} className="hover:bg-slate-800/30 transition">
                            <td className="py-2.5 px-4 font-semibold text-white font-sans">
                              {c.name}
                            </td>
                            <td className="py-2.5 px-4 text-slate-400 text-[11px]">{c.dtype}</td>
                            <td className="py-2.5 px-4">
                              {c.missing_count > 0 ? (
                                <span className="text-amber-400">
                                  {c.missing_count} ({(c.missing_ratio * 100).toFixed(1)}%)
                                </span>
                              ) : (
                                <span className="text-slate-500">0</span>
                              )}
                            </td>
                            <td className="py-2.5 px-4 text-slate-300">
                              {(c.unique_ratio * 100).toFixed(1)}% ({c.unique_count})
                            </td>
                            <td className="py-2.5 px-4">
                              {c.outlier_count > 0 ? (
                                <span className="text-purple-400">{c.outlier_count}</span>
                              ) : (
                                <span className="text-slate-500">0</span>
                              )}
                            </td>
                            <td className="py-2.5 px-4">
                              <div className="flex items-center gap-2">
                                <span className="text-white font-bold">{c.score}</span>
                                <div className="w-16 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                  <div
                                    className={`h-full rounded-full ${
                                      c.score >= 85
                                        ? "bg-emerald-500"
                                        : c.score >= 70
                                        ? "bg-amber-500"
                                        : "bg-rose-500"
                                    }`}
                                    style={{ width: `${c.score}%` }}
                                  />
                                </div>
                              </div>
                            </td>
                            <td className="py-2.5 px-4 text-right">
                              <span
                                className={`text-[10px] font-sans font-bold uppercase px-2 py-0.5 rounded-full ${
                                  c.status === "excellent"
                                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                                    : c.status === "good"
                                    ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
                                    : c.status === "fair"
                                    ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                                    : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                                }`}
                              >
                                {c.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            ) : null}
          </div>
        )}

        {/* SUBTAB 2: CORRELATIONS */}
        {activeSubTab === "correlations" && (
          <div className="space-y-6 max-w-7xl mx-auto">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-cyan-400" />
                  Pairwise Correlation Analysis
                </h2>
                <p className="text-xs text-slate-400">
                  Statistical association matrices for all numeric features
                </p>
              </div>

              <div className="flex items-center gap-2 p-1 bg-slate-900 rounded-lg border border-slate-800 text-xs">
                <button
                  onClick={() => setCorrelationMethod("pearson")}
                  className={`px-3 py-1 rounded-md transition ${
                    correlationMethod === "pearson"
                      ? "bg-cyan-600 text-white font-medium"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Pearson (Linear)
                </button>
                <button
                  onClick={() => setCorrelationMethod("spearman")}
                  className={`px-3 py-1 rounded-md transition ${
                    correlationMethod === "spearman"
                      ? "bg-cyan-600 text-white font-medium"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Spearman (Rank)
                </button>
              </div>
            </div>

            {isCorrLoading ? (
              <div className="flex items-center justify-center p-20 text-slate-400">
                <RotateCw className="w-6 h-6 animate-spin text-cyan-400 mr-3" />
                Computing numeric correlation matrix...
              </div>
            ) : correlations && correlations.columns.length >= 2 ? (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Correlation Matrix Heatmap Table */}
                <div className="lg:col-span-2 p-4 rounded-xl bg-slate-900/30 border border-slate-800 overflow-x-auto">
                  <table className="w-full text-center text-xs font-mono">
                    <thead>
                      <tr>
                        <th className="p-2 text-left font-sans text-slate-400">Feature</th>
                        {correlations.columns.map((c) => (
                          <th
                            key={c}
                            className="p-2 text-slate-300 font-sans truncate max-w-[90px]"
                            title={c}
                          >
                            {c}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {correlations.columns.map((rCol, rIdx) => {
                        const matrix =
                          correlationMethod === "pearson"
                            ? correlations.pearson
                            : correlations.spearman;
                        return (
                          <tr key={rCol}>
                            <td
                              className="p-2 text-left font-sans font-semibold text-white truncate max-w-[120px]"
                              title={rCol}
                            >
                              {rCol}
                            </td>
                            {correlations.columns.map((cCol, cIdx) => {
                              const val = matrix[rIdx]?.[cIdx] ?? 0;
                              const isDiagonal = rIdx === cIdx;
                              // Heatmap color interpolation
                              const colorClass = isDiagonal
                                ? "bg-slate-800/40 text-slate-500"
                                : val > 0.6
                                ? "bg-emerald-500/30 text-emerald-300 font-bold"
                                : val > 0.3
                                ? "bg-cyan-500/20 text-cyan-300"
                                : val < -0.6
                                ? "bg-rose-500/30 text-rose-300 font-bold"
                                : val < -0.3
                                ? "bg-purple-500/20 text-purple-300"
                                : "bg-slate-900/40 text-slate-400";

                              return (
                                <td
                                  key={cCol}
                                  className={`p-2 rounded transition ${colorClass}`}
                                  title={`${rCol} vs ${cCol}: ${val.toFixed(3)}`}
                                >
                                  {val.toFixed(2)}
                                </td>
                              );
                            })}
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>

                {/* Top Correlations Leaderboard */}
                <div className="space-y-3">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                    Strongest Associations
                  </h3>
                  <div className="space-y-2.5">
                    {correlations.top_correlations.slice(0, 8).map((pair, idx) => (
                      <div
                        key={idx}
                        className="p-3 rounded-xl bg-slate-900/50 border border-slate-800 text-xs flex flex-col gap-1.5"
                      >
                        <div className="flex items-center justify-between font-semibold text-white">
                          <span className="truncate max-w-[140px]">{pair.col1}</span>
                          <span className="text-slate-500 font-normal">↔</span>
                          <span className="truncate max-w-[140px]">{pair.col2}</span>
                        </div>
                        <div className="flex items-center justify-between text-[11px] text-slate-400">
                          <span>
                            Pearson:{" "}
                            <strong
                              className={
                                pair.pearson > 0 ? "text-emerald-400" : "text-rose-400"
                              }
                            >
                              {pair.pearson.toFixed(2)}
                            </strong>
                          </span>
                          <span>Spearman: {pair.spearman.toFixed(2)}</span>
                        </div>
                        <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              pair.pearson > 0 ? "bg-emerald-500" : "bg-rose-500"
                            }`}
                            style={{ width: `${pair.abs_pearson * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-12 text-center text-sm text-slate-400 border border-slate-800 rounded-xl">
                Need at least 2 numeric columns with variance to compute correlations.
              </div>
            )}
          </div>
        )}

        {/* SUBTAB 3: ANOMALY EXPLORER */}
        {activeSubTab === "anomalies" && (
          <div className="space-y-6 max-w-7xl mx-auto">
            {isAnomaliesLoading ? (
              <div className="flex items-center justify-center p-20 text-slate-400">
                <RotateCw className="w-6 h-6 animate-spin text-cyan-400 mr-3" />
                Executing unsupervised Isolation Forest anomaly detection...
              </div>
            ) : anomalies ? (
              <>
                {/* Header Stats */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800">
                    <span className="text-xs text-slate-400">Analyzed Rows</span>
                    <div className="text-2xl font-bold text-white mt-1">
                      {anomalies.total_rows.toLocaleString()}
                    </div>
                    <span className="text-[11px] text-slate-500">
                      {anomalies.features_analyzed.length} numeric features
                    </span>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800">
                    <span className="text-xs text-slate-400">Detected Outliers</span>
                    <div className="text-2xl font-bold text-rose-400 mt-1">
                      {anomalies.anomaly_count}
                    </div>
                    <span className="text-[11px] text-slate-400">
                      {(anomalies.anomaly_rate * 100).toFixed(1)}% contamination rate
                    </span>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800">
                    <span className="text-xs text-slate-400">Detector Model</span>
                    <div className="text-sm font-bold text-cyan-400 mt-1">
                      Isolation Forest (Ensemble)
                    </div>
                    <span className="text-[11px] text-slate-500">
                      Unsupervised tree-based path length scoring
                    </span>
                  </div>
                </div>

                {/* Top Outlier Records Table */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                      Top Outlier Records with Feature Attributions
                    </h3>
                    <button
                      onClick={() => refetchAnomalies()}
                      className="text-xs text-slate-400 hover:text-cyan-400 flex items-center gap-1 transition"
                    >
                      <RotateCw className="w-3.5 h-3.5" /> Re-scan
                    </button>
                  </div>

                  <div className="space-y-3">
                    {anomalies.top_anomalies.map((rec) => (
                      <div
                        key={rec.row_index}
                        className={`p-4 rounded-xl border transition ${
                          rec.is_outlier
                            ? "bg-rose-950/15 border-rose-800/40"
                            : "bg-slate-900/30 border-slate-800"
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-xs font-bold text-white px-2 py-0.5 rounded bg-slate-800 border border-slate-700">
                              Row #{rec.row_index}
                            </span>
                            {rec.is_outlier && (
                              <span className="text-[10px] uppercase font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded-full border border-rose-500/20">
                                Outlier
                              </span>
                            )}
                          </div>
                          <span className="text-xs font-mono text-cyan-400">
                            Anomaly Score:{" "}
                            <strong className="text-white">
                              {(rec.anomaly_score * 100).toFixed(1)}%
                            </strong>
                          </span>
                        </div>

                        {/* Feature Attributions Badges */}
                        {rec.top_attributions.length > 0 && (
                          <div className="flex flex-wrap items-center gap-2 my-2">
                            <span className="text-[11px] text-slate-400">Key Drivers:</span>
                            {rec.top_attributions.map((attr, idx) => (
                              <span
                                key={idx}
                                className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-purple-300"
                              >
                                {attr.column} = {String(attr.value)} (Z: {attr.z_score > 0 ? "+" : ""}
                                {attr.z_score})
                              </span>
                            ))}
                          </div>
                        )}

                        {/* Raw Record Data Snippet */}
                        <div className="mt-2 text-[11px] font-mono text-slate-400 bg-slate-950/60 p-2 rounded border border-slate-800/80 overflow-x-auto">
                          {JSON.stringify(rec.data)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            ) : null}
          </div>
        )}

        {/* SUBTAB 4: AUTOML TRAINER */}
        {activeSubTab === "automl" && (
          <div className="space-y-6 max-w-7xl mx-auto">
            {/* AutoML Config Bar */}
            <div className="p-5 rounded-2xl bg-slate-900/50 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
              <div className="space-y-1">
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-cyan-400" />
                  AutoML Multi-Model Baseline Trainer
                </h2>
                <p className="text-xs text-slate-400">
                  Select a prediction target to train and benchmark Random Forest vs Gradient Boosting
                </p>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 text-xs">
                  <span className="text-slate-400">Target Column:</span>
                  <select
                    value={selectedTarget}
                    onChange={(e) => setSelectedTarget(e.target.value)}
                    className="bg-slate-950 border border-slate-700 text-white rounded-lg px-3 py-1.5 text-xs focus:ring-1 focus:ring-cyan-500 outline-none"
                  >
                    {schemaData?.[0]?.columns?.map((col) => (
                      <option key={col.name} value={col.name}>
                        {col.name} ({col.type})
                      </option>
                    ))}
                  </select>
                </div>

                <button
                  onClick={() => autoMlMutation.mutate({ target_column: selectedTarget })}
                  disabled={!selectedTarget || autoMlMutation.isPending}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 transition disabled:opacity-50"
                >
                  {autoMlMutation.isPending ? (
                    <>
                      <RotateCw className="w-4 h-4 animate-spin" />
                      Training Baselines...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 fill-white" />
                      Train AutoML
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* AutoML Results */}
            {autoMlMutation.data && (
              <div className="space-y-6">
                {/* Winner Banner */}
                <div className="p-5 rounded-2xl bg-gradient-to-r from-cyan-950/40 via-blue-950/30 to-slate-900/40 border border-cyan-500/30 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="p-3 rounded-xl bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                      <Sparkles className="w-6 h-6" />
                    </div>
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400">
                        Winning Model Baseline
                      </span>
                      <h3 className="text-xl font-black text-white">
                        {autoMlMutation.data.best_model}
                      </h3>
                      <p className="text-xs text-slate-400">
                        Task: <span className="font-mono text-cyan-300 uppercase">{autoMlMutation.data.problem_type}</span> • {autoMlMutation.data.rows_trained} rows evaluated
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={() => handleCopyCode(autoMlMutation.data.generated_code)}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition"
                  >
                    {copiedCode ? (
                      <>
                        <Check className="w-4 h-4 text-emerald-400" />
                        Copied Script!
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4 text-slate-400" />
                        Copy Python Code
                      </>
                    )}
                  </button>
                </div>

                {/* Model Leaderboard */}
                <div className="space-y-3">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                    Model Comparison Leaderboard
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {autoMlMutation.data.models.map((model) => (
                      <div
                        key={model.model_name}
                        className={`p-4 rounded-xl border transition flex flex-col justify-between ${
                          model.is_best
                            ? "bg-cyan-950/20 border-cyan-500/50 shadow-md shadow-cyan-500/10"
                            : "bg-slate-900/40 border-slate-800"
                        }`}
                      >
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-bold text-white text-sm">
                              {model.display_name}
                            </h4>
                            {model.is_best && (
                              <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                                Best Model
                              </span>
                            )}
                          </div>
                          <div className="space-y-1.5 my-3 text-xs font-mono">
                            {Object.entries(model.metrics).map(([k, v]) => (
                              <div key={k} className="flex justify-between text-slate-300">
                                <span className="text-slate-400 font-sans capitalize">
                                  {k.replace("_", " ")}:
                                </span>
                                <span className="font-bold text-white">{v.toFixed(4)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                        <div className="pt-2 border-t border-slate-800 text-[11px] text-slate-500">
                          Trained in {model.training_time_ms} ms
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Feature Importance & Confusion Matrix */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Feature Importance Bar Chart */}
                  <div className="p-4 rounded-xl bg-slate-900/30 border border-slate-800 space-y-3">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Feature Importance Rankings
                    </h4>
                    <div className="space-y-2.5">
                      {autoMlMutation.data.feature_importances.map((item) => (
                        <div key={item.feature} className="space-y-1 text-xs">
                          <div className="flex justify-between">
                            <span className="text-white font-medium">{item.feature}</span>
                            <span className="font-mono text-cyan-400">
                              {(item.importance * 100).toFixed(1)}%
                            </span>
                          </div>
                          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                            <div
                              className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full"
                              style={{ width: `${item.importance * 100}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Confusion Matrix (for classification) */}
                  {autoMlMutation.data.confusion_matrix && (
                    <div className="p-4 rounded-xl bg-slate-900/30 border border-slate-800 space-y-3">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Confusion Matrix
                      </h4>
                      <div className="p-2 overflow-x-auto">
                        <table className="w-full text-center text-xs font-mono">
                          <thead>
                            <tr>
                              <th className="p-2 text-slate-500 text-left">True \ Pred</th>
                              {autoMlMutation.data.confusion_matrix.labels.map((lbl) => (
                                <th key={lbl} className="p-2 text-slate-300 font-sans">
                                  {lbl}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {autoMlMutation.data.confusion_matrix.labels.map((lbl, rIdx) => (
                              <tr key={lbl}>
                                <td className="p-2 font-sans font-semibold text-slate-400 text-left">
                                  {lbl}
                                </td>
                                {autoMlMutation.data.confusion_matrix!.matrix[rIdx]?.map(
                                  (val, cIdx) => (
                                    <td
                                      key={cIdx}
                                      className={`p-3 rounded font-bold text-sm ${
                                        rIdx === cIdx
                                          ? "bg-emerald-500/20 text-emerald-300"
                                          : val > 0
                                          ? "bg-rose-500/20 text-rose-300"
                                          : "bg-slate-900 text-slate-500"
                                      }`}
                                    >
                                      {val}
                                    </td>
                                  )
                                )}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>

                {/* Generated Reproducible Code Snippet */}
                <div className="p-4 rounded-xl bg-slate-900/30 border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Standalone Reproducible Python Pipeline
                    </h4>
                    <button
                      onClick={() => handleCopyCode(autoMlMutation.data.generated_code)}
                      className="text-xs text-cyan-400 hover:underline flex items-center gap-1"
                    >
                      <Copy className="w-3.5 h-3.5" /> Copy Code
                    </button>
                  </div>
                  <pre className="p-4 bg-slate-950 rounded-xl border border-slate-800 text-xs font-mono text-slate-300 overflow-x-auto max-h-72">
                    <code>{autoMlMutation.data.generated_code}</code>
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
