"""Client SDK for interacting with the sandbox execution engine."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import httpx

from services.sandbox.runner import SandboxRunner, ExecutionResult


class SandboxClient:
    """Base interface for sandbox interaction."""

    def execute(self, code: str, timeout_seconds: Optional[int] = None) -> ExecutionResult:
        raise NotImplementedError

    def health(self) -> Dict[str, Any]:
        raise NotImplementedError

    def reset(self) -> Dict[str, Any]:
        raise NotImplementedError

    def get_state(self) -> Dict[str, Any]:
        raise NotImplementedError

    def save_checkpoint(self, file_path: str) -> Dict[str, Any]:
        raise NotImplementedError

    def restore_checkpoint(self, file_path: str) -> Dict[str, Any]:
        raise NotImplementedError


# Backward-compatible alias
BaseSandboxClient = SandboxClient


class RemoteSandboxClient(SandboxClient):
    """HTTP client communicating with the containerized sandbox runner."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 65.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url, timeout=timeout)

    def execute(self, code: str, timeout_seconds: Optional[int] = None) -> ExecutionResult:
        payload = {"code": code, "timeout_seconds": timeout_seconds}
        resp = self.client.post("/execute", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return ExecutionResult(
            status=data["status"],
            stdout=data.get("stdout", ""),
            stderr=data.get("stderr", ""),
            figures=data.get("figures", []),
            duration_ms=data.get("duration_ms", 0),
            has_mutated_df=data.get("has_mutated_df", False),
            df_shape=tuple(data["df_shape"]) if data.get("df_shape") else None,
        )

    def health(self) -> Dict[str, Any]:
        resp = self.client.get("/health")
        resp.raise_for_status()
        return resp.json()

    def reset(self) -> Dict[str, Any]:
        resp = self.client.post("/reset")
        resp.raise_for_status()
        return resp.json()

    def get_state(self) -> Dict[str, Any]:
        resp = self.client.get("/state")
        resp.raise_for_status()
        return resp.json()

    def save_checkpoint(self, file_path: str) -> Dict[str, Any]:
        resp = self.client.post("/checkpoint/save", json={"file_path": file_path})
        resp.raise_for_status()
        return resp.json()

    def restore_checkpoint(self, file_path: str) -> Dict[str, Any]:
        resp = self.client.post("/checkpoint/restore", json={"file_path": file_path})
        resp.raise_for_status()
        return resp.json()


class LocalSandboxClient(SandboxClient):
    """In-process sandbox client for rapid local testing without container dependencies."""

    def __init__(self, default_timeout_seconds: int = 60) -> None:
        self.runner = SandboxRunner(default_timeout_seconds=default_timeout_seconds)

    def execute(self, code: str, timeout_seconds: Optional[int] = None) -> ExecutionResult:
        return self.runner.execute(code=code, timeout_seconds=timeout_seconds)

    def health(self) -> Dict[str, Any]:
        state = self.runner.get_state()
        return {
            "status": "healthy",
            "ready": True,
            "has_df": state.get("has_df", False),
        }

    def reset(self) -> Dict[str, Any]:
        self.runner.reset()
        return {"status": "reset_complete"}

    def get_state(self) -> Dict[str, Any]:
        return self.runner.get_state()

    def save_checkpoint(self, file_path: str) -> Dict[str, Any]:
        return self.runner.save_checkpoint(file_path=file_path)

    def restore_checkpoint(self, file_path: str) -> Dict[str, Any]:
        return self.runner.load_checkpoint(file_path=file_path)
