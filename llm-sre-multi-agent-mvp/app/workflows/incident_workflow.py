import logging

from sqlalchemy.orm import Session

from app.agents.diagnosis_agent import DiagnosisAgent
from app.agents.perception_agent import PerceptionAgent
from app.agents.postmortem_agent import PostmortemAgent
from app.agents.remediation_agent import RemediationAgent
from app.schemas.alert import AlertWebhookRequest
from app.services.diagnosis_service import DiagnosisService
from app.services.incident_service import IncidentService
from app.services.postmortem_service import PostmortemService
from app.services.remediation_service import RemediationService

logger = logging.getLogger(__name__)


class IncidentWorkflow:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.incident_service = IncidentService(db)
        self.diagnosis_service = DiagnosisService(db)
        self.remediation_service = RemediationService(db)
        self.postmortem_service = PostmortemService(db)

        self.perception_agent = PerceptionAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.remediation_agent = RemediationAgent()
        self.postmortem_agent = PostmortemAgent()

    def run(self, incident_id: str, payload: AlertWebhookRequest) -> None:
        logger.info("Workflow start: %s", incident_id)

        perception_output = self.perception_agent.run(payload)
        self.incident_service.update_perception(incident_id, perception_output)

        diagnosis_result = self.diagnosis_agent.run(perception_output)
        diagnosis_output = diagnosis_result.model_dump()
        self.incident_service.update_diagnosis(incident_id, diagnosis_output)
        self.diagnosis_service.save_trace(incident_id, diagnosis_output["trace"])

        incident = self.incident_service.get_incident(incident_id)
        if not incident:
            logger.error("Incident not found during workflow: %s", incident_id)
            return

        remediation_result = self.remediation_agent.run(
            incident={
                "id": incident.id,
                "status": incident.status,
                "severity": incident.severity,
                "service": incident.service,
                "summary": incident.summary,
            },
            diagnosis=diagnosis_output,
        )
        remediation_output = remediation_result.model_dump()
        self.incident_service.update_remediation(incident_id, remediation_output)
        self.remediation_service.save_plan(incident_id, remediation_output)

        incident = self.incident_service.get_incident(incident_id)
        if not incident:
            logger.error("Incident not found before postmortem: %s", incident_id)
            return

        postmortem_result = self.postmortem_agent.run(
            incident={
                "id": incident.id,
                "status": "resolved",
                "severity": incident.severity,
                "service": incident.service,
                "summary": incident.summary,
            },
            diagnosis=diagnosis_output,
            remediation=remediation_output,
        )
        postmortem_output = postmortem_result.model_dump()
        self.incident_service.update_postmortem(incident_id, postmortem_output)
        self.postmortem_service.save_report(incident_id, postmortem_output)

        logger.info("Workflow finished: %s", incident_id)
