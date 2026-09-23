export interface ColumnProfile {
  name: string;
  dtype: string;
  null_count: number;
  null_percentage: number;
  cardinality: number;
  sample_values: any[];
}

export interface DataFrameProfile {
  session_id: string;
  table_name: string;
  version_tag: string;
  row_count: number;
  column_count: number;
  memory_footprint_mb: number;
  columns: ColumnProfile[];
  head_preview_markdown: string;
}

export interface SessionDetail {
  session_id: string;
  title: string;
  active_dataframe_version: string;
  created_at: string;
  updated_at: string;
  files: {
    id: string;
    filename: string;
    size_bytes: number;
    mime_type: string;
    created_at: string;
  }[];
}

export interface ReflexionStep {
  attempt: number;
  error: string;
  status: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  thought?: string;
  code?: string;
  stdout?: string;
  status?: "generating_code" | "running_sandbox" | "synthesizing_insights" | "complete" | "error";
  figures?: any[];
  reflexionSteps?: ReflexionStep[];
  durationMs?: number;
  activeVersion?: string;
}

export interface SchemaResponse {
  session_id: string;
  active_version: string;
  table_count: number;
  profiles: DataFrameProfile[];
}

export interface FileUploadResponse {
  file_id: string;
  filename: string;
  size_bytes: number;
  mime_type: string;
  storage_path: string;
  profiles: DataFrameProfile[];
  status: string;
}

export interface ColumnDiff {
  name: string;
  diff_type: "added" | "removed" | "modified";
  old_dtype?: string;
  new_dtype?: string;
}

export interface SchemaDiff {
  row_delta: number;
  column_delta: number;
  columns_added: string[];
  columns_removed: string[];
  columns_modified: ColumnDiff[];
}

export interface CheckpointSummary {
  id: string;
  session_id: string;
  version_tag: string;
  operation_summary: string;
  row_count: number;
  column_count: number;
  memory_bytes: number;
  created_at: string;
  is_active: boolean;
  diff_from_previous?: SchemaDiff | null;
}

export interface RevertResponse {
  status: string;
  session_id: string;
  active_version: string;
  profile: DataFrameProfile;
  message: string;
}

export interface DatasetColumn {
  name: string;
  type: string;
}

export interface DatasetDataResponse {
  session_id: string;
  total_rows: number;
  columns: DatasetColumn[];
  rows: Record<string, any>[];
  truncated: boolean;
}

export interface DatasetEventPayload {
  session_id: string;
  total_rows: number;
  columns: DatasetColumn[];
  rows: Record<string, any>[];
  truncated: boolean;
}

export interface SqlQueryColumn {
  name: string;
  type: string;
}

export interface SqlQueryResponse {
  status: "success" | "error";
  session_id: string;
  sql: string;
  columns: SqlQueryColumn[];
  rows: Record<string, any>[];
  total_rows: number;
  execution_time_ms: number;
  error?: string | null;
}

export interface ForeignKeyRelation {
  from_table: string;
  from_column: string;
  to_table: string;
  to_column: string;
  confidence: number;
  suggested_join_type: "INNER JOIN" | "LEFT JOIN" | "RIGHT JOIN" | "FULL OUTER JOIN";
}

export interface SessionRelationsResponse {
  session_id: string;
  tables: string[];
  relations: ForeignKeyRelation[];
}

export interface WarehouseConnectorStatus {
  name: string;
  type: string;
  configured: boolean;
  project_id?: string;
  account?: string;
  database?: string;
  warehouse?: string;
  supported_features: string[];
}

export interface ConnectorsStatusResponse {
  bigquery: WarehouseConnectorStatus;
  snowflake: WarehouseConnectorStatus;
  [key: string]: WarehouseConnectorStatus;
}

// ---------------------------------------------------------------------------
// Enterprise Security & Multi-Tenancy Types
// ---------------------------------------------------------------------------

export type WorkspaceRole = "owner" | "admin" | "analyst" | "viewer";

export interface User {
  id: string;
  email: string;
  full_name: string;
  avatar_url?: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface Workspace {
  id: string;
  name: string;
  slug: string;
  plan_tier: "free" | "pro" | "enterprise";
  role: WorkspaceRole;
  created_at: string;
}

export interface WorkspaceMember {
  id: string;
  workspace_id: string;
  user_id: string;
  email: string;
  full_name: string;
  role: WorkspaceRole;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
  active_workspace: Workspace;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface SignUpPayload {
  email: string;
  password: string;
  full_name?: string;
}

// ---------------------------------------------------------------------------
// Diagnostics & AutoML Types (Track B)
// ---------------------------------------------------------------------------

export interface HealthScoreBreakdown {
  completeness_score: number;
  uniqueness_score: number;
  consistency_score: number;
  outlier_score: number;
  missing_cells: number;
  total_cells: number;
  duplicate_rows: number;
  total_rows: number;
}

export interface ColumnHealth {
  name: string;
  dtype: string;
  missing_count: number;
  missing_ratio: number;
  unique_count: number;
  unique_ratio: number;
  outlier_count: number;
  score: number;
  status: "excellent" | "good" | "fair" | "poor";
}

export interface HygieneRecommendation {
  id: string;
  category: "missing_values" | "duplicates" | "outliers" | "constants" | "skewness";
  severity: "critical" | "warning" | "info";
  column?: string | null;
  title: string;
  description: string;
  suggested_action: string;
  parameters: Record<string, any>;
  python_code: string;
}

export interface DataHealthResponse {
  session_id: string;
  overall_score: number;
  status: "healthy" | "warning" | "critical";
  breakdown: HealthScoreBreakdown;
  columns: ColumnHealth[];
  recommendations: HygieneRecommendation[];
}

export interface CorrelationPair {
  col1: string;
  col2: string;
  pearson: number;
  spearman: number;
  abs_pearson: number;
}

export interface CorrelationMatrixResponse {
  session_id: string;
  columns: string[];
  pearson: number[][];
  spearman: number[][];
  top_correlations: CorrelationPair[];
}

export interface AnomalyAttribution {
  column: string;
  value: any;
  z_score: number;
}

export interface AnomalyRecord {
  row_index: number;
  anomaly_score: number;
  is_outlier: boolean;
  data: Record<string, any>;
  top_attributions: AnomalyAttribution[];
}

export interface AnomalyReportResponse {
  session_id: string;
  total_rows: number;
  anomaly_count: number;
  anomaly_rate: number;
  features_analyzed: string[];
  top_anomalies: AnomalyRecord[];
}

export interface ModelBenchmarkResult {
  model_name: string;
  display_name: string;
  is_best: boolean;
  metrics: Record<string, number>;
  training_time_ms: number;
}

export interface FeatureImportanceItem {
  feature: string;
  importance: number;
}

export interface ConfusionMatrixData {
  labels: string[];
  matrix: number[][];
}

export interface AutoMLTrainResponse {
  session_id: string;
  target_column: string;
  problem_type: "binary" | "multiclass" | "regression";
  best_model: string;
  models: ModelBenchmarkResult[];
  feature_importances: FeatureImportanceItem[];
  confusion_matrix?: ConfusionMatrixData | null;
  generated_code: string;
  rows_trained: number;
}


