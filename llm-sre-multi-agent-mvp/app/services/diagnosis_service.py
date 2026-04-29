from sqlalchemy.orm import Session

from app.models import DiagnosisTrace


class DiagnosisService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_trace(self, incident_id: str, trace: list[dict]) -> None:
        for item in trace:
            row = DiagnosisTrace(
                incident_id=incident_id,
                step=item["step"],
                hypothesis=item["hypothesis"],
                action=item["action"],
                observation=item["observation"],
                conclusion=item.get("conclusion"),
                tool_name=item.get("tool_name"),
                tool_input=item.get("tool_input"),
                tool_output=item.get("tool_output"),
            )
            self.db.add(row)
        self.db.commit()
