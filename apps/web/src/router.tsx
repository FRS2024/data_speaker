import React, { useState, useEffect } from "react";
import {
  createRootRoute,
  createRoute,
  createRouter,
  Outlet,
  useNavigate,
  useSearch,
} from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { z } from "zod";

import { Sidebar } from "./components/Sidebar";
import { Header } from "./components/Header";
import { ZeroStateCanvas } from "./components/ZeroStateCanvas";
import { ActiveChatView } from "./components/ActiveChatView";
import { SqlWorkspace } from "./components/SqlWorkspace";
import { VirtualDataTable } from "./components/VirtualDataTable";
import { VisualizationStudio } from "./components/VisualizationStudio";
import { VersionHistoryView } from "./components/VersionHistoryView";
import { FileUploadModal } from "./components/FileUploadModal";
import { SqlPatchModal } from "./components/SqlPatchModal";
import { SchemaMapper } from "./components/SchemaMapper";
import { DiagnosticsStudio } from "./components/DiagnosticsStudio";
import { ReportsStudio } from "./components/ReportsStudio";

import { useChatStream } from "./hooks/useChatStream";
import {
  createSession,
  fetchSession,
  fetchSchema,
  fetchCheckpoints,
  fetchDatasetData,
  revertSessionVersion,
  getExportUrl,
  fetchProvidersStatus,
} from "./lib/api";
import { queryClient } from "./lib/queryClient";

// Zod Search Parameters Schema for Type-Safe Navigation
const searchSchema = z.object({
  session_id: z.string().optional(),
  tab: z.enum(["canvas", "sql", "table", "charts", "history", "mapper", "diagnostics", "reports"]).optional().default("canvas"),
});

type SearchParams = z.infer<typeof searchSchema>;

// Root Component
const RootLayout: React.FC = () => {
  const navigate = useNavigate();
  const search = useSearch({ strict: false }) as SearchParams;

  const [activeTab, setActiveTab] = useState<string>(search.tab || "canvas");
  const [activeSessionId, setActiveSessionId] = useState<string>(search.session_id || "");
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState<boolean>(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState<boolean>(false);
  const [isPatchModalOpen, setIsPatchModalOpen] = useState<boolean>(false);
  const [promptInput, setPromptInput] = useState<string>("");
  const [isReverting, setIsReverting] = useState<boolean>(false);
  const [selectedProvider, setSelectedProvider] = useState<string>("gemini");
  const [isSwarmMode, setIsSwarmMode] = useState<boolean>(false);

  const { data: providersStatus } = useQuery({
    queryKey: ["providers-status"],
    queryFn: fetchProvidersStatus,
  });

  useEffect(() => {
    if (providersStatus?.active_provider) {
      setSelectedProvider(providersStatus.active_provider);
    }
  }, [providersStatus?.active_provider]);

  // Initialize or fetch default session
  useEffect(() => {
    async function initSession() {
      if (!activeSessionId) {
        const saved = localStorage.getItem("data_speaker_session_id");
        if (saved) {
          setActiveSessionId(saved);
          navigate({ search: (prev: any) => ({ ...prev, session_id: saved }) });
        } else {
          try {
            const newSess = await createSession("Q3 Revenue Cohort Analysis");
            setActiveSessionId(newSess.session_id);
            localStorage.setItem("data_speaker_session_id", newSess.session_id);
            navigate({ search: (prev: any) => ({ ...prev, session_id: newSess.session_id }) });
          } catch (e) {
            console.error("Failed to initialize session", e);
          }
        }
      }
    }
    initSession();
  }, [activeSessionId, navigate]);

  // Sync tab change with search params
  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    navigate({ search: (prev: any) => ({ ...prev, tab }) });
  };

  // Switch session
  const handleSelectSession = (sessionId: string) => {
    setActiveSessionId(sessionId);
    localStorage.setItem("data_speaker_session_id", sessionId);
    navigate({ search: (prev: any) => ({ ...prev, session_id: sessionId }) });
  };

  // Create new session
  const handleNewSession = async () => {
    try {
      const newSess = await createSession("New Ad-hoc Analysis");
      handleSelectSession(newSess.session_id);
      handleTabChange("canvas");
    } catch (err) {
      console.error("Failed to create new session:", err);
    }
  };

  // Queries
  const { data: sessionDetail } = useQuery({
    queryKey: ["session", activeSessionId],
    queryFn: () => fetchSession(activeSessionId),
    enabled: Boolean(activeSessionId),
  });

  const { data: schemaData, refetch: refetchSchema } = useQuery({
    queryKey: ["schema", activeSessionId],
    queryFn: () => fetchSchema(activeSessionId),
    enabled: Boolean(activeSessionId),
  });

  const { data: datasetData, refetch: refetchDataset, isLoading: isDatasetLoading } = useQuery({
    queryKey: ["dataset", activeSessionId, sessionDetail?.active_dataframe_version || "active"],
    queryFn: () => fetchDatasetData(activeSessionId, 50000),
    enabled: Boolean(activeSessionId),
    staleTime: Infinity,
  });

  const { data: checkpoints = [], refetch: refetchCheckpoints } = useQuery({
    queryKey: ["checkpoints", activeSessionId],
    queryFn: () => fetchCheckpoints(activeSessionId),
    enabled: Boolean(activeSessionId),
  });

  // Chat Streaming Hook with Tri-Channel Decoupling
  const {
    messages,
    isStreaming,
    activeFigures,
    activeSwarmPhase,
    sendMessage,
  } = useChatStream({
    onTurnComplete: () => {
      refetchSchema();
      refetchCheckpoints();
      refetchDataset();
      queryClient.invalidateQueries({ queryKey: ["sessions-list"] });
    },
    onDatasetReceived: () => {
      refetchDataset();
    },
  });

  const handleSendPrompt = () => {
    if (!promptInput.trim() || !activeSessionId || isStreaming) return;
    const p = promptInput;
    setPromptInput("");
    sendMessage(activeSessionId, p, selectedProvider, undefined, isSwarmMode);
  };

  const handleRollback = async (versionTag: string) => {
    if (!activeSessionId) return;
    setIsReverting(true);
    try {
      await revertSessionVersion(activeSessionId, versionTag);
      await Promise.all([refetchSchema(), refetchCheckpoints(), refetchDataset()]);
    } catch (e: any) {
      alert(`Rollback error: ${e.message}`);
    } finally {
      setIsReverting(false);
    }
  };

  const handleExport = (format: string) => {
    if (!activeSessionId) return;
    window.open(getExportUrl(activeSessionId, format), "_blank");
  };

  return (
    <div className="flex bg-[#131314] text-[#e5e2e3] min-h-screen font-sans antialiased overflow-x-hidden">
      {/* Fixed Collapsible Sidebar */}
      <Sidebar
        currentTab={activeTab}
        onTabChange={handleTabChange}
        activeSessionId={activeSessionId}
        onSelectSession={handleSelectSession}
        onNewSession={handleNewSession}
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        onOpenSettings={() => setIsUploadModalOpen(true)}
      />

      {/* Main Workspace Frame */}
      <div
        className={`flex-1 flex flex-col min-h-screen transition-all duration-300 ${
          isSidebarCollapsed ? "pl-16" : "pl-64"
        }`}
      >
        {/* Fixed Top Header */}
        <Header
          sessionTitle={sessionDetail?.title || "Q3 Revenue Cohort Analysis"}
          isCollapsed={isSidebarCollapsed}
          onUploadClick={() => setIsUploadModalOpen(true)}
          onPresentClick={() => handleTabChange("reports")}
          activeDataFrameVersion={sessionDetail?.active_dataframe_version || "df_v0"}
        />

        {/* Tab Viewport Routing */}
        <main className="w-full pt-16 flex-1 flex flex-col">
          {activeTab === "canvas" && (
            messages.length === 0 ? (
              <ZeroStateCanvas
                promptValue={promptInput}
                onPromptChange={setPromptInput}
                onSubmitPrompt={handleSendPrompt}
                isStreaming={isStreaming}
                onSelectSuggestedPrompt={(prompt) => {
                  setPromptInput(prompt);
                }}
                onOpenSchemaCatalog={() => handleTabChange("table")}
                tableCount={schemaData?.table_count || 1}
                selectedProvider={selectedProvider}
                onSelectProvider={setSelectedProvider}
                providersStatus={providersStatus}
                isSwarmMode={isSwarmMode}
                onToggleSwarmMode={() => setIsSwarmMode(!isSwarmMode)}
              />
            ) : (
              <ActiveChatView
                messages={messages}
                promptValue={promptInput}
                onPromptChange={setPromptInput}
                onSubmitPrompt={handleSendPrompt}
                isStreaming={isStreaming}
                sessionId={activeSessionId}
                onOpenPatchModal={() => setIsPatchModalOpen(true)}
                onNavigateTab={handleTabChange}
                selectedProvider={selectedProvider}
                onSelectProvider={setSelectedProvider}
                providersStatus={providersStatus}
                activeSwarmPhase={activeSwarmPhase}
                isSwarmMode={isSwarmMode}
                onToggleSwarmMode={() => setIsSwarmMode(!isSwarmMode)}
              />
            )
          )}

          {activeTab === "sql" && (
            <SqlWorkspace
              sessionId={activeSessionId}
              schema={schemaData}
              datasetData={datasetData}
              onExecuteSql={(sql) => {
                sendMessage(activeSessionId, `Execute SQL and optimize scan: \n\`\`\`sql\n${sql}\n\`\`\``);
                handleTabChange("canvas");
              }}
              isExecuting={isStreaming}
            />
          )}

          {activeTab === "mapper" && (
            <SchemaMapper
              sessionId={activeSessionId}
              schema={schemaData}
              onNavigateTab={handleTabChange}
              onExecuteSql={(sql) => {
                handleTabChange("sql");
              }}
              onSendToChat={(prompt) => {
                sendMessage(activeSessionId, prompt);
                handleTabChange("canvas");
              }}
            />
          )}

          {activeTab === "table" && (
            <div className="flex-1 flex flex-col h-[calc(100vh-4rem)]">
              <VirtualDataTable
                columns={
                  datasetData?.columns && datasetData.columns.length > 0
                    ? datasetData.columns
                    : [
                        { name: "cohort_month", type: "DATE" },
                        { name: "active_subscribers", type: "INT64" },
                        { name: "total_mrr", type: "NUMERIC" },
                        { name: "arpu", type: "NUMERIC" },
                        { name: "mom_growth_pct", type: "FLOAT" },
                      ]
                }
                data={
                  datasetData?.rows && datasetData.rows.length > 0
                    ? datasetData.rows
                    : [
                        {
                          cohort_month: "2024-03-01",
                          active_subscribers: 14820,
                          total_mrr: 412850.0,
                          arpu: 27.85,
                          mom_growth_pct: 14.2,
                        },
                        {
                          cohort_month: "2024-02-01",
                          active_subscribers: 13110,
                          total_mrr: 361500.0,
                          arpu: 27.57,
                          mom_growth_pct: 8.7,
                        },
                        {
                          cohort_month: "2024-01-01",
                          active_subscribers: 12050,
                          total_mrr: 332400.0,
                          arpu: 27.58,
                          mom_growth_pct: 11.4,
                        },
                      ]
                }
                totalRows={datasetData?.total_rows || 3}
                tableName={schemaData?.profiles?.[0]?.table_name || "active_dataset"}
                onExport={handleExport}
                isLoading={isDatasetLoading}
              />
            </div>
          )}

          {activeTab === "charts" && (
            <VisualizationStudio
              figures={activeFigures}
              onGenerateChart={(type) => {
                sendMessage(activeSessionId, `Generate an interactive ${type} chart for the active dataset.`);
                handleTabChange("canvas");
              }}
            />
          )}

          {activeTab === "history" && (
            <VersionHistoryView
              checkpoints={checkpoints}
              activeVersion={sessionDetail?.active_dataframe_version || "df_v0"}
              onRollback={handleRollback}
              isReverting={isReverting}
            />
          )}

          {activeTab === "diagnostics" && activeSessionId && (
            <DiagnosticsStudio
              sessionId={activeSessionId}
              onVersionCreated={() => {
                refetchSchema();
                refetchCheckpoints();
                refetchDataset();
              }}
            />
          )}

          {activeTab === "reports" && activeSessionId && (
            <ReportsStudio sessionId={activeSessionId} />
          )}
        </main>
      </div>

      {/* Dataset Ingestion Modal */}
      <FileUploadModal
        isOpen={isUploadModalOpen}
        sessionId={activeSessionId}
        onClose={() => setIsUploadModalOpen(false)}
        onUploadSuccess={() => {
          refetchSchema();
          refetchDataset();
          refetchCheckpoints();
        }}
      />

      {/* SQL Remediation Modal */}
      <SqlPatchModal
        isOpen={isPatchModalOpen}
        onClose={() => setIsPatchModalOpen(false)}
        onApplyPatch={(patchSql) => {
          sendMessage(
            activeSessionId,
            `Apply SQL Remediation Patch with Dry-Run Validation:\n\`\`\`sql\n${patchSql}\n\`\`\``
          );
        }}
      />
    </div>
  );
};

// Define TanStack Router Route Hierarchy
const rootRoute = createRootRoute({
  component: RootLayout,
  validateSearch: (search: Record<string, unknown>): SearchParams => {
    return searchSchema.parse(search);
  },
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: () => <Outlet />,
});

const routeTree = rootRoute.addChildren([indexRoute]);

export const router = createRouter({
  routeTree,
  defaultPreload: "intent",
});

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
