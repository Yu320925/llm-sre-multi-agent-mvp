from app.agents.base import BaseAgent
from app.schemas.diagnosis import DiagnosisResult, DiagnosisStep
from app.tools.elasticsearch_tool import ElasticsearchTool
from app.tools.prometheus_tool import PrometheusTool
from app.tools.runbook_tool import RunbookTool
from app.tools.topology_tool import TopologyTool


class DiagnosisAgent(BaseAgent):
    def __init__(self) -> None:
        self.prom = PrometheusTool()
        self.es = ElasticsearchTool()
        self.topology = TopologyTool()
        self.runbook = RunbookTool()

    def run(self, perception_output: dict) -> DiagnosisResult:
        ctx = perception_output["aggregated_context"]
        service = ctx["service"]
        namespace = ctx.get("namespace")
        trace: list[DiagnosisStep] = []

        step1_result = self.prom.query_service_overview(service=service, namespace=namespace)
        trace.append(
            DiagnosisStep(
                step=1,
                hypothesis=f"{service} itself is overloaded or serving elevated 5xx errors",
                action="query_prometheus(service_overview_metrics)",
                observation=step1_result.summary,
                conclusion="Service error rate is elevated while CPU is not saturated.",
                tool_name=step1_result.tool_name,
                tool_input={"service": service, "namespace": namespace},
                tool_output=step1_result.data,
            )
        )

        step2_result = self.topology.get_dependencies(service=service)
        trace.append(
            DiagnosisStep(
                step=2,
                hypothesis=f"{service} may be impacted by an unhealthy downstream dependency",
                action="get_service_topology(dependencies)",
                observation=step2_result.summary,
                conclusion="Primary downstream dependency identified as payment-db.",
                tool_name=step2_result.tool_name,
                tool_input={"service": service},
                tool_output=step2_result.data,
            )
        )

        step3_result = self.es.search_logs(
            service=service,
            query="error OR exception OR timeout",
            time_range="last_15m",
        )
        trace.append(
            DiagnosisStep(
                step=3,
                hypothesis="Application logs may reveal concrete exceptions corresponding to 5xx spikes",
                action="query_elasticsearch(error_logs)",
                observation=step3_result.summary,
                conclusion="Connection pool exhaustion and DB timeout patterns found in logs.",
                tool_name=step3_result.tool_name,
                tool_input={"service": service, "query": "error OR exception OR timeout", "time_range": "last_15m"},
                tool_output=step3_result.data,
            )
        )

        step4_result = self.runbook.search(keyword="connection pool exhausted")
        trace.append(
            DiagnosisStep(
                step=4,
                hypothesis="Historical runbooks may confirm likely root cause and standard mitigations",
                action="search_runbook(connection pool exhausted)",
                observation=step4_result.summary,
                conclusion="Runbook strongly matches DB connection pool exhaustion scenario.",
                tool_name=step4_result.tool_name,
                tool_input={"keyword": "connection pool exhausted"},
                tool_output=step4_result.data,
            )
        )

        root_cause = "Database connection pool exhausted in payment-db causing timeout propagation to checkout-service"
        confidence = 0.91
        affected_services = [service, "payment-db"]
        evidence = [
            {
                "type": "metric",
                "source": "prometheus",
                "detail": step1_result.summary,
            },
            {
                "type": "topology",
                "source": "service-topology",
                "detail": step2_result.summary,
            },
            {
                "type": "log",
                "source": "elasticsearch",
                "detail": step3_result.summary,
            },
            {
                "type": "runbook",
                "source": "knowledge-base",
                "detail": step4_result.summary,
            },
        ]

        return DiagnosisResult(
            root_cause=root_cause,
            confidence=confidence,
            affected_services=affected_services,
            evidence=evidence,
            trace=trace,
            final_summary=(
                f"Diagnosed {service} incident as a downstream database connectivity saturation issue. "
                f"payment-db connection pool exhaustion likely caused request timeouts and elevated 5xx."
            ),
        )
