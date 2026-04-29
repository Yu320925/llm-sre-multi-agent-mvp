from fastapi import FastAPI

from app.database import Base, engine
from app.routers.health import router as health_router
from app.routers.incidents import router as incidents_router
from app.routers.reports import router as reports_router
from app.routers.webhook import router as webhook_router
from app.utils.logging import setup_logging

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LLM SRE Multi-Agent MVP",
    version="1.0.0",
    description="智能 SRE 故障自动诊断与复盘 Multi-Agent MVP",
)

app.include_router(health_router)
app.include_router(webhook_router)
app.include_router(incidents_router)
app.include_router(reports_router)
