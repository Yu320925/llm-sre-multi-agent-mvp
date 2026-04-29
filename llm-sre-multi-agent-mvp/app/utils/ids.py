import uuid


def generate_incident_id() -> str:
    return f"inc_{uuid.uuid4().hex[:10]}"
