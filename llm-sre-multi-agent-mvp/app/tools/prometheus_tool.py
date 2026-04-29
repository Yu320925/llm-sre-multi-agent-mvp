from app.schemas.diagnosis import ToolResult


class PrometheusTool:
    def query_service_overview(self, service: str, namespace: str | None = None) -> ToolResult:
        data = {
            "service": service,
            "namespace": namespace,
            "request_rate_rps": 420,
            "error_rate_percent": 14.8,
            "p95_latency_ms": 1850,
            "cpu_percent": 51,
            "memory_percent": 63,
        }
        summary = (
            f"Prometheus indicates {service} request rate=420rps, error rate=14.8%, "
            f"p95 latency=1850ms, CPU=51%, memory=63%. Error rate and latency are elevated "
            f"without corresponding CPU saturation."
        )
        return ToolResult(
            tool_name="prometheus_tool",
            success=True,
            data=data,
            summary=summary,
        )
