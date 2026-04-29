from app.agents.base import BaseAgent
from app.schemas.postmortem import PostmortemResult
from app.utils.time import utc_now_iso


class PostmortemAgent(BaseAgent):
    def run(self, incident: dict, diagnosis: dict, remediation: dict) -> PostmortemResult:
        timeline = [
            {"time": utc_now_iso(), "event": "Alert received and incident created"},
            {"time": utc_now_iso(), "event": "Perception Agent aggregated alerts"},
            {"time": utc_now_iso(), "event": "Diagnosis Agent completed structured evidence collection"},
            {"time": utc_now_iso(), "event": "Remediation Agent generated mitigation plan"},
            {"time": utc_now_iso(), "event": "Incident marked resolved for MVP demo flow"},
        ]

        markdown = f"""# Incident Postmortem - {incident["id"]}

## Summary
- **Service**: {incident["service"]}
- **Severity**: {incident["severity"]}
- **Status**: {incident["status"]}
- **Summary**: {incident["summary"]}

## Root Cause
{diagnosis["root_cause"]}

## Confidence
{diagnosis["confidence"]}

## Affected Services
{", ".join(diagnosis["affected_services"])}

## Evidence
""" + "\n".join(
            [f"- [{ev['type']}] {ev['detail']}" for ev in diagnosis["evidence"]]
        ) + f"""

## Mitigation Plan
- **Title**: {remediation["title"]}
- **Approval Required**: {remediation["approval_required"]}
- **Risk**: {remediation["risk"]}

### Actions
""" + "\n".join(
            [f"- Step {a.get('step', '?')}: {a.get('action')}" for a in remediation["actions"]]
        ) + f"""

### Suggested Script
```bash
{remediation["script"]}
