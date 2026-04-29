from app.schemas.diagnosis import ToolResult


class ElasticsearchTool:
    def search_logs(self, service: str, query: str, time_range: str) -> ToolResult:
        hits = [
            {
                "timestamp": "2026-04-29T10:01:12Z",
                "level": "ERROR",
                "message": "TimeoutError: acquire connection timed out from pool",
            },
            {
                "timestamp": "2026-04-29T10:01:43Z",
                "level": "ERROR",
                "message": "DatabaseError: connection pool exhausted",
            },
            {
                "timestamp": "2026-04-29T10:02:02Z",
                "level": "WARN",
                "message": "Downstream payment-db latency above threshold",
            },
        ]

        summary = (
            f"Elasticsearch logs for {service} in {time_range} show repeated "
            f"'connection pool exhausted' and timeout errors related to payment-db."
        )

        return ToolResult(
            tool_name="elasticsearch_tool",
            success=True,
            data={
                "service": service,
                "query": query,
                "time_range": time_range,
                "hits": hits,
            },
            summary=summary,
        )
