from sqlalchemy.orm import Session

from app.models import PostmortemReport


class PostmortemService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_report(self, incident_id: str, report: dict) -> None:
        existing = self.get_report_by_incident_id(incident_id)
        if existing:
            existing.markdown = report["markdown"]
            existing.timeline = report["timeline"]
            existing.metadata = report["metadata"]
            self.db.commit()
            return

        row = PostmortemReport(
            incident_id=incident_id,
            markdown=report["markdown"],
            timeline=report["timeline"],
            metadata=report["metadata"],
        )
        self.db.add(row)
        self.db.commit()

    def get_report_by_incident_id(self, incident_id: str) -> PostmortemReport | None:
        return self.db.query(PostmortemReport).filter(PostmortemReport.incident_id == incident_id).first()
