import React, { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchSessions, authApi, getActiveWorkspace, setActiveWorkspace, getStoredTokens } from "@/lib/api";
import { queryClient } from "@/lib/queryClient";
import { User, Workspace } from "@/lib/types";
import { AuthModal } from "./AuthModal";
import { TeamDrawer } from "./TeamDrawer";
import { Building2, Shield, User as UserIcon } from "lucide-react";

interface SidebarProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
  activeSessionId?: string;
  onSelectSession?: (sessionId: string) => void;
  onNewSession?: () => void;
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
  onOpenSettings?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onTabChange,
  activeSessionId,
  onSelectSession,
  onNewSession,
  isCollapsed = false,
  onToggleCollapse,
  onOpenSettings,
}) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [activeWorkspace, setActiveWs] = useState<Workspace | null>(getActiveWorkspace());
  const [isTeamDrawerOpen, setIsTeamDrawerOpen] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  useEffect(() => {
    const { accessToken } = getStoredTokens();
    if (accessToken) {
      authApi.me().then((data) => {
        setCurrentUser(data.user);
        if (data.workspaces.length > 0) {
          const current = getActiveWorkspace();
          const found = data.workspaces.find((w) => w.id === current?.id) || data.workspaces[0];
          setActiveWs(found);
          setActiveWorkspace(found);
        }
      }).catch(() => {
        setCurrentUser(null);
      });
    }
  }, []);

  const handleWorkspaceChange = (ws: Workspace) => {
    setActiveWs(ws);
    queryClient.invalidateQueries({ queryKey: ["sessions-list"] });
  };

  const handleAuthSuccess = (user: User, ws: Workspace) => {
    setCurrentUser(user);
    setActiveWs(ws);
    queryClient.invalidateQueries({ queryKey: ["sessions-list"] });
  };

  const { data: sessions = [] } = useQuery({
    queryKey: ["sessions-list", activeWorkspace?.id],
    queryFn: () => fetchSessions(25),
    staleTime: 1000 * 30,
  });

  const filteredSessions = sessions.filter((s) =>
    s.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <aside
      className={`fixed left-0 top-0 h-full bg-surface-container-low z-50 flex flex-col justify-between shadow-[0_1px_8px_rgba(0,0,0,0.04)] border-r border-outline-variant/20 transition-all duration-300 ${
        isCollapsed ? "w-16" : "w-64"
      }`}
    >
      <div className="flex flex-col min-h-0">
        {/* Brand & Collapse Header */}
        <div className="h-16 px-space-md flex items-center justify-between shrink-0 border-b border-outline-variant/10">
          <div className="flex items-center gap-space-sm overflow-hidden">
            <img
              alt="Gemini Ambient Spark Logo"
              className="h-8 w-8 object-contain shrink-0"
              src="/assets/gemini-spark.svg"
              onError={(e) => {
                // Fallback to png if svg fails
                (e.target as HTMLImageElement).src = "/assets/gemini-spark.png";
              }}
            />
            {!isCollapsed && (
              <span className="font-headline-md text-headline-md text-on-surface whitespace-nowrap">
                Gemini Data
              </span>
            )}
          </div>
          {onToggleCollapse && (
            <button
              onClick={onToggleCollapse}
              className="w-8 h-8 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors shrink-0"
              type="button"
              title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            >
              <span className="material-symbols-outlined text-[18px]">
                {isCollapsed ? "right_panel_open" : "left_panel_close"}
              </span>
            </button>
          )}
        </div>

        {/* Segmented Mode Switcher Capsule */}
        {!isCollapsed && (
          <div className="px-space-md py-space-xs shrink-0">
            <div className="p-space-xs bg-surface-container rounded-full flex items-center gap-space-xs">
              <button
                onClick={() => onTabChange("canvas")}
                className={`flex-1 py-1 px-space-xs text-center rounded-full font-body-sm text-body-sm transition-all ${
                  currentTab === "canvas"
                    ? "bg-surface-container-highest text-primary font-medium shadow-sm"
                    : "text-on-surface-variant hover:text-on-surface"
                }`}
                type="button"
              >
                Chat AI
              </button>
              <button
                onClick={() => onTabChange("sql")}
                className={`flex-1 py-1 px-space-xs text-center rounded-full font-body-sm text-body-sm transition-all ${
                  currentTab === "sql"
                    ? "bg-surface-container-highest text-primary font-medium shadow-sm"
                    : "text-on-surface-variant hover:text-on-surface"
                }`}
                type="button"
              >
                SQL Lab
              </button>
            </div>
          </div>
        )}

        {/* New Session Button */}
        <div className="px-space-md py-space-sm shrink-0">
          <button
            onClick={onNewSession}
            className={`w-full py-2 rounded-full bg-surface-container-high hover:bg-surface-container-highest text-primary font-body-md text-body-md flex items-center justify-center gap-space-sm transition-all shadow-[0_0_16px_rgba(124,167,255,0.08)] active:scale-95 ${
              isCollapsed ? "px-0" : "px-space-md"
            }`}
            type="button"
            title="New Session"
          >
            <span className="material-symbols-outlined text-[20px]">add</span>
            {!isCollapsed && <span>New Session</span>}
          </button>
        </div>

        {/* Search Bar */}
        {!isCollapsed && (
          <div className="px-space-md py-space-xs shrink-0">
            <div className="w-full py-1.5 px-space-md rounded-full bg-surface-container text-on-surface-variant flex items-center justify-between font-body-sm text-body-sm focus-within:ring-1 focus-within:ring-primary/40">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search analysis..."
                className="bg-transparent text-on-surface placeholder:text-outline focus:outline-none w-full text-body-sm"
              />
              <span className="material-symbols-outlined text-[16px] text-outline ml-1">search</span>
            </div>
          </div>
        )}

        {/* Workspaces Navigation */}
        <div className="px-space-md mt-space-sm flex flex-col gap-1 shrink-0">
          {!isCollapsed && (
            <span className="font-label-caps text-label-caps uppercase tracking-wider text-outline px-space-xs py-1">
              Workspaces
            </span>
          )}
          <nav className="flex flex-col gap-0.5">
            <button
              onClick={() => onTabChange("canvas")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "canvas"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Active Analytics"
            >
              <span className="material-symbols-outlined text-[18px] text-primary shrink-0">
                bubble_chart
              </span>
              {!isCollapsed && <span className="truncate">Active Analytics</span>}
            </button>

            <button
              onClick={() => onTabChange("sql")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "sql"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="SQL & Deep Query"
            >
              <span className="material-symbols-outlined text-[18px] text-tertiary shrink-0">
                terminal
              </span>
              {!isCollapsed && <span className="truncate">SQL & Deep Query</span>}
            </button>

            <button
              onClick={() => onTabChange("mapper")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "mapper"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Schema & Relational Mapper"
            >
              <span className="material-symbols-outlined text-[18px] text-amber-400 shrink-0">
                hub
              </span>
              {!isCollapsed && <span className="truncate">Schema Mapper</span>}
            </button>

            <button
              onClick={() => onTabChange("table")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "table"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Dataset Explorer"
            >
              <span className="material-symbols-outlined text-[18px] text-secondary shrink-0">
                table_chart
              </span>
              {!isCollapsed && <span className="truncate">Dataset Explorer</span>}
            </button>

            <button
              onClick={() => onTabChange("charts")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "charts"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Visualizations"
            >
              <span className="material-symbols-outlined text-[18px] text-primary-fixed shrink-0">
                insert_chart
              </span>
              {!isCollapsed && <span className="truncate">Visualizations</span>}
            </button>

            <button
              onClick={() => onTabChange("diagnostics")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "diagnostics"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Diagnostics & AutoML Studio"
            >
              <span className="material-symbols-outlined text-[18px] text-cyan-400 shrink-0">
                stethoscope
              </span>
              {!isCollapsed && <span className="truncate">Diagnostics & ML</span>}
            </button>

            <button
              onClick={() => onTabChange("reports")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "reports"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Executive Reports & Presentation Studio"
            >
              <span className="material-symbols-outlined text-[18px] text-indigo-400 shrink-0">
                co_present
              </span>
              {!isCollapsed && <span className="truncate">Executive Deck</span>}
            </button>

            <button
              onClick={() => onTabChange("warehouse")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "warehouse"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Enterprise Warehouse & Lakehouse Studio"
            >
              <span className="material-symbols-outlined text-[18px] text-amber-400 shrink-0">
                cloud_sync
              </span>
              {!isCollapsed && <span className="truncate">Warehouse Studio</span>}
            </button>

            <button
              onClick={() => onTabChange("history")}
              className={`flex items-center gap-space-sm px-2.5 py-1.5 rounded-lg text-body-sm transition-colors text-left ${
                currentTab === "history"
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
              }`}
              title="Version History & Rollbacks"
            >
              <span className="material-symbols-outlined text-[18px] text-outline shrink-0">
                history
              </span>
              {!isCollapsed && <span className="truncate">Version History</span>}
            </button>
          </nav>
        </div>

        {/* Recent Sessions List */}
        {!isCollapsed && (
          <div className="px-space-md mt-space-md flex flex-col gap-1 min-h-0 flex-1 overflow-y-auto">
            <span className="font-label-caps text-label-caps uppercase tracking-wider text-outline px-space-xs py-1">
              Recent Sessions
            </span>
            <div className="flex flex-col gap-0.5 pb-2">
              {filteredSessions.length === 0 ? (
                <span className="px-space-xs text-[12px] text-outline italic">No sessions found</span>
              ) : (
                filteredSessions.map((s) => (
                  <button
                    key={s.session_id}
                    onClick={() => onSelectSession?.(s.session_id)}
                    className={`px-2.5 py-1.5 rounded text-body-sm font-body-sm truncate transition-colors text-left w-full ${
                      s.session_id === activeSessionId
                        ? "bg-surface-container-high text-primary font-medium"
                        : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
                    }`}
                    title={s.title}
                  >
                    {s.title}
                  </button>
                ))
              )}
            </div>
          </div>
        )}
      </div>

      {/* Interactive Account & Workspace Widget */}
      <div className="p-space-md bg-surface-container-lowest flex items-center justify-between border-t border-outline-variant/10 shrink-0">
        <button
          type="button"
          onClick={() => setIsTeamDrawerOpen(true)}
          className="flex items-center gap-space-sm overflow-hidden text-left group w-full rounded-lg p-1 -m-1 hover:bg-surface-container transition-colors"
          title="Open Workspace & Team Settings"
        >
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center text-white text-xs font-bold shrink-0 border border-primary/20 shadow-sm">
            {currentUser?.full_name ? currentUser.full_name[0].toUpperCase() : "G"}
          </div>
          {!isCollapsed && (
            <div className="flex flex-col min-w-0 flex-1">
              <span className="font-body-md text-body-md text-on-surface truncate leading-tight font-medium group-hover:text-primary transition-colors">
                {currentUser?.full_name || "Guest Analyst"}
              </span>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="font-label-caps text-[9px] px-1.5 py-0.2 rounded bg-surface-container-high text-tertiary uppercase tracking-wider font-semibold">
                  {activeWorkspace?.role?.toUpperCase() || (currentUser ? "ANALYST" : "DEMO")}
                </span>
                <span className="text-[10px] text-outline truncate max-w-[90px]">
                  {activeWorkspace?.name || "Default Workspace"}
                </span>
              </div>
            </div>
          )}
        </button>

        {!isCollapsed && onOpenSettings && (
          <button
            onClick={onOpenSettings}
            className="p-space-xs rounded-full text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors shrink-0 ml-1"
            type="button"
            title="Settings & Integrations"
          >
            <span className="material-symbols-outlined text-[18px]">settings</span>
          </button>
        )}
      </div>

      {/* Slide-over Team & Workspace Drawer */}
      <TeamDrawer
        isOpen={isTeamDrawerOpen}
        onClose={() => setIsTeamDrawerOpen(false)}
        currentUser={currentUser}
        activeWorkspace={activeWorkspace}
        onWorkspaceChange={handleWorkspaceChange}
        onOpenAuth={() => setIsAuthModalOpen(true)}
      />

      {/* Auth Modal (Login / Signup / Guest) */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={handleAuthSuccess}
      />
    </aside>
  );
};
