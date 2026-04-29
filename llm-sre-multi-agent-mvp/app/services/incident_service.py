from sqlalchemy.orm import Session

from app.models import AlertEvent, Incident
from app.schemas.alert import AlertWebhookRequest
from app.utils.ids import generate_incident_id


class IncidentService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_incident_from_alerts(self, payload: AlertWebhookRequest) -> Incident:
        first = payload.alerts[0]
        labels = first.labels or {}
        annotations = first.annotations or {}

        incident = Incident(
            id=generate_incident_id(),
            status="processing",
            source=payload.source,
            severity=labels.get("severity", "warning"),
            service=labels.get("service", "unknown-service"),
            namespace=labels.get("namespace"),
            summary=annotations.get("summary", labels.get("alertname", "Unknown alert")),
            description=annotations.get("description"),
        )
        self.db.add(incident)
        self.db.flush()

        for alert in payload.alerts:
            event = AlertEvent(
                incident_id=incident.id,
                fingerprint=alert.fingerprint,
                status=alert.status,
                labels=alert.labels,
                annotations=alert.annotations,
                starts_at=alert.startsAt,
                raw_payload=alert.model_dump(),
            )
            self.db.add(event)

        self.db.commit()
        self.db.refresh(incident)
        return incident

    def get_incident(self, incident_id: str) -> Incident | None:
        return self.db.query(Incident).filter(Incident.id == incident_id).first()

    def update_perception(self, incident_id: str, perception_output: dict) -> None:
        incident = self.get_incident(incident_id)
        if not incident:
            return
        agg = perception_output["aggregated_context"]
        incident.service = agg["service"]
        incident.severity = agg["severity"]
        incident.namespace = agg.get("namespace")
        incident.summary = agg["summary"]
        incident.description = agg.get("description")
        incident.perception_output = perception_output
        self.db.commit()

    def update_diagnosis(self, incident_id: str, diagnosis_output: dict) -> None:
        incident = self.get_incident(incident_id)
        if not incident:
            return
        incident.root_cause = diagnosis_output["root_cause"]
        incident.confidence = diagnosis_output["confidence"]
        incident.affected_services = diagnosis_output["affected_services"]
        incident.evidence = diagnosis_output["evidence"]
        incident.diagnosis_output = diagnosis_output
        self.db.commit()

    def update_remediation(self, incident_id: str, remediation_output: dict) -> None:
        incident = self.get_incident(incident_id)
        if not incident:
            return
        incident.remediation_output = remediation_output
        self.db.commit()

    def update_postmortem(self, incident_id: str, postmortem_output: dict) -> None:
        incident = self.get_incident(incident_id)
        if not incident:
            return
        incident.postmortem_output = postmortem_output
        incident.status = "resolved"
        self.db.commit()
