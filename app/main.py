from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers import (
    auth,
    report_activity,
    report_schedules,
    report_templates,
    reports,
)

app = FastAPI(
    title="EDABIP Reports API",
    description="Reports API with JWT authentication, roles, schedules and CSV export",
    version="2.0.0",
)

app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(report_templates.router)
app.include_router(report_activity.router)
app.include_router(report_schedules.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "EDABIP Reports API is running",
        "version": "2.0.0",
    }


@app.get("/health", tags=["Health"])
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "healthy", "database": "connected"}

    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}