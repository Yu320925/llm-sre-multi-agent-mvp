from app.schemas.diagnosis import ToolResult
from app.storage.knowledge_base import load_runbooks


class RunbookTool:
    def search(self, keyword: str) -> ToolResult:
        runbooks = load_runbooks()
        matched = [rb for rb in runbooks if keyword.lower() in " ".join(rb.get("keywords", [])).lower()]
        summary = (
            f"Knowledge base search found {len(matched)} runbook(s) related to '{keyword}'."
        )
        return ToolResult(
            tool_name="runbook_tool",
            success=True,
            data={"keyword": keyword, "matches": matched},
            summary=summary,
        )
