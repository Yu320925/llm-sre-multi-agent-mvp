from app.schemas.diagnosis import ToolResult


class TopologyTool:
    def get_dependencies(self, service: str) -> ToolResult:
        dependencies = {
            "service": service,
            "dependencies": [
                {"name": "payment-db", "type": "database", "critical": True},
                {"name": "inventory-service", "type": "http", "critical": False},
                {"name": "user-profile-service", "type": "http", "critical": False},
            ],
        }
        summary = (
            f"Topology for {service} shows critical downstream dependency payment-db, "
            f"plus non-critical dependencies inventory-service and user-profile-service."
        )
        return ToolResult(
            tool_name="topology_tool",
            success=True,
            data=dependencies,
            summary=summary,
        )
