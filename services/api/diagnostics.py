"""
Autonomous Diagnostic Engine for Conversational Data Platform.
Provides data health scoring, smart hygiene rule detection, correlation analysis,
and unsupervised Isolation Forest anomaly detection.
"""
from __future__ import annotations

import logging
import math
import uuid
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest

from services.api.models import (
    AnomalyAttribution,
    AnomalyRecord,
    AnomalyReportResponse,
    ColumnHealth,
    CorrelationMatrixResponse,
    CorrelationPair,
    DataHealthResponse,
    HealthScoreBreakdown,
    HygieneRecommendation,
)

logger = logging.getLogger(__name__)


def compute_data_health(df: pd.DataFrame, session_id: str) -> DataHealthResponse:
    """
    Computes a multi-dimensional health score (0-100) and actionable hygiene recommendations
    for an active pandas DataFrame.
    """
    total_rows = len(df)
    total_cols = len(df.columns)
    total_cells = total_rows * total_cols

    if total_rows == 0 or total_cols == 0:
        return DataHealthResponse(
            session_id=session_id,
            overall_score=100.0,
            status="healthy",
            breakdown=HealthScoreBreakdown(
                completeness_score=100.0,
                uniqueness_score=100.0,
                consistency_score=100.0,
                outlier_score=100.0,
                missing_cells=0,
                total_cells=0,
                duplicate_rows=0,
                total_rows=0,
            ),
            columns=[],
            recommendations=[],
        )

    # 1. Completeness Dimension
    missing_series = df.isna().sum()
    missing_cells = int(missing_series.sum())
    completeness_score = max(0.0, min(100.0, round(100.0 * (1.0 - (missing_cells / max(total_cells, 1))), 2)))

    # 2. Uniqueness Dimension
    try:
        duplicate_rows = int(df.duplicated().sum())
    except Exception:
        duplicate_rows = 0
    uniqueness_score = max(0.0, min(100.0, round(100.0 * (1.0 - (duplicate_rows / max(total_rows, 1))), 2)))

    # 3. Column Health & Consistency & Outlier Score
    columns_health: List[ColumnHealth] = []
    recommendations: List[HygieneRecommendation] = []
    outlier_rows_set = set()
    inconsistent_col_count = 0

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in df.columns:
        series = df[col]
        n_missing = int(series.isna().sum())
        missing_ratio = round(float(n_missing / max(total_rows, 1)), 4)
        n_unique = int(series.nunique(dropna=True))
        unique_ratio = round(float(n_unique / max(total_rows, 1)), 4)
        dtype_str = str(series.dtype)

        n_outliers = 0
        is_numeric = col in numeric_cols

        if is_numeric and total_rows >= 5:
            clean_s = series.dropna()
            if len(clean_s) >= 5:
                q25 = clean_s.quantile(0.25)
                q75 = clean_s.quantile(0.75)
                iqr = q75 - q25
                if iqr > 0:
                    lower_bound = q25 - (1.5 * iqr)
                    upper_bound = q75 + (1.5 * iqr)
                    outlier_mask = (clean_s < lower_bound) | (clean_s > upper_bound)
                    outlier_indices = clean_s[outlier_mask].index.tolist()
                    n_outliers = len(outlier_indices)
                    outlier_rows_set.update(outlier_indices)

        # Column quality score
        penalties = 0.0
        penalties += min(50.0, missing_ratio * 70.0)
        if total_rows > 1 and n_unique == 1:
            penalties += 25.0  # Constant column
        if total_rows > 1 and n_outliers > 0:
            outlier_ratio = n_outliers / total_rows
            penalties += min(30.0, outlier_ratio * 60.0)

        col_score = max(0.0, min(100.0, round(100.0 - penalties, 1)))

        if col_score >= 85.0:
            col_status = "excellent"
        elif col_score >= 70.0:
            col_status = "good"
        elif col_score >= 50.0:
            col_status = "fair"
        else:
            col_status = "poor"

        columns_health.append(
            ColumnHealth(
                name=str(col),
                dtype=dtype_str,
                missing_count=n_missing,
                missing_ratio=missing_ratio,
                unique_count=n_unique,
                unique_ratio=unique_ratio,
                outlier_count=n_outliers,
                score=col_score,
                status=col_status,
            )
        )

        # Hygiene Rule: Missing Values
        if n_missing > 0:
            pct = round(missing_ratio * 100, 1)
            if missing_ratio > 0.70:
                rec_id = f"drop_missing_col_{col}_{uuid.uuid4().hex[:4]}"
                recommendations.append(
                    HygieneRecommendation(
                        id=rec_id,
                        category="missing_values",
                        severity="critical",
                        column=str(col),
                        title=f"Drop high-null column '{col}'",
                        description=f"Column '{col}' has {n_missing} missing values ({pct}%). Pruning sparse columns prevents model degradation.",
                        suggested_action="drop_column",
                        parameters={"column": str(col)},
                        python_code=f"df = df.drop(columns=['{col}'])",
                    )
                )
            elif is_numeric:
                rec_id = f"impute_median_{col}_{uuid.uuid4().hex[:4]}"
                recommendations.append(
                    HygieneRecommendation(
                        id=rec_id,
                        category="missing_values",
                        severity="warning" if missing_ratio > 0.15 else "info",
                        column=str(col),
                        title=f"Impute numeric nulls in '{col}' with Median",
                        description=f"Column '{col}' has {n_missing} nulls ({pct}%). Median imputation preserves distribution without outlier distortion.",
                        suggested_action="impute_median",
                        parameters={"column": str(col)},
                        python_code=f"df['{col}'] = df['{col}'].fillna(df['{col}'].median())",
                    )
                )
            else:
                rec_id = f"impute_mode_{col}_{uuid.uuid4().hex[:4]}"
                recommendations.append(
                    HygieneRecommendation(
                        id=rec_id,
                        category="missing_values",
                        severity="warning" if missing_ratio > 0.15 else "info",
                        column=str(col),
                        title=f"Impute categorical nulls in '{col}' with Mode",
                        description=f"Column '{col}' has {n_missing} nulls ({pct}%). Mode imputation fills with most frequent category.",
                        suggested_action="impute_mode",
                        parameters={"column": str(col)},
                        python_code=f"df['{col}'] = df['{col}'].fillna(df['{col}'].mode()[0] if not df['{col}'].mode().empty else 'Unknown')",
                    )
                )

        # Hygiene Rule: Constant Column (zero variance)
        if total_rows > 1 and n_unique == 1:
            rec_id = f"drop_constant_{col}_{uuid.uuid4().hex[:4]}"
            recommendations.append(
                HygieneRecommendation(
                    id=rec_id,
                    category="constants",
                    severity="warning",
                    column=str(col),
                    title=f"Remove constant column '{col}'",
                    description=f"Column '{col}' only contains 1 unique value across all rows. It provides zero analytical or predictive value.",
                    suggested_action="drop_column",
                    parameters={"column": str(col)},
                    python_code=f"df = df.drop(columns=['{col}'])",
                )
            )

        # Hygiene Rule: Outlier clipping
        if is_numeric and n_outliers > 0 and (n_outliers / total_rows) >= 0.03:
            rec_id = f"clip_outliers_{col}_{uuid.uuid4().hex[:4]}"
            pct = round((n_outliers / total_rows) * 100, 1)
            clean_s = df[col].dropna()
            q01 = float(clean_s.quantile(0.01))
            q99 = float(clean_s.quantile(0.99))
            recommendations.append(
                HygieneRecommendation(
                    id=rec_id,
                    category="outliers",
                    severity="info",
                    column=str(col),
                    title=f"Winsorize outliers in '{col}'",
                    description=f"Found {n_outliers} ({pct}%) extreme values. Clipping to 1st/99th percentiles ({q01:.2f} to {q99:.2f}) stabilizes variance.",
                    suggested_action="clip_outliers",
                    parameters={"column": str(col), "lower": q01, "upper": q99},
                    python_code=f"df['{col}'] = df['{col}'].clip(lower={q01}, upper={q99})",
                )
            )

        # Hygiene Rule: Distribution Skewness
        if is_numeric and total_rows >= 30:
            clean_s = df[col].dropna()
            if len(clean_s) >= 30 and (clean_s > 0).all():
                try:
                    skew_val = float(stats.skew(clean_s))
                    if abs(skew_val) > 2.0:
                        rec_id = f"log_transform_{col}_{uuid.uuid4().hex[:4]}"
                        recommendations.append(
                            HygieneRecommendation(
                                id=rec_id,
                                category="skewness",
                                severity="info",
                                column=str(col),
                                title=f"Log-transform highly skewed column '{col}'",
                                description=f"Skewness is {skew_val:.2f}. Applying log1p transformation will normalize the distribution.",
                                suggested_action="log_transform",
                                parameters={"column": str(col)},
                                python_code=f"import numpy as np\ndf['{col}_log'] = np.log1p(df['{col}'])",
                            )
                        )
                except Exception:
                    pass

    # Hygiene Rule: Duplicate Rows
    if duplicate_rows > 0:
        rec_id = f"drop_duplicates_{uuid.uuid4().hex[:4]}"
        pct = round((duplicate_rows / total_rows) * 100, 1)
        recommendations.append(
            HygieneRecommendation(
                id=rec_id,
                category="duplicates",
                severity="critical" if pct > 5.0 else "warning",
                column=None,
                title=f"Deduplicate {duplicate_rows} redundant rows",
                description=f"Identified {duplicate_rows} exact duplicate rows ({pct}%). Removing duplicates avoids skewed frequencies and data leakage.",
                suggested_action="drop_duplicates",
                parameters={},
                python_code="df = df.drop_duplicates().reset_index(drop=True)",
            )
        )

    # 4. Outlier & Consistency Breakdown Scores
    outlier_ratio = len(outlier_rows_set) / max(total_rows, 1)
    outlier_score = max(0.0, min(100.0, round(100.0 * (1.0 - outlier_ratio), 2)))

    # Consistency score: based on percentage of columns without invalid/constant anomalies
    consistency_score = round(float(np.mean([c.score for c in columns_health])) if columns_health else 100.0, 2)

    # 5. Composite Health Score with Hygiene Penalties
    raw_composite = (
        (0.30 * completeness_score)
        + (0.30 * uniqueness_score)
        + (0.20 * consistency_score)
        + (0.20 * outlier_score)
    )

    rec_penalty = 0.0
    for r in recommendations:
        if r.severity == "critical":
            rec_penalty += 12.0
        elif r.severity == "warning":
            rec_penalty += 6.0
        elif r.severity == "info":
            rec_penalty += 2.0

    overall_score = max(5.0, min(100.0, round(raw_composite - min(40.0, rec_penalty), 1)))

    if overall_score >= 80.0:
        health_status = "healthy"
    elif overall_score >= 60.0:
        health_status = "warning"
    else:
        health_status = "critical"

    # Sort recommendations: critical first, then warning, then info
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    recommendations.sort(key=lambda r: severity_order.get(r.severity, 3))

    return DataHealthResponse(
        session_id=session_id,
        overall_score=overall_score,
        status=health_status,
        breakdown=HealthScoreBreakdown(
            completeness_score=completeness_score,
            uniqueness_score=uniqueness_score,
            consistency_score=consistency_score,
            outlier_score=outlier_score,
            missing_cells=missing_cells,
            total_cells=total_cells,
            duplicate_rows=duplicate_rows,
            total_rows=total_rows,
        ),
        columns=columns_health,
        recommendations=recommendations,
    )


def compute_correlation_matrix(df: pd.DataFrame, session_id: str) -> CorrelationMatrixResponse:
    """
    Computes Pearson (linear) and Spearman (rank) correlation matrices for numeric features,
    along with ranked pairwise associations.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    numeric_cols = [str(c) for c in numeric_df.columns if numeric_df[c].nunique(dropna=True) > 1]

    if len(numeric_cols) < 2:
        return CorrelationMatrixResponse(
            session_id=session_id,
            columns=numeric_cols,
            pearson=[],
            spearman=[],
            top_correlations=[],
        )

    clean_numeric = numeric_df[numeric_cols].copy()

    # Impute temporarily for clean correlations if nulls exist
    for col in numeric_cols:
        if clean_numeric[col].isna().any():
            clean_numeric[col] = clean_numeric[col].fillna(clean_numeric[col].median())

    pearson_mat = clean_numeric.corr(method="pearson").fillna(0.0).round(4)
    spearman_mat = clean_numeric.corr(method="spearman").fillna(0.0).round(4)

    # Extract top pairwise correlations (symmetric unique pairs)
    top_pairs: List[CorrelationPair] = []
    n = len(numeric_cols)
    for i in range(n):
        for j in range(i + 1, n):
            c1 = numeric_cols[i]
            c2 = numeric_cols[j]
            p_val = float(pearson_mat.loc[c1, c2])
            s_val = float(spearman_mat.loc[c1, c2])
            if not math.isnan(p_val) and not math.isnan(s_val):
                top_pairs.append(
                    CorrelationPair(
                        col1=c1,
                        col2=c2,
                        pearson=round(p_val, 4),
                        spearman=round(s_val, 4),
                        abs_pearson=round(abs(p_val), 4),
                    )
                )

    top_pairs.sort(key=lambda x: x.abs_pearson, reverse=True)

    return CorrelationMatrixResponse(
        session_id=session_id,
        columns=numeric_cols,
        pearson=pearson_mat.values.tolist(),
        spearman=spearman_mat.values.tolist(),
        top_correlations=top_pairs[:20],
    )


def compute_anomalies(
    df: pd.DataFrame,
    session_id: str,
    contamination: float = 0.05,
    max_records: int = 50,
) -> AnomalyReportResponse:
    """
    Performs unsupervised multivariate anomaly detection with Isolation Forest
    plus univariate Z-score feature attributions.
    """
    total_rows = len(df)
    numeric_df = df.select_dtypes(include=[np.number])
    valid_cols = [str(c) for c in numeric_df.columns if numeric_df[c].nunique(dropna=True) > 1]

    if total_rows < 10 or len(valid_cols) < 1:
        return AnomalyReportResponse(
            session_id=session_id,
            total_rows=total_rows,
            anomaly_count=0,
            anomaly_rate=0.0,
            features_analyzed=valid_cols,
            top_anomalies=[],
        )

    # Prepare feature matrix with median imputation for NaN
    X = numeric_df[valid_cols].copy()
    col_means = {}
    col_stds = {}
    for col in valid_cols:
        median_val = X[col].median()
        mean_val = float(X[col].mean()) if not pd.isna(X[col].mean()) else 0.0
        std_val = float(X[col].std()) if not pd.isna(X[col].std()) and X[col].std() > 0 else 1.0
        col_means[col] = mean_val
        col_stds[col] = std_val
        X[col] = X[col].fillna(median_val if not pd.isna(median_val) else 0.0)

    # Fit Isolation Forest
    model = IsolationForest(
        contamination=min(max(contamination, 0.01), 0.20),
        random_state=42,
        n_estimators=100,
        n_jobs=-1,
    )
    preds = model.fit_predict(X)  # -1 is outlier, 1 is inlier
    raw_scores = model.score_samples(X)  # lower = more abnormal

    # Normalize scores between 0 (most normal) and 1 (most anomalous)
    min_s = float(raw_scores.min())
    max_s = float(raw_scores.max())
    score_range = max(max_s - min_s, 1e-6)
    anomaly_scores = [round(float(1.0 - ((s - min_s) / score_range)), 4) for s in raw_scores]

    is_outlier_list = [bool(p == -1) for p in preds]
    anomaly_count = sum(is_outlier_list)
    anomaly_rate = round(float(anomaly_count / total_rows), 4)

    # Build top anomalous records
    indexed_scores = [(idx, anomaly_scores[idx], is_outlier_list[idx]) for idx in range(total_rows)]
    indexed_scores.sort(key=lambda x: x[1], reverse=True)

    top_records: List[AnomalyRecord] = []
    for orig_idx, score, is_outlier in indexed_scores[:max_records]:
        row_series = df.iloc[orig_idx]
        row_dict: Dict[str, Any] = {}
        for k, v in row_series.items():
            if pd.isna(v):
                row_dict[str(k)] = None
            elif isinstance(v, (np.integer, int)):
                row_dict[str(k)] = int(v)
            elif isinstance(v, (np.floating, float)):
                row_dict[str(k)] = round(float(v), 4)
            else:
                row_dict[str(k)] = str(v)

        # Feature attributions via Z-score
        attributions: List[AnomalyAttribution] = []
        for col in valid_cols:
            val = X[col].iloc[orig_idx]
            z = (val - col_means[col]) / col_stds[col]
            if abs(z) >= 1.5:
                attributions.append(
                    AnomalyAttribution(
                        column=col,
                        value=row_dict.get(col),
                        z_score=round(float(z), 2),
                    )
                )

        attributions.sort(key=lambda a: abs(a.z_score), reverse=True)

        top_records.append(
            AnomalyRecord(
                row_index=orig_idx,
                anomaly_score=score,
                is_outlier=is_outlier,
                data=row_dict,
                top_attributions=attributions[:5],
            )
        )

    return AnomalyReportResponse(
        session_id=session_id,
        total_rows=total_rows,
        anomaly_count=anomaly_count,
        anomaly_rate=anomaly_rate,
        features_analyzed=valid_cols,
        top_anomalies=top_records,
    )
