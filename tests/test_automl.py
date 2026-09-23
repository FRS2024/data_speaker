"""
Unit and integration tests for Autonomous AutoML Baseline Engine (Track B).
Tests problem type detection, classification/regression training,
metrics leaderboard, confusion matrix, feature importances, and code generation.
"""
import ast
import numpy as np
import pandas as pd
import pytest

from services.api.automl import detect_problem_type, run_automl


def test_problem_type_detection():
    """Verifies heuristic problem type detection across varied column types."""
    df = pd.DataFrame({
        "binary_num": [0, 1, 0, 1, 0, 1],
        "binary_str": ["yes", "no", "yes", "no", "yes", "no"],
        "multiclass_str": ["cat", "dog", "bird", "fish", "dog", "cat"],
        "multiclass_int": [1, 2, 3, 1, 2, 3],
        "continuous_reg": np.linspace(10.5, 99.2, 6),
    })

    assert detect_problem_type(df, "binary_num") == "binary"
    assert detect_problem_type(df, "binary_str") == "binary"
    assert detect_problem_type(df, "multiclass_str") == "multiclass"
    assert detect_problem_type(df, "multiclass_int") == "multiclass"
    assert detect_problem_type(df, "continuous_reg") == "regression"


def test_automl_classification_training():
    """Verifies end-to-end classification benchmarking and feature importances."""
    np.random.seed(42)
    n = 120
    age = np.random.randint(20, 70, size=n)
    tenure = np.random.randint(1, 10, size=n)
    contract = np.random.choice(["Month-to-month", "One year", "Two year"], size=n)
    # Synthetic target correlated with age and tenure
    prob = 1 / (1 + np.exp(-(0.05 * age - 0.2 * tenure)))
    churn = (np.random.rand(n) < prob).astype(int)

    df = pd.DataFrame({
        "age": age,
        "tenure": tenure,
        "contract": contract,
        "churn": churn,
    })

    res = run_automl(
        df=df,
        session_id="automl_session",
        target_column="churn",
        max_rows=1000,
    )

    assert res.problem_type == "binary"
    assert len(res.models) >= 2
    assert res.best_model != ""
    assert res.rows_trained == n

    # Check metrics on best model
    best = next(m for m in res.models if m.is_best)
    assert "accuracy" in best.metrics
    assert best.metrics["accuracy"] >= 0.50

    # Check confusion matrix
    assert res.confusion_matrix is not None
    assert len(res.confusion_matrix.labels) == 2
    assert len(res.confusion_matrix.matrix) == 2

    # Check feature importances
    assert len(res.feature_importances) > 0
    top_features = [f.feature for f in res.feature_importances]
    assert "age" in top_features or "tenure" in top_features or "contract" in top_features

    # Check generated Python code syntax
    assert "def train_baseline(df: pd.DataFrame):" in res.generated_code
    ast.parse(res.generated_code)  # Raises SyntaxError if invalid Python


def test_automl_regression_training():
    """Verifies end-to-end regression benchmarking, R² scoring, and feature attribution."""
    np.random.seed(42)
    n = 150
    sqft = np.random.uniform(500, 3500, size=n)
    bedrooms = np.random.randint(1, 6, size=n)
    neighborhood = np.random.choice(["Downtown", "Suburbs", "Rural"], size=n)
    price = 150 * sqft + 20000 * bedrooms + np.random.normal(0, 10000, size=n)

    df = pd.DataFrame({
        "sqft": sqft,
        "bedrooms": bedrooms,
        "neighborhood": neighborhood,
        "price": price,
    })

    res = run_automl(
        df=df,
        session_id="regression_session",
        target_column="price",
    )

    assert res.problem_type == "regression"
    assert len(res.models) >= 2

    best = next(m for m in res.models if m.is_best)
    assert "r2_score" in best.metrics
    assert best.metrics["r2_score"] > 0.60  # Strong synthetic regression signal

    # Verify generated script
    ast.parse(res.generated_code)
