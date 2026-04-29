from app.agents.base import BaseAgent
from app.schemas.remediation import RemediationResult
from app.storage.knowledge_base import load_runbooks


class RemediationAgent(BaseAgent):
    def run(self, incident: dict, diagnosis: dict) -> RemediationResult:
        root_cause = diagnosis["root_cause"]
        runbooks = load_runbooks()

        matched = next(
            (
                rb for rb in runbooks
                if "connection pool exhausted" in root_cause.lower()
                and "connection pool exhausted" in rb.get("keywords", [])
            ),
            None,
        )

        actions = [
            {
                "step": 1,
                "action": "Temporarily scale out checkout-service replicas to reduce per-pod request pressure",
                "type": "scale",
            },
            {
                "step": 2,
                "action": "Check and increase payment-db connection pool size if safe",
                "type": "database_tuning",
            },
            {
                "step": 3,
                "action": "Apply rate limiting on high-cardinality traffic path if error storm continues",
                "type": "traffic_control",
            },
            {
                "step": 4,
                "action": "Rollback recent release if incident correlates with deployment window",
                "type": "rollback",
            },
        ]

        if matched:
            actions.extend(matched.get("actions", []))

        script = """#!/bin/bash
set -e

echo "[MVP] Suggested remediation steps:"
echo "1) kubectl scale deploy/checkout-service --replicas=6 -n prod"
echo "2) Review DB pool configuration and max connections"
echo "3) Consider enabling temporary rate limit at gateway"
echo "4) Rollback last release if deployment correlation confirmed"
"""

        return RemediationResult(
            title="Mitigation plan for DB connection pool exhaustion",
            actions=actions,
            script=script,
            approval_required=True,
            risk="medium",
            rationale=(
                "Actions prioritize service stabilization, dependency pressure reduction, and safe rollback. "
                "Human approval is required for scaling, DB tuning, and rollback operations."
            ),
        )
