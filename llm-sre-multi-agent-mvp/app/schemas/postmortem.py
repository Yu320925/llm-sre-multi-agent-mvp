from pydantic import BaseModel
from typing import Any


class PostmortemResult(BaseModel):
    markdown: str
    timeline: list[dict[str, Any]]
    metadata: dict[str, Any]
