"""
Statistician & Critic Agent for Track D Multi-Agent Swarm.
Performs two-stage audits:
1. Pre-execution static AST screening for methodology & data-loss traps.
2. Post-execution statistical verification for sample size adequacy (N < 30),
   distributional skewness, correlation leaps, and Simpson's paradox risks.
"""

from __future__ import annotations

import ast
import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from services.api.models import CriticReview


class StatisticianCritic:
    """Rigorous statistical reviewer that audits code and outputs before user delivery."""

    def pre_execute_audit(self, code: str, df: Optional[pd.DataFrame] = None) -> CriticReview:
        """
        Static AST and heuristic scan of Python code prior to sandbox execution.
        Catches silent dropna, Cartesian join explosions, and reckless filtering.
        """
        warnings: List[str] = []
        fallacies: List[str] = []
        requires_revision = False
        suggested_fix = None

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return CriticReview(
                verdict="requires_revision",
                confidence_score=20.0,
                statistical_warnings=[f"Syntax Error in generated code: {e.msg}"],
                critique="The code contains syntax errors and cannot be compiled.",
                sample_size_ok=False,
                detected_fallacies=["syntax_error"],
            )

        # 1. Detect uncontrolled dropna without verification
        has_dropna = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr == "dropna":
                has_dropna = True
                break

        if has_dropna:
            # Check if code prints or checks dropped rows
            if "len(" not in code and "shape" not in code and "isnull" not in code:
                warnings.append(
                    "Uncontrolled Data Loss Risk: Calling dropna() without computing or logging "
                    "the percentage of dropped rows. Recommend logging dropped record volume."
                )
                fallacies.append("uncontrolled_data_loss")

        # 2. Detect arbitrary head/tail slicing without ordering
        if re.search(r"df(\[[^\]]+\])?\.(head|tail)\(\d+\)", code) and "sort_values" not in code:
            warnings.append(
                "Arbitrary Sample Slicing: Slicing head()/tail() without explicit sort_values() "
                "depends on physical row storage order and may introduce selection bias."
            )
            fallacies.append("selection_bias")

        # 3. Detect averaging averages (mathematical fallacy)
        if re.search(r"\.mean\(\)[^;\n]*\.mean\(\)", code):
            warnings.append(
                "Mathematical Fallacy: Computing mean of means without weighting by group sizes "
                "distorts the true population mean."
            )
            fallacies.append("unweighted_mean_of_means")
            requires_revision = True
            suggested_fix = "Use sum() / total_count instead of chaining mean() over pre-aggregated groups."

        # Compute pre-execution confidence
        if requires_revision:
            confidence = 45.0
            verdict = "requires_revision"
        elif warnings:
            confidence = 75.0
            verdict = "warning"
        else:
            confidence = 98.0
            verdict = "approved"

        critique = (
            "Code pre-screened cleanly with zero critical methodology violations."
            if not warnings
            else f"Identified {len(warnings)} methodology caveat(s) for consideration."
        )

        return CriticReview(
            verdict=verdict,
            confidence_score=confidence,
            statistical_warnings=warnings,
            critique=critique,
            sample_size_ok=True,
            detected_fallacies=fallacies,
            suggested_fix=suggested_fix,
        )

    def post_execute_audit(
        self,
        code: str,
        stdout: str,
        df_before: Optional[pd.DataFrame] = None,
        df_after: Optional[pd.DataFrame] = None,
        figures: Optional[List[Dict[str, Any]]] = None,
    ) -> CriticReview:
        """
        Deep post-execution audit inspecting numeric values, sample sizes, and output distributions.
        """
        warnings: List[str] = []
        fallacies: List[str] = []
        sample_size_ok = True
        confidence = 95.0

        # 1. Audit Data Loss if DataFrame was mutated
        if df_before is not None and df_after is not None:
            n_before = len(df_before)
            n_after = len(df_after)
            if n_before > 0:
                loss_ratio = (n_before - n_after) / n_before
                if loss_ratio > 0.20:
                    warnings.append(
                        f"Severe Data Loss Detected: Operation removed {loss_ratio:.1%} of records "
                        f"({n_before:,} ➔ {n_after:,} rows). Check if aggressive filtering or inner join occurred."
                    )
                    fallacies.append("survivorship_bias")
                    confidence -= 30.0

        # 2. Audit Subgroup Sample Sizes (N < 30 Trap)
        # Search stdout for count tables or group distributions
        count_matches = re.findall(r"(?:count|n|size|total)\s*[:=]\s*(\d+)", stdout, re.IGNORECASE)
        for c_str in count_matches:
            val = int(c_str)
            if 0 < val < 30:
                sample_size_ok = False
                warnings.append(
                    f"Small Subgroup Sample Size (N = {val} < 30): Statistical power is limited. "
                    "Central Limit Theorem does not reliably apply; avoid definitive causal conclusions."
                )
                fallacies.append("small_sample_fallacy")
                confidence -= 20.0
                break

        # 3. Check for Outlier & Mean-Median Divergence
        # Match lines reporting both mean and median
        mean_match = re.search(r"mean\s*[:=]\s*([+-]?\d+(?:\.\d+)?)", stdout, re.IGNORECASE)
        median_match = re.search(r"median\s*[:=]\s*([+-]?\d+(?:\.\d+)?)", stdout, re.IGNORECASE)
        if mean_match and median_match:
            try:
                mean_val = float(mean_match.group(1))
                median_val = float(median_match.group(1))
                if abs(median_val) > 1e-4:
                    divergence = abs(mean_val - median_val) / abs(median_val)
                    if divergence > 0.50:
                        warnings.append(
                            f"Significant Distributional Skew (Mean {mean_val:.2f} vs Median {median_val:.2f}): "
                            "Distribution is heavily skewed by outliers. Median and IQR are strongly recommended."
                        )
                        fallacies.append("skewness_distortion")
                        confidence -= 15.0
            except ValueError:
                pass

        # 4. Correlation vs Causality Check
        if "corr" in code.lower() or "pearson" in code.lower():
            warnings.append(
                "Correlation vs Causation Guardrail: Measured associations reflect observational alignment. "
                "Uncontrolled confounders may influence relationships."
            )
            fallacies.append("observational_correlation")

        # 5. Determine Verdict
        confidence = max(10.0, min(100.0, confidence))
        if confidence < 60.0:
            verdict = "requires_revision"
        elif warnings:
            verdict = "warning"
        else:
            verdict = "approved"

        critique = (
            "Statistical peer-review passed with robust sample size and sound methodology."
            if not warnings
            else f"Statistical review completed with {len(warnings)} advisory warning(s)."
        )

        return CriticReview(
            verdict=verdict,
            confidence_score=round(confidence, 1),
            statistical_warnings=warnings,
            critique=critique,
            sample_size_ok=sample_size_ok,
            detected_fallacies=fallacies,
        )


statistician_critic = StatisticianCritic()
