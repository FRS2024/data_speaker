"""
Unit test suite for Track D: Statistician Critic Guardrails & AST Audits.
Validates pre-execution static AST rules and post-execution statistical validity checks.
"""

import pandas as pd
import pytest

from services.api.agent.critic import StatisticianCritic


@pytest.fixture
def critic() -> StatisticianCritic:
    return StatisticianCritic()


def test_pre_execute_audit_clean_code(critic: StatisticianCritic):
    """Clean idiomatic pandas code should be approved with high confidence."""
    code = (
        "summary = df.sort_values(by='salary', ascending=False).head(10)\n"
        "print(summary[['name', 'salary']])"
    )
    review = critic.pre_execute_audit(code)
    assert review.verdict == "approved"
    assert review.confidence_score >= 90.0
    assert len(review.detected_fallacies) == 0


def test_pre_execute_audit_catches_unlogged_dropna(critic: StatisticianCritic):
    """Calling dropna() without logging shape/counts should trigger an AST warning."""
    code = "df_clean = df.dropna()\nprint(df_clean.describe())"
    review = critic.pre_execute_audit(code)
    assert "uncontrolled_data_loss" in review.detected_fallacies
    assert any("dropna" in w.lower() for w in review.statistical_warnings)


def test_pre_execute_audit_catches_arbitrary_head(critic: StatisticianCritic):
    """Slicing head() without sort_values() should trigger a selection bias warning."""
    code = "top_rows = df.head(5)\nprint(top_rows)"
    review = critic.pre_execute_audit(code)
    assert "selection_bias" in review.detected_fallacies
    assert any("sort_values" in w for w in review.statistical_warnings)


def test_pre_execute_audit_catches_mean_of_means(critic: StatisticianCritic):
    """Averaging averages should trigger a revision requirement."""
    code = "overall_avg = df.groupby('dept')['salary'].mean().mean()\nprint(overall_avg)"
    review = critic.pre_execute_audit(code)
    assert review.verdict == "requires_revision"
    assert "unweighted_mean_of_means" in review.detected_fallacies
    assert review.suggested_fix is not None


def test_post_execute_audit_catches_small_sample_size(critic: StatisticianCritic):
    """Stdout reporting sample sizes N < 30 should be flagged with small sample warning."""
    code = "print('Count of active users:', len(df))"
    stdout = "Group A Total Count: 14\nMean Salary: 75000"
    review = critic.post_execute_audit(code=code, stdout=stdout)
    assert not review.sample_size_ok
    assert "small_sample_fallacy" in review.detected_fallacies
    assert any("N = 14 < 30" in w for w in review.statistical_warnings)


def test_post_execute_audit_catches_skewness(critic: StatisticianCritic):
    """Severe divergence between Mean and Median should flag outlier/skewness distortion."""
    code = "print(df['bonus'].describe())"
    stdout = "Mean: 125000.0\nMedian: 35000.0\nStd: 85000.0"
    review = critic.post_execute_audit(code=code, stdout=stdout)
    assert "skewness_distortion" in review.detected_fallacies
    assert any("skew" in w.lower() for w in review.statistical_warnings)


def test_post_execute_audit_catches_severe_data_loss(critic: StatisticianCritic):
    """Losing >20% of rows after operation flags survivorship bias risk."""
    df_before = pd.DataFrame({"x": range(100)})
    df_after = pd.DataFrame({"x": range(60)})  # 40% loss
    code = "df = df[df['x'] > 40]"
    stdout = "Filtered down rows."
    review = critic.post_execute_audit(
        code=code, stdout=stdout, df_before=df_before, df_after=df_after
    )
    assert "survivorship_bias" in review.detected_fallacies
    assert any("Severe Data Loss" in w for w in review.statistical_warnings)


def test_post_execute_audit_catches_correlation_guardrail(critic: StatisticianCritic):
    """Correlation queries should append observational confounder warning."""
    code = "corr_matrix = df[['tenure', 'churn']].corr()\nprint(corr_matrix)"
    stdout = "tenure churn\ntenure 1.0 -0.45\nchurn -0.45 1.0"
    review = critic.post_execute_audit(code=code, stdout=stdout)
    assert "observational_correlation" in review.detected_fallacies
    assert any("causation" in w.lower() for w in review.statistical_warnings)
