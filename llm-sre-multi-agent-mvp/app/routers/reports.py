from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.postmortem_service import PostmortemService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{incident_id}")
def get_report(incident_id: str, db: Session = Depends(get_db)) -> dict:
    service = PostmortemService(db)
    report = service.get_report_by_incident_id(incident_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "incident_id": incident_id,
        "markdown": report.markdown,
        "timeline": report.timeline,
        "metadata": report.metadata,
    }
