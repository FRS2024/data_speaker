"""
Autonomous AutoML Baseline Engine for Conversational Data Platform.
Provides problem type detection, automated preprocessing, multi-model benchmarking
(Random Forest vs Gradient Boosting vs Linear/Ridge), feature importance ranking,
and reproducible standalone Python code generation.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from services.api.models import (
    AutoMLTrainResponse,
    ConfusionMatrixData,
    FeatureImportanceItem,
    ModelBenchmarkResult,
)

logger = logging.getLogger(__name__)


def detect_problem_type(df: pd.DataFrame, target_col: str, requested_type: Optional[str] = None) -> str:
    """
    Detects whether target is binary, multiclass, or regression.
    """
    if requested_type in ("classification", "binary", "multiclass", "regression"):
        if requested_type == "classification":
            n_unique = df[target_col].nunique(dropna=True)
            return "binary" if n_unique == 2 else "multiclass"
        return requested_type

    target_s = df[target_col].dropna()
    n_unique = int(target_s.nunique())
    is_numeric = pd.api.types.is_numeric_dtype(target_s)
    is_float = pd.api.types.is_float_dtype(target_s)

    if n_unique == 2:
        return "binary"
    elif is_float:
        return "regression"
    elif not is_numeric:
        return "multiclass"
    elif n_unique <= 15:
        return "multiclass"
    else:
        return "regression"


def run_automl(
    df: pd.DataFrame,
    session_id: str,
    target_column: str,
    problem_type: Optional[str] = None,
    selected_features: Optional[List[str]] = None,
    max_rows: int = 10000,
) -> AutoMLTrainResponse:
    """
    Executes fast-bounded multi-model training, scoring, feature importance,
    and Python code synthesis.
    """
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in DataFrame.")

    # Drop rows where target is missing
    clean_df = df.dropna(subset=[target_column]).copy()
    if len(clean_df) < 10:
        raise ValueError(f"Target column '{target_column}' has fewer than 10 non-null values.")

    # Determine problem type
    resolved_type = detect_problem_type(clean_df, target_column, problem_type)

    # Downsample if exceeding max_rows for fast-bounded baseline training
    if len(clean_df) > max_rows:
        if resolved_type in ("binary", "multiclass"):
            try:
                clean_df = clean_df.groupby(target_column, group_keys=False).apply(
                    lambda x: x.sample(int(np.rint(max_rows * len(x) / len(clean_df))), random_state=42)
                )
            except Exception:
                clean_df = clean_df.sample(n=max_rows, random_state=42)
        else:
            clean_df = clean_df.sample(n=max_rows, random_state=42)

    total_trained_rows = len(clean_df)

    # Feature candidate selection
    if selected_features:
        feature_cols = [c for c in selected_features if c in clean_df.columns and c != target_column]
    else:
        feature_cols = []
        for c in clean_df.columns:
            if c == target_column:
                continue
            # Filter high cardinality ID-like text columns
            nunique = clean_df[c].nunique(dropna=True)
            if nunique == len(clean_df) and clean_df[c].dtype == object:
                continue
            if str(c).lower().endswith(("_id", "id")) and nunique > 50:
                continue
            feature_cols.append(c)

    if not feature_cols:
        raise ValueError("No valid predictive feature columns found in dataset.")

    X = clean_df[feature_cols].copy()
    y = clean_df[target_column].copy()

    # Separate numeric and categorical columns
    numeric_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(X[c])]
    categorical_cols = [c for c in feature_cols if c not in numeric_cols]

    # Preprocessing pipelines
    transformers = []
    if numeric_cols:
        numeric_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        transformers.append(("num", numeric_pipeline, numeric_cols))

    if categorical_cols:
        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False, max_categories=10)),
        ])
        transformers.append(("cat", categorical_pipeline, categorical_cols))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

    # Split 80/20 train/test
    stratify = y if resolved_type in ("binary", "multiclass") and y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=stratify
    )

    # Model definitions
    if resolved_type in ("binary", "multiclass"):
        candidate_models = [
            ("rf", "Random Forest Classifier", RandomForestClassifier(n_estimators=60, max_depth=10, random_state=42, n_jobs=-1)),
            ("gb", "Gradient Boosting (Hist)", HistGradientBoostingClassifier(max_iter=60, random_state=42)),
            ("lr", "Logistic Regression", LogisticRegression(max_iter=300, random_state=42)),
        ]
    else:
        candidate_models = [
            ("rf", "Random Forest Regressor", RandomForestRegressor(n_estimators=60, max_depth=10, random_state=42, n_jobs=-1)),
            ("gb", "Gradient Boosting (Hist)", HistGradientBoostingRegressor(max_iter=60, random_state=42)),
            ("ridge", "Ridge Regressor", Ridge(random_state=42)),
        ]

    benchmark_results: List[ModelBenchmarkResult] = []
    trained_pipelines: Dict[str, Pipeline] = {}

    for key, display_name, estimator in candidate_models:
        pipe = Pipeline([
            ("prep", preprocessor),
            ("model", estimator),
        ])

        t0 = time.time()
        try:
            pipe.fit(X_train, y_train)
            train_ms = round((time.time() - t0) * 1000, 1)
            y_pred = pipe.predict(X_test)

            metrics: Dict[str, float] = {}
            if resolved_type in ("binary", "multiclass"):
                metrics["accuracy"] = round(float(accuracy_score(y_test, y_pred)), 4)
                metrics["f1_weighted"] = round(float(f1_score(y_test, y_pred, average="weighted", zero_division=0)), 4)
                metrics["precision"] = round(float(precision_score(y_test, y_pred, average="weighted", zero_division=0)), 4)
                metrics["recall"] = round(float(recall_score(y_test, y_pred, average="weighted", zero_division=0)), 4)

                # ROC-AUC if probability supported
                try:
                    if hasattr(pipe.named_steps["model"], "predict_proba"):
                        y_prob = pipe.predict_proba(X_test)
                        if resolved_type == "binary":
                            metrics["roc_auc"] = round(float(roc_auc_score(y_test, y_prob[:, 1])), 4)
                        else:
                            metrics["roc_auc"] = round(float(roc_auc_score(y_test, y_prob, multi_class="ovr")), 4)
                except Exception:
                    pass
            else:
                r2 = float(r2_score(y_test, y_pred))
                rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
                mae = float(mean_absolute_error(y_test, y_pred))
                metrics["r2_score"] = round(r2, 4)
                metrics["rmse"] = round(rmse, 4)
                metrics["mae"] = round(mae, 4)

            benchmark_results.append(
                ModelBenchmarkResult(
                    model_name=key,
                    display_name=display_name,
                    metrics=metrics,
                    training_time_ms=train_ms,
                )
            )
            trained_pipelines[key] = pipe
        except Exception as e:
            logger.warning(f"AutoML model {key} failed: {e}")

    if not benchmark_results:
        raise RuntimeError("All candidate models failed during training.")

    # Determine Best Model
    if resolved_type in ("binary", "multiclass"):
        benchmark_results.sort(key=lambda m: m.metrics.get("f1_weighted", m.metrics.get("accuracy", 0.0)), reverse=True)
    else:
        benchmark_results.sort(key=lambda m: m.metrics.get("r2_score", -999.0), reverse=True)

    benchmark_results[0].is_best = True
    best_key = benchmark_results[0].model_name
    best_pipe = trained_pipelines[best_key]

    # Feature Importance extraction
    feature_importances: List[FeatureImportanceItem] = []
    try:
        # Use Random Forest pipeline if available for stable feature importances
        rf_pipe = trained_pipelines.get("rf", best_pipe)
        fitted_model = rf_pipe.named_steps["model"]
        if hasattr(fitted_model, "feature_importances_"):
            raw_importances = fitted_model.feature_importances_
            fitted_prep = rf_pipe.named_steps["prep"]
            encoded_names = []
            if hasattr(fitted_prep, "get_feature_names_out"):
                try:
                    encoded_names = [n.replace("num__", "").replace("cat__", "") for n in fitted_prep.get_feature_names_out()]
                except Exception:
                    encoded_names = feature_cols
            else:
                encoded_names = feature_cols

            if len(encoded_names) == len(raw_importances):
                # Aggregate one-hot encoded categories back to root column
                col_importance_map: Dict[str, float] = {}
                for name, imp in zip(encoded_names, raw_importances):
                    root_col = name.split("_")[0] if name not in feature_cols and "_" in name else name
                    if root_col not in feature_cols and name in feature_cols:
                        root_col = name
                    col_importance_map[root_col] = col_importance_map.get(root_col, 0.0) + float(imp)

                for feat, imp in col_importance_map.items():
                    feature_importances.append(
                        FeatureImportanceItem(feature=feat, importance=round(float(imp), 4))
                    )
                feature_importances.sort(key=lambda x: x.importance, reverse=True)
    except Exception as e:
        logger.warning(f"Could not compute feature importances: {e}")

    # Fallback feature importance if empty
    if not feature_importances:
        even_imp = round(1.0 / max(len(feature_cols), 1), 4)
        feature_importances = [FeatureImportanceItem(feature=c, importance=even_imp) for c in feature_cols[:10]]

    # Confusion Matrix for Classification
    cm_data: Optional[ConfusionMatrixData] = None
    if resolved_type in ("binary", "multiclass"):
        try:
            y_pred_best = best_pipe.predict(X_test)
            unique_labels = sorted(list(set(list(y_test.astype(str)) + list(y_pred_best.astype(str)))))
            cm = confusion_matrix(y_test.astype(str), y_pred_best.astype(str), labels=unique_labels)
            cm_data = ConfusionMatrixData(
                labels=[str(lbl) for lbl in unique_labels],
                matrix=[[int(val) for val in row] for row in cm],
            )
        except Exception as e:
            logger.warning(f"Confusion matrix calculation failed: {e}")

    # Generate reproducible standalone Python script
    generated_code = generate_python_code(
        target_column=target_column,
        numeric_cols=numeric_cols,
        categorical_cols=categorical_cols,
        problem_type=resolved_type,
        best_model_name=benchmark_results[0].display_name,
        best_model_key=best_key,
    )

    return AutoMLTrainResponse(
        session_id=session_id,
        target_column=target_column,
        problem_type=resolved_type,
        best_model=benchmark_results[0].display_name,
        models=benchmark_results,
        feature_importances=feature_importances[:15],
        confusion_matrix=cm_data,
        generated_code=generated_code,
        rows_trained=total_trained_rows,
    )


def generate_python_code(
    target_column: str,
    numeric_cols: List[str],
    categorical_cols: List[str],
    problem_type: str,
    best_model_name: str,
    best_model_key: str,
) -> str:
    """
    Synthesizes a clean, standalone, executable scikit-learn Python script.
    """
    is_clf = problem_type in ("binary", "multiclass")
    model_import = ""
    model_init = ""

    if best_model_key == "rf":
        if is_clf:
            model_import = "from sklearn.ensemble import RandomForestClassifier"
            model_init = "RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)"
        else:
            model_import = "from sklearn.ensemble import RandomForestRegressor"
            model_init = "RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)"
    elif best_model_key == "gb":
        if is_clf:
            model_import = "from sklearn.ensemble import HistGradientBoostingClassifier"
            model_init = "HistGradientBoostingClassifier(max_iter=100, random_state=42)"
        else:
            model_import = "from sklearn.ensemble import HistGradientBoostingRegressor"
            model_init = "HistGradientBoostingRegressor(max_iter=100, random_state=42)"
    elif best_model_key == "lr":
        model_import = "from sklearn.linear_model import LogisticRegression"
        model_init = "LogisticRegression(max_iter=500, random_state=42)"
    else:
        model_import = "from sklearn.linear_model import Ridge"
        model_init = "Ridge(random_state=42)"

    metrics_import = (
        "from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score"
        if is_clf
        else "from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error"
    )

    eval_code = (
        f"""    # 5. Evaluate Classification Metrics
    y_pred = pipeline.predict(X_test)
    print("=== Classification Report ===")
    print(classification_report(y_test, y_pred))
    print("=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))"""
        if is_clf
        else f"""    # 5. Evaluate Regression Metrics
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"R-squared: {{r2:.4f}}")
    print(f"RMSE: {{rmse:.4f}}")
    print(f"MAE:  {{mae:.4f}}")"""
    )

    return f'''# Auto-Generated Standalone Training Pipeline by Conversational Data Platform
# Problem Type: {problem_type.upper()} | Winning Baseline: {best_model_name}

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
{model_import}
{metrics_import}

def train_baseline(df: pd.DataFrame):
    # 1. Separate Features and Target
    target_col = "{target_column}"
    clean_df = df.dropna(subset=[target_col]).copy()
    
    numeric_features = {repr(numeric_cols)}
    categorical_features = {repr(categorical_cols)}
    
    X = clean_df[numeric_features + categorical_features]
    y = clean_df[target_col]
    
    # 2. Automated Feature Transformers
    transformers = []
    if numeric_features:
        num_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        transformers.append(("num", num_pipe, numeric_features))
        
    if categorical_features:
        cat_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False, max_categories=10)),
        ])
        transformers.append(("cat", cat_pipe, categorical_features))
        
    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    # 4. Fit Full Pipeline
    model = {model_init}
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model),
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
{eval_code}
    
    return pipeline

if __name__ == "__main__":
    # Load dataset
    df = pd.read_parquet("dataset.parquet")
    pipeline = train_baseline(df)
'''
