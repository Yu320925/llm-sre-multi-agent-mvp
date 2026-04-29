from sqlalchemy.orm import Session

from app.models import RemediationPlan


class RemediationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_plan(self, incident_id: str, remediation: dict) -> None:
        plan = RemediationPlan(
            incident_id=incident_id,
            title=remediation["title"],
            actions=remediation["actions"],
            script=remediation["script"],
            approval_required=remediation["approval_required"],
            risk=remediation["risk"],
        )
        self.db.add(plan)
        self.db.commit()
