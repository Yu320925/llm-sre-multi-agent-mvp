from pydantic import BaseModel, Field
from typing import Any


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    summary: str


class DiagnosisStep(BaseModel):
    step: int
    hypothesis: str
    action: str
    observation: str
    conclusion: str | None = None
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = None
    tool_output: dict[str, Any] | None = None


class DiagnosisResult(BaseModel):
    root_cause: str
    confidence: float
    affected_services: list[str]
    evidence: list[dict[str, Any]]
    trace: list[DiagnosisStep]
    final_summary: str
