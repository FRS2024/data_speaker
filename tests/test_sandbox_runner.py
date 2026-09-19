"""Comprehensive test suite verifying the stateful execution sandbox engine."""

import pytest
from services.sandbox.client import LocalSandboxClient, SandboxClient


@pytest.fixture
def client() -> SandboxClient:
    """Fixture providing an in-process sandbox client."""
    client = LocalSandboxClient()
    client.reset()
    return client


def test_state_persistence_across_turns(client: SandboxClient):
    """Verify that variable state survives sequential execution turns."""
    # Turn 1: Assign variables
    res1 = client.execute("x = 42\nname = 'data_speaker'")
    assert res1.status == "success"
    assert res1.stderr == ""

    # Turn 2: Read and manipulate previously defined variables
    res2 = client.execute("print(f'{name}_{x + 8}')")
    assert res2.status == "success"
    assert "data_speaker_50" in res2.stdout.strip()


def test_dataframe_mutation_and_shape_tracking(client: SandboxClient):
    """Verify that DataFrames persist and shape mutations are tracked accurately."""
    # Turn 1: Instantiate DataFrame
    code1 = (
        "import pandas as pd\n"
        "df = pd.DataFrame({'age': [25, 30, 35, None], 'salary': [50000, 60000, 75000, 90000]})\n"
        "print(df.shape)"
    )
    res1 = client.execute(code1)
    assert res1.status == "success"
    assert res1.has_mutated_df is True
    assert res1.df_shape == (4, 2)
    assert "(4, 2)" in res1.stdout

    # Turn 2: Impute missing values (state mutation)
    code2 = "df['age'] = df['age'].fillna(df['age'].median())"
    res2 = client.execute(code2)
    assert res2.status == "success"
    assert res2.df_shape == (4, 2)

    # Turn 3: Add new column
    code3 = "df['bonus'] = df['salary'] * 0.10"
    res3 = client.execute(code3)
    assert res3.status == "success"
    assert res3.has_mutated_df is True
    assert res3.df_shape == (4, 3)

    # Turn 4: Assert values in memory
    code4 = "print(int(df['bonus'].sum()))"
    res4 = client.execute(code4)
    assert res4.status == "success"
    assert "27500" in res4.stdout.strip()


def test_plotly_figure_interception_via_show(client: SandboxClient):
    """Verify that Plotly figures created and shown via fig.show() are intercepted."""
    code = (
        "import plotly.express as px\n"
        "df_chart = pd.DataFrame({'category': ['A', 'B', 'C'], 'val': [10, 25, 15]})\n"
        "fig = px.bar(df_chart, x='category', y='val', title='Revenue by Category')\n"
        "fig.show()"
    )
    res = client.execute(code)
    assert res.status == "success"
    assert len(res.figures) >= 1

    figure_spec = res.figures[0]
    assert "data" in figure_spec
    assert "layout" in figure_spec
    assert figure_spec["layout"]["title"]["text"] == "Revenue by Category"


def test_plotly_figure_interception_without_show(client: SandboxClient):
    """Verify that Plotly figures assigned to 'fig' or returned as cell expression are captured."""
    code = (
        "import plotly.graph_objects as go\n"
        "fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))\n"
        "fig.update_layout(title_text='Scatter Plot')"
    )
    res = client.execute(code)
    assert res.status == "success"
    assert len(res.figures) >= 1
    assert res.figures[0]["layout"]["title"]["text"] == "Scatter Plot"


def test_stdout_and_stderr_interception(client: SandboxClient):
    """Verify stdout separation and clean Python error traceback capture."""
    # Stdout test
    res1 = client.execute("for i in range(3): print(f'Row {i}')")
    assert res1.status == "success"
    assert "Row 0\nRow 1\nRow 2" in res1.stdout

    # Stderr / Exception test (ZeroDivisionError)
    res2 = client.execute("10 / 0")
    assert res2.status == "error"
    assert "ZeroDivisionError" in res2.stderr
    assert "division by zero" in res2.stderr


def test_timeout_enforcement(client: SandboxClient):
    """Verify that runaway or infinite loops are halted cleanly at the timeout boundary."""
    code = "import time\ntime.sleep(5)"
    res = client.execute(code, timeout_seconds=1)
    assert res.status == "timeout"
    assert "timed out" in res.stderr.lower()


def test_reset_flushes_state(client: SandboxClient):
    """Verify that reset clears custom variables while keeping baseline imports functional."""
    # Turn 1: Set variable
    client.execute("secret_var = 12345")
    state1 = client.get_state()
    assert "secret_var" in state1["variables"]

    # Reset
    client.reset()

    # Turn 2: Variable should no longer exist
    res = client.execute("print(secret_var)")
    assert res.status == "error"
    assert "NameError" in res.stderr

    # But baseline imports should still work
    res_baseline = client.execute("df_test = pd.DataFrame({'x': [1]})\nprint(df_test.shape)")
    assert res_baseline.status == "success"
    assert "(1, 1)" in res_baseline.stdout
