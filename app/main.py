from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers import report_activity
from app.routers import report_templates
from app.routers import reports

# Import models so SQLAlchemy knows about all models.
from app.models import report
from app.models import report_activity as report_activity_model
from app.models import report_template


app = FastAPI(
    title="EDABIP Reports API",
    description="Backend API for EDABIP Reports Module",
    version="1.0.0"
)


app.include_router(
    reports.router
)

app.include_router(
    report_templates.router
)

app.include_router(
    report_activity.router
)


@app.get(
    "/",
    tags=["Health"]
)
def root():
    return {
        "message": "EDABIP Reports API is running"
    }


@app.get(
    "/health",
    tags=["Health"]
)
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(exc)
        }