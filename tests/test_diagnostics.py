"""
Unit and integration tests for Autonomous Diagnostic Engine (Track B).
Tests data health scoring, smart hygiene rule detection, correlation matrices,
and Isolation Forest anomaly detection.
"""
import numpy as np
import pandas as pd
import pytest

from services.api.diagnostics import (
    compute_anomalies,
    compute_correlation_matrix,
    compute_data_health,
)


def test_clean_dataframe_health():
    """A pristine dataset should receive a near-100% health score and 0 critical recommendations."""
    np.random.seed(42)
    df = pd.DataFrame({
        "age": np.random.randint(20, 60, size=100),
        "salary": np.random.normal(50000, 5000, size=100),
        "department": np.random.choice(["Sales", "Engineering", "Marketing"], size=100),
    })

    res = compute_data_health(df, session_id="test_session")
    assert res.overall_score >= 85.0
    assert res.status == "healthy"
    assert res.breakdown.missing_cells == 0
    assert res.breakdown.duplicate_rows == 0
    assert len(res.columns) == 3


def test_dirty_dataframe_health_and_recommendations():
    """A dataset with missing values, duplicate rows, and constant columns triggers actionable recommendations."""
    df = pd.DataFrame({
        "id": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "constant_col": ["fixed"] * 10,
        "missing_numeric": [10.0, 10.0, np.nan, np.nan, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0],
        "category": ["A", "A", "B", "B", "C", "C", "D", "E", "F", "G"],
    })

    res = compute_data_health(df, session_id="dirty_session")
    assert res.overall_score < 80.0
    assert res.breakdown.missing_cells == 2
    assert res.breakdown.duplicate_rows >= 1

    # Check recommendations
    actions = [r.suggested_action for r in res.recommendations]
    assert "drop_duplicates" in actions
    assert "drop_column" in actions
    assert "impute_median" in actions


def test_correlation_matrix_computation():
    """Verifies Pearson and Spearman correlation matrices and top ranked pairs."""
    np.random.seed(42)
    x = np.linspace(1, 100, 100)
    y = 2.5 * x + np.random.normal(0, 5, 100)  # Strong positive correlation
    z = -1.8 * x + np.random.normal(0, 5, 100)  # Strong negative correlation
    w = np.random.normal(0, 1, 100)  # Uncorrelated

    df = pd.DataFrame({"x": x, "y": y, "z": z, "w": w})
    res = compute_correlation_matrix(df, session_id="corr_session")

    assert len(res.columns) == 4
    assert len(res.pearson) == 4
    assert len(res.spearman) == 4
    assert len(res.top_correlations) > 0

    # Top correlation should be x & y or x & z (magnitude > 0.9)
    top = res.top_correlations[0]
    assert top.abs_pearson > 0.90


def test_isolation_forest_anomaly_detection():
    """Verifies unsupervised anomaly detection flags injected extreme outliers with feature attribution."""
    np.random.seed(42)
    # Generate 100 normal observations
    n = 100
    df = pd.DataFrame({
        "feature_a": np.random.normal(10, 2, n),
        "feature_b": np.random.normal(50, 5, n),
    })

    # Inject 2 severe outliers
    df.loc[98, "feature_a"] = 999.0
    df.loc[99, "feature_b"] = -888.0

    res = compute_anomalies(df, session_id="anomaly_session", contamination=0.05, max_records=10)
    assert res.anomaly_count > 0
    assert len(res.top_anomalies) > 0

    # Top anomalies should include row 98 or 99
    top_indices = [rec.row_index for rec in res.top_anomalies[:3]]
    assert 98 in top_indices or 99 in top_indices

    # Check feature attribution
    top_rec = res.top_anomalies[0]
    assert len(top_rec.top_attributions) > 0
    assert abs(top_rec.top_attributions[0].z_score) > 2.0
