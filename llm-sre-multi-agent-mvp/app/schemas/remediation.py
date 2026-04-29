from pydantic import BaseModel
from typing import Any


class RemediationResult(BaseModel):
    title: str
    actions: list[dict[str, Any]]
    script: str
    approval_required: bool
    risk: str
    rationale: str
