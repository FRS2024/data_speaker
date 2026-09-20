"""FastAPI micro-daemon exposing the stateful sandbox runner over HTTP."""

import os
import time
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.sandbox.runner import SandboxRunner, ExecutionResult


START_TIME = time.time()
runner: Optional[SandboxRunner] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global runner
    default_timeout = int(os.environ.get("SANDBOX_TIMEOUT", "60"))
    runner = SandboxRunner(default_timeout_seconds=default_timeout)
    yield
    if runner:
        runner.reset()


app = FastAPI(
    title="data_speaker Sandbox Execution Daemon",
    version="0.1.0",
    lifespan=lifespan,
)


class ExecuteRequest(BaseModel):
    code: str = Field(..., description="Python code block to execute sequentially")
    timeout_seconds: Optional[int] = Field(None, description="Optional per-execution timeout in seconds")


class ExecuteResponse(BaseModel):
    status: str
    stdout: str
    stderr: str
    figures: List[Dict[str, Any]] = Field(default_factory=list)
    duration_ms: int
    has_mutated_df: bool
    df_shape: Optional[List[int]] = None


class HealthResponse(BaseModel):
    status: str
    ready: bool
    uptime_seconds: float
    has_df: bool


@app.get("/health", response_model=HealthResponse)
def health_check():
    if runner is None:
        raise HTTPException(status_code=503, detail="Sandbox runner not initialized")
    state = runner.get_state()
    return HealthResponse(
        status="healthy",
        ready=True,
        uptime_seconds=round(time.time() - START_TIME, 2),
        has_df=state.get("has_df", False),
    )


@app.post("/execute", response_model=ExecuteResponse)
def execute_code(request: ExecuteRequest):
    if runner is None:
        raise HTTPException(status_code=503, detail="Sandbox runner not initialized")

    result: ExecutionResult = runner.execute(
        code=request.code,
        timeout_seconds=request.timeout_seconds,
    )

    return ExecuteResponse(
        status=result.status,
        stdout=result.stdout,
        stderr=result.stderr,
        figures=result.figures,
        duration_ms=result.duration_ms,
        has_mutated_df=result.has_mutated_df,
        df_shape=list(result.df_shape) if result.df_shape else None,
    )


class CheckpointFileRequest(BaseModel):
    file_path: str = Field(..., description="Path to checkpoint parquet file")


@app.post("/reset")
def reset_sandbox():
    if runner is None:
        raise HTTPException(status_code=503, detail="Sandbox runner not initialized")
    runner.reset()
    return {"status": "reset_complete"}


@app.get("/state")
def get_sandbox_state():
    if runner is None:
        raise HTTPException(status_code=503, detail="Sandbox runner not initialized")
    return runner.get_state()


@app.post("/checkpoint/save")
def save_checkpoint(request: CheckpointFileRequest):
    if runner is None:
        raise HTTPException(status_code=503, detail="Sandbox runner not initialized")
    try:
        return runner.save_checkpoint(request.file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/checkpoint/restore")
def restore_checkpoint(request: CheckpointFileRequest):
    if runner is None:
        raise HTTPException(status_code=503, detail="Sandbox runner not initialized")
    try:
        return runner.load_checkpoint(request.file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("SANDBOX_HOST", "0.0.0.0")
    port = int(os.environ.get("SANDBOX_PORT", "8000"))
    uvicorn.run("services.sandbox.server:app", host=host, port=port, log_level="info")
