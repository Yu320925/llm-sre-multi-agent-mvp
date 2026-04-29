import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.alert import AlertWebhookRequest, AlertWebhookResponse
from app.services.incident_service import IncidentService
from app.workflows.incident_workflow import IncidentWorkflow

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/alerts", response_model=AlertWebhookResponse)
def receive_alerts(payload: AlertWebhookRequest, db: Session = Depends(get_db)) -> AlertWebhookResponse:
    incident_service = IncidentService(db)
    workflow = IncidentWorkflow(db)

    incident = incident_service.create_incident_from_alerts(payload)
    workflow.run(incident.id, payload)

    logger.info("Incident processed: %s", incident.id)

    return AlertWebhookResponse(
        incident_id=incident.id,
        status="processing",
        message="Incident created and workflow started",
    )
