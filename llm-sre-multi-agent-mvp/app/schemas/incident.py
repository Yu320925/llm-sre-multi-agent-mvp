from pydantic import BaseModel
from typing import Any


class IncidentResponse(BaseModel):
    id: str
    status: str
    source: str
    severity: str
    service: str
    namespace: str | None = None
    summary: str
    description: str | None = None
    root_cause: str | None = None
    confidence: float | None = None
    affected_services: list[str] | None = None
    evidence: list[dict[str, Any]] | None = None
    perception_output: dict[str, Any] | None = None
    diagnosis_output: dict[str, Any] | None = None
    remediation_output: dict[str, Any] | None = None
    postmortem_output: dict[str, Any] | None = None

    model_config = {"from_attributes": True}
