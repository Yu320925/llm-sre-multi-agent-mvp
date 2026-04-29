from collections import defaultdict

from app.agents.base import BaseAgent
from app.schemas.alert import AlertWebhookRequest, StandardizedAlert


class PerceptionAgent(BaseAgent):
    def standardize_alerts(self, payload: AlertWebhookRequest) -> list[StandardizedAlert]:
        results: list[StandardizedAlert] = []
        for alert in payload.alerts:
            labels = alert.labels or {}
            annotations = alert.annotations or {}
            results.append(
                StandardizedAlert(
                    fingerprint=alert.fingerprint,
                    source=payload.source,
                    status=alert.status,
                    service=labels.get("service", "unknown-service"),
                    severity=labels.get("severity", "warning"),
                    namespace=labels.get("namespace"),
                    alert_name=labels.get("alertname", "UnknownAlert"),
                    summary=annotations.get("summary", labels.get("alertname", "Unknown alert")),
                    description=annotations.get("description"),
                    starts_at=alert.startsAt,
                    labels=labels,
                    annotations=annotations,
                )
            )
        return results

    def aggregate(self, alerts: list[StandardizedAlert]) -> dict:
        grouped = defaultdict(list)
        for alert in alerts:
            key = f"{alert.service}:{alert.alert_name}:{alert.severity}"
            grouped[key].append(alert)

        top_group_key = max(grouped.keys(), key=lambda x: len(grouped[x]))
        group = grouped[top_group_key]
        first = group[0]

        return {
            "group_key": top_group_key,
            "service": first.service,
            "severity": first.severity,
            "namespace": first.namespace,
            "summary": first.summary,
            "description": first.description,
            "alert_count": len(group),
            "alert_names": list({a.alert_name for a in group}),
            "fingerprints": [a.fingerprint for a in group],
        }

    def run(self, payload: AlertWebhookRequest) -> dict:
        standardized = self.standardize_alerts(payload)
        aggregated = self.aggregate(standardized)
        return {
            "standardized_alerts": [item.model_dump() for item in standardized],
            "aggregated_context": aggregated,
        }
