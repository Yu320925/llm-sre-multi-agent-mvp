from pydantic import BaseModel, Field
from typing import Any


class AlertItem(BaseModel):
    fingerprint: str
    status: str
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)
    startsAt: str | None = None


class AlertWebhookRequest(BaseModel):
    source: str
    alerts: list[AlertItem]


class AlertWebhookResponse(BaseModel):
    incident_id: str
    status: str
    message: str


class StandardizedAlert(BaseModel):
    fingerprint: str
    source: str
    status: str
    service: str
    severity: str
    namespace: str | None = None
    alert_name: str
    summary: str
    description: str | None = None
    starts_at: str | None = None
    labels: dict[str, Any] = Field(default_factory=dict)
    annotations: dict[str, Any] = Field(default_factory=dict)
