"""Integration test verifying the running Docker sandbox container over HTTP."""

import pytest
from services.sandbox.client import RemoteSandboxClient


@pytest.fixture
def remote_client():
    client = RemoteSandboxClient(base_url="http://localhost:8000")
    client.reset()
    return client


def test_docker_health(remote_client):
    health = remote_client.health()
    assert health["status"] == "healthy"
    assert health["ready"] is True


def test_docker_state_persistence_and_mutation(remote_client):
    # Turn 1: define variables and df
    code1 = (
        "import pandas as pd\n"
        "x = 100\n"
        "df = pd.DataFrame({'a': [1, 2, 3], 'b': [10, 20, 30]})\n"
        "print(df.shape)"
    )
    res1 = remote_client.execute(code1)
    assert res1.status == "success"
    assert res1.has_mutated_df is True
    assert res1.df_shape == (3, 2)
    assert "(3, 2)" in res1.stdout

    # Turn 2: mutate df using x from Turn 1
    code2 = "df['total'] = df['a'] * df['b'] + x"
    res2 = remote_client.execute(code2)
    assert res2.status == "success"
    assert res2.has_mutated_df is True
    assert res2.df_shape == (3, 3)

    # Turn 3: print computed result
    code3 = "print(df['total'].tolist())"
    res3 = remote_client.execute(code3)
    assert res3.status == "success"
    assert "[110, 140, 190]" in res3.stdout.strip()


def test_docker_plotly_capture(remote_client):
    code = (
        "import plotly.express as px\n"
        "df_chart = pd.DataFrame({'team': ['Eng', 'Design', 'Product'], 'count': [12, 4, 6]})\n"
        "fig = px.pie(df_chart, values='count', names='team', title='Team Distribution')\n"
        "fig.show()"
    )
    res = remote_client.execute(code)
    assert res.status == "success"
    assert len(res.figures) >= 1
    chart_spec = res.figures[0]
    assert "data" in chart_spec
    assert chart_spec["layout"]["title"]["text"] == "Team Distribution"


def test_docker_runtime_error_traceback(remote_client):
    code = "import nonexistent_module"
    res = remote_client.execute(code)
    assert res.status == "error"
    assert "ModuleNotFoundError" in res.stderr
