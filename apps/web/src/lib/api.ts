import { queryOptions } from "@tanstack/react-query";
import {
  AuthTokens,
  CheckpointSummary,
  DatasetDataResponse,
  FileUploadResponse,
  LoginPayload,
  RevertResponse,
  SchemaResponse,
  SessionDetail,
  SignUpPayload,
  User,
  Workspace,
  WorkspaceMember,
  DataHealthResponse,
  CorrelationMatrixResponse,
  AnomalyReportResponse,
  AutoMLTrainResponse,
  DeckConfigRequest,
  DeckPreviewResponse,
  AIPolishResponse,
  WarehouseConnectorType,
  WarehouseConnectorSummary,
  WarehouseConfigResponse,
  WarehouseConfigRequest,
  WarehouseTestRequest,
  WarehouseTestResponse,
  WarehouseSchemaTreeResponse,
  WarehouseTableListResponse,
  WarehouseTablePreviewResponse,
  WarehouseSyncRequest,
  WarehouseSyncResponse,
} from "./types";

export interface SessionListItem {
  session_id: string;
  title: string;
  active_dataframe_version: string;
  workspace_id?: string;
  created_at: string;
  updated_at: string;
}

// ---------------------------------------------------------------------------
// Token Storage & Workspace Management
// ---------------------------------------------------------------------------

const ACCESS_TOKEN_KEY = "ds_access_token";
const REFRESH_TOKEN_KEY = "ds_refresh_token";
const ACTIVE_WORKSPACE_KEY = "ds_active_workspace";

export function getStoredTokens(): { accessToken: string | null; refreshToken: string | null } {
  return {
    accessToken: localStorage.getItem(ACCESS_TOKEN_KEY),
    refreshToken: localStorage.getItem(REFRESH_TOKEN_KEY),
  };
}

export function setStoredTokens(tokens: {
  access_token: string;
  refresh_token: string;
  active_workspace?: Workspace;
}) {
  localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
  if (tokens.active_workspace) {
    localStorage.setItem(ACTIVE_WORKSPACE_KEY, JSON.stringify(tokens.active_workspace));
  }
}

export function clearStoredTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(ACTIVE_WORKSPACE_KEY);
}

export function getActiveWorkspace(): Workspace | null {
  try {
    const raw = localStorage.getItem(ACTIVE_WORKSPACE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function setActiveWorkspace(ws: Workspace) {
  localStorage.setItem(ACTIVE_WORKSPACE_KEY, JSON.stringify(ws));
}

// ---------------------------------------------------------------------------
// Intercepting Auth Fetch with Automatic Token Refresh
// ---------------------------------------------------------------------------

let isRefreshing = false;
let refreshSubscribers: ((token: string) => void)[] = [];

function onRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token));
  refreshSubscribers = [];
}

export async function authFetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  const { accessToken, refreshToken } = getStoredTokens();
  const activeWs = getActiveWorkspace();

  const headers = new Headers(init?.headers || {});
  if (accessToken && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }
  if (activeWs?.id && !headers.has("X-Workspace-Id")) {
    headers.set("X-Workspace-Id", activeWs.id);
  }

  const response = await fetch(input, { ...init, headers });

  if (response.status === 401 && refreshToken) {
    if (!isRefreshing) {
      isRefreshing = true;
      try {
        const refreshRes = await fetch("/api/v1/auth/refresh", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
        if (refreshRes.ok) {
          const newTokens: AuthTokens = await refreshRes.json();
          setStoredTokens(newTokens);
          isRefreshing = false;
          onRefreshed(newTokens.access_token);
          headers.set("Authorization", `Bearer ${newTokens.access_token}`);
          return fetch(input, { ...init, headers });
        } else {
          clearStoredTokens();
          isRefreshing = false;
          window.dispatchEvent(new Event("auth:unauthorized"));
        }
      } catch {
        clearStoredTokens();
        isRefreshing = false;
        window.dispatchEvent(new Event("auth:unauthorized"));
      }
    } else {
      return new Promise<Response>((resolve) => {
        refreshSubscribers.push((newToken: string) => {
          headers.set("Authorization", `Bearer ${newToken}`);
          resolve(fetch(input, { ...init, headers }));
        });
      });
    }
  }

  return response;
}

// ---------------------------------------------------------------------------
// Authentication API
// ---------------------------------------------------------------------------

export const authApi = {
  async signup(payload: SignUpPayload): Promise<AuthTokens> {
    const res = await fetch("/api/v1/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Registration failed");
    }
    const data: AuthTokens = await res.json();
    setStoredTokens(data);
    return data;
  },

  async login(payload: LoginPayload): Promise<AuthTokens> {
    const res = await fetch("/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Invalid email or password");
    }
    const data: AuthTokens = await res.json();
    setStoredTokens(data);
    return data;
  },

  async logout(): Promise<void> {
    const { refreshToken } = getStoredTokens();
    if (refreshToken) {
      await fetch("/api/v1/auth/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
      }).catch(() => {});
    }
    clearStoredTokens();
    window.dispatchEvent(new Event("auth:logout"));
  },

  async me(): Promise<{ user: User; workspaces: Workspace[] }> {
    const res = await authFetch("/api/v1/auth/me");
    if (!res.ok) throw new Error("Failed to fetch user profile");
    return res.json();
  },
};

// ---------------------------------------------------------------------------
// Workspaces API
// ---------------------------------------------------------------------------

export const workspacesApi = {
  async list(): Promise<Workspace[]> {
    const res = await authFetch("/api/v1/workspaces");
    if (!res.ok) return [];
    return res.json();
  },

  async create(name: string): Promise<Workspace> {
    const res = await authFetch("/api/v1/workspaces", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to create workspace");
    }
    return res.json();
  },

  async listMembers(workspaceId: string): Promise<WorkspaceMember[]> {
    const res = await authFetch(`/api/v1/workspaces/${workspaceId}/members`);
    if (!res.ok) return [];
    return res.json();
  },

  async inviteMember(workspaceId: string, email: string, role: string = "analyst"): Promise<WorkspaceMember> {
    const res = await authFetch(`/api/v1/workspaces/${workspaceId}/members`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, role }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to invite member");
    }
    return res.json();
  },

  async updateRole(workspaceId: string, userId: string, role: string): Promise<WorkspaceMember> {
    const res = await authFetch(`/api/v1/workspaces/${workspaceId}/members/${userId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to update role");
    }
    return res.json();
  },

  async removeMember(workspaceId: string, userId: string): Promise<void> {
    const res = await authFetch(`/api/v1/workspaces/${workspaceId}/members/${userId}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to remove member");
    }
  },
};

// ---------------------------------------------------------------------------
// Sessions & Analytics API
// ---------------------------------------------------------------------------

export async function createSession(title: string = "New Analysis"): Promise<{ session_id: string; title: string }> {
  const res = await authFetch("/api/v1/sessions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error(`Failed to create session: ${res.statusText}`);
  return res.json();
}

export async function fetchSessions(limit: number = 20): Promise<SessionListItem[]> {
  const res = await authFetch(`/api/v1/sessions?limit=${limit}`);
  if (!res.ok) return [];
  return res.json();
}

export async function fetchSession(sessionId: string): Promise<SessionDetail> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}`);
  if (!res.ok) throw new Error(`Failed to fetch session: ${res.statusText}`);
  return res.json();
}

export async function fetchSchema(sessionId: string): Promise<SchemaResponse> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/schema`);
  if (!res.ok) throw new Error(`Failed to fetch schema: ${res.statusText}`);
  return res.json();
}

export async function fetchDatasetData(
  sessionId: string,
  limit: number = 50000,
  versionTag?: string
): Promise<DatasetDataResponse> {
  const url = new URL(`/api/v1/sessions/${sessionId}/dataset`, window.location.origin);
  url.searchParams.set("limit", String(limit));
  if (versionTag) {
    url.searchParams.set("version_tag", versionTag);
  }
  const res = await authFetch(url.toString());
  if (!res.ok) {
    return {
      session_id: sessionId,
      total_rows: 0,
      columns: [],
      rows: [],
      truncated: false,
    };
  }
  return res.json();
}

export async function fetchCheckpoints(sessionId: string): Promise<CheckpointSummary[]> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/checkpoints`);
  if (!res.ok) return [];
  return res.json();
}

export async function revertVersion(sessionId: string, versionTag: string): Promise<RevertResponse> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/revert`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ version_tag: versionTag }),
  });
  if (!res.ok) throw new Error(`Failed to revert version: ${res.statusText}`);
  return res.json();
}

export async function executeCode(sessionId: string, code: string): Promise<{ stdout: string; figures: any[] }> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Execution failed: ${res.statusText}`);
  }
  return res.json();
}

export async function executeSqlQuery(
  sessionId: string,
  sql: string,
  limit: number = 1000
): Promise<import("./types").SqlQueryResponse> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/sql`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sql, limit }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `SQL execution failed: ${res.statusText}`);
  }
  return res.json();
}

export async function saveSqlCheckpoint(
  sessionId: string,
  sql: string,
  versionTag?: string,
  summary?: string
): Promise<{ status: string; version_tag: string; message: string; row_count: number; column_count: number }> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/sql/save-checkpoint`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sql, version_tag: versionTag, summary }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Failed to save checkpoint: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchTableRelations(
  sessionId: string
): Promise<import("./types").SessionRelationsResponse> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/relations`);
  if (!res.ok) {
    return { session_id: sessionId, tables: [], relations: [] };
  }
  return res.json();
}

export async function fetchConnectorsStatus(): Promise<import("./types").ConnectorsStatusResponse> {
  const res = await authFetch("/api/v1/connectors/status");
  if (!res.ok) {
    return {
      bigquery: { name: "Google BigQuery", type: "bigquery", configured: false, supported_features: [] },
      snowflake: { name: "Snowflake Data Cloud", type: "snowflake", configured: false, supported_features: [] },
    };
  }
  return res.json();
}

export async function importWarehouseDataset(
  sessionId: string,
  connectorType: string,
  query: string,
  tableName: string
): Promise<FileUploadResponse> {
  const res = await authFetch(`/api/v1/sessions/${sessionId}/connectors/${connectorType}/import`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, table_name: tableName }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Warehouse import failed: ${res.statusText}`);
  }
  return res.json();
}

export async function uploadDataset(sessionId: string, file: File): Promise<FileUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await authFetch(`/api/v1/sessions/${sessionId}/files/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Upload failed: ${res.statusText}`);
  }
  return res.json();
}

export function getExportUrl(sessionId: string, format: string): string {
  return `/api/v1/sessions/${sessionId}/export/${format}`;
}

export async function fetchProvidersStatus(): Promise<{ active_provider: string; providers: Record<string, any> }> {
  const res = await authFetch("/api/v1/system/providers");
  if (!res.ok) {
    return { active_provider: "mock", providers: {} };
  }
  return res.json();
}

export const revertSessionVersion = revertVersion;
export const executeSql = executeSqlQuery;

// ---------------------------------------------------------------------------
// Diagnostics & AutoML API (Track B)
// ---------------------------------------------------------------------------

export const diagnosticsApi = {
  async getHealth(sessionId: string): Promise<DataHealthResponse> {
    const res = await authFetch(`/api/v1/sessions/${sessionId}/diagnostics/health`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to compute data health");
    }
    return res.json();
  },

  async applyHygiene(
    sessionId: string,
    payload: {
      recommendation_id: string;
      action: string;
      column?: string | null;
      parameters?: Record<string, any>;
    }
  ): Promise<{ status: string; checkpoint: CheckpointSummary; profile: any; applied_code: string; message: string }> {
    const res = await authFetch(`/api/v1/sessions/${sessionId}/diagnostics/hygiene/apply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to apply hygiene remediation");
    }
    return res.json();
  },

  async getCorrelations(sessionId: string): Promise<CorrelationMatrixResponse> {
    const res = await authFetch(`/api/v1/sessions/${sessionId}/diagnostics/correlations`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to fetch correlation matrix");
    }
    return res.json();
  },

  async getAnomalies(
    sessionId: string,
    contamination: number = 0.05,
    maxRecords: number = 50
  ): Promise<AnomalyReportResponse> {
    const res = await authFetch(
      `/api/v1/sessions/${sessionId}/diagnostics/anomalies?contamination=${contamination}&max_records=${maxRecords}`
    );
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to run anomaly detection");
    }
    return res.json();
  },

  async trainAutoML(
    sessionId: string,
    payload: {
      target_column: string;
      problem_type?: string;
      selected_features?: string[];
      max_rows?: number;
    }
  ): Promise<AutoMLTrainResponse> {
    const res = await authFetch(`/api/v1/sessions/${sessionId}/automl/train`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "AutoML training failed");
    }
    return res.json();
  },
};

// ---------------------------------------------------------------------------
// TanStack Query Options
// ---------------------------------------------------------------------------

export const sessionQueryOptions = (sessionId: string) =>
  queryOptions({
    queryKey: ["session", sessionId],
    queryFn: () => fetchSession(sessionId),
  });

export const schemaQueryOptions = (sessionId: string) =>
  queryOptions({
    queryKey: ["schema", sessionId],
    queryFn: () => fetchSchema(sessionId),
  });

export const checkpointsQueryOptions = (sessionId: string) =>
  queryOptions({
    queryKey: ["checkpoints", sessionId],
    queryFn: () => fetchCheckpoints(sessionId),
  });

export const diagnosticsHealthQueryOptions = (sessionId: string) =>
  queryOptions({
    queryKey: ["diagnostics", "health", sessionId],
    queryFn: () => diagnosticsApi.getHealth(sessionId),
    staleTime: 30000,
  });

export const diagnosticsCorrelationsQueryOptions = (sessionId: string) =>
  queryOptions({
    queryKey: ["diagnostics", "correlations", sessionId],
    queryFn: () => diagnosticsApi.getCorrelations(sessionId),
    staleTime: 60000,
  });

export const diagnosticsAnomaliesQueryOptions = (sessionId: string) =>
  queryOptions({
    queryKey: ["diagnostics", "anomalies", sessionId],
    queryFn: () => diagnosticsApi.getAnomalies(sessionId),
    staleTime: 60000,
  });

// ---------------------------------------------------------------------------
// Reports & Presentation Studio API (Track C)
// ---------------------------------------------------------------------------

export const reportsApi = {
  async getDeckPreview(sessionId: string, theme: string = "dark"): Promise<DeckPreviewResponse> {
    const res = await authFetch(`/api/v1/sessions/${sessionId}/reports/preview?theme=${theme}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to load deck preview");
    }
    return res.json();
  },

  async requestAIPolish(sessionId: string, slideId: string): Promise<AIPolishResponse> {
    const res = await authFetch(`/api/v1/sessions/${sessionId}/reports/polish`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ slide_id: slideId }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to generate AI executive polish");
    }
    return res.json();
  },

  async downloadDeckPptx(sessionId: string, config?: DeckConfigRequest): Promise<void> {
    const tokens = getStoredTokens();
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (tokens?.access_token) {
      headers["Authorization"] = `Bearer ${tokens.access_token}`;
    }

    const res = await fetch(`/api/v1/sessions/${sessionId}/reports/export/pptx`, {
      method: "POST",
      headers,
      body: JSON.stringify(config || {}),
    });
    if (!res.ok) throw new Error("Failed to export PowerPoint presentation");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${sessionId}_presentation.pptx`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
  },

  async downloadReportPdf(sessionId: string, title?: string): Promise<void> {
    const tokens = getStoredTokens();
    const headers: Record<string, string> = {};
    if (tokens?.access_token) {
      headers["Authorization"] = `Bearer ${tokens.access_token}`;
    }

    const params = new URLSearchParams();
    if (title) params.set("title", title);

    const res = await fetch(`/api/v1/sessions/${sessionId}/reports/export/pdf?${params.toString()}`, {
      method: "POST",
      headers,
    });
    if (!res.ok) throw new Error("Failed to export PDF brief");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${sessionId}_brief.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
  },
};

export const reportsPreviewQueryOptions = (sessionId: string, theme: string = "dark") =>
  queryOptions({
    queryKey: ["reports", "preview", sessionId, theme],
    queryFn: () => reportsApi.getDeckPreview(sessionId, theme),
    staleTime: 30000,
  });

// ---------------------------------------------------------------------------
// Warehouse & Lakehouse Connectors Studio API (Track F)
// ---------------------------------------------------------------------------

export const warehouseApi = {
  async getConnectors(): Promise<WarehouseConnectorSummary[]> {
    const res = await authFetch("/api/v1/connectors");
    if (!res.ok) {
      throw new Error(`Failed to load warehouse connectors: ${res.statusText}`);
    }
    return res.json();
  },

  async testConnection(req: WarehouseTestRequest): Promise<WarehouseTestResponse> {
    const res = await authFetch("/api/v1/connectors/test", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Connection test failed");
    }
    return res.json();
  },

  async saveConfig(req: WarehouseConfigRequest): Promise<WarehouseConfigResponse> {
    const res = await authFetch("/api/v1/connectors/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to save warehouse credentials");
    }
    return res.json();
  },

  async getConfigs(connectorType: WarehouseConnectorType): Promise<WarehouseConfigResponse[]> {
    const res = await authFetch(`/api/v1/connectors/config/${connectorType}`);
    if (!res.ok) {
      return [];
    }
    return res.json();
  },

  async deleteConfig(configId: string): Promise<void> {
    const res = await authFetch(`/api/v1/connectors/config/${configId}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      throw new Error("Failed to delete warehouse config");
    }
  },

  async getSchemas(connectorType: WarehouseConnectorType): Promise<WarehouseSchemaTreeResponse> {
    const res = await authFetch(`/api/v1/connectors/${connectorType}/schemas`);
    if (!res.ok) {
      throw new Error(`Failed to load schemas for ${connectorType}`);
    }
    return res.json();
  },

  async getTables(connectorType: WarehouseConnectorType, schemaName: string): Promise<WarehouseTableListResponse> {
    const res = await authFetch(`/api/v1/connectors/${connectorType}/schemas/${schemaName}/tables`);
    if (!res.ok) {
      throw new Error(`Failed to load tables for ${schemaName}`);
    }
    return res.json();
  },

  async previewTable(
    connectorType: WarehouseConnectorType,
    schemaName: string,
    tableName: string,
    limit: number = 50
  ): Promise<WarehouseTablePreviewResponse> {
    const res = await authFetch(
      `/api/v1/connectors/${connectorType}/schemas/${schemaName}/tables/${tableName}/preview?limit=${limit}`
    );
    if (!res.ok) {
      throw new Error(`Failed to preview table ${tableName}`);
    }
    return res.json();
  },

  async syncData(
    connectorType: WarehouseConnectorType,
    sessionId: string,
    req: WarehouseSyncRequest
  ): Promise<WarehouseSyncResponse> {
    const res = await authFetch(`/api/v1/connectors/${connectorType}/sync/${sessionId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Failed to sync warehouse data into session`);
    }
    return res.json();
  },
};

export const warehouseConnectorsQueryOptions = () =>
  queryOptions({
    queryKey: ["warehouse", "connectors"],
    queryFn: () => warehouseApi.getConnectors(),
    staleTime: 10000,
  });

export const warehouseSchemasQueryOptions = (connectorType: WarehouseConnectorType) =>
  queryOptions({
    queryKey: ["warehouse", "schemas", connectorType],
    queryFn: () => warehouseApi.getSchemas(connectorType),
    staleTime: 30000,
  });

export const warehouseTablesQueryOptions = (connectorType: WarehouseConnectorType, schemaName: string) =>
  queryOptions({
    queryKey: ["warehouse", "tables", connectorType, schemaName],
    queryFn: () => warehouseApi.getTables(connectorType, schemaName),
    enabled: Boolean(schemaName),
    staleTime: 30000,
  });

export const warehousePreviewQueryOptions = (
  connectorType: WarehouseConnectorType,
  schemaName: string,
  tableName: string
) =>
  queryOptions({
    queryKey: ["warehouse", "preview", connectorType, schemaName, tableName],
    queryFn: () => warehouseApi.previewTable(connectorType, schemaName, tableName),
    enabled: Boolean(schemaName && tableName),
    staleTime: 30000,
  });


