from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False, default="processing")
    source = Column(String, nullable=False)
    severity = Column(String, nullable=False, default="warning")
    service = Column(String, nullable=False, index=True)
    namespace = Column(String, nullable=True)
    summary = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    root_cause = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    affected_services = Column(JSON, nullable=True)
    evidence = Column(JSON, nullable=True)

    perception_output = Column(JSON, nullable=True)
    diagnosis_output = Column(JSON, nullable=True)
    remediation_output = Column(JSON, nullable=True)
    postmortem_output = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AlertEvent(Base):
    __tablename__ = "alert_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(String, index=True, nullable=False)
    fingerprint = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)
    labels = Column(JSON, nullable=False)
    annotations = Column(JSON, nullable=True)
    starts_at = Column(String, nullable=True)
    raw_payload = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DiagnosisTrace(Base):
    __tablename__ = "diagnosis_traces"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(String, index=True, nullable=False)
    step = Column(Integer, nullable=False)
    hypothesis = Column(Text, nullable=False)
    action = Column(Text, nullable=False)
    observation = Column(Text, nullable=False)
    conclusion = Column(Text, nullable=True)
    tool_name = Column(String, nullable=True)
    tool_input = Column(JSON, nullable=True)
    tool_output = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RemediationPlan(Base):
    __tablename__ = "remediation_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    actions = Column(JSON, nullable=False)
    script = Column(Text, nullable=True)
    approval_required = Column(Boolean, nullable=False, default=True)
    risk = Column(String, nullable=False, default="medium")

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PostmortemReport(Base):
    __tablename__ = "postmortem_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(String, index=True, nullable=False, unique=True)
    markdown = Column(Text, nullable=False)
    timeline = Column(JSON, nullable=False)
    metadata = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
