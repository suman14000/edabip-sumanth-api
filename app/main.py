from fastapi import FastAPI
from sqlalchemy import text
from app.config import APP_NAME
from app.database import engine
from app.routers import auth, reports, report_activity, report_schedules

app = FastAPI(title=APP_NAME, version="2.0.0",
              description="EDABIP Reports API with JWT authentication, roles, schedules and CSV export")

# Create tables in MySQL Workbench by running sql/database.sql before starting the API.

app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(report_activity.router)
app.include_router(report_schedules.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "EDABIP Reports API is running", "version": "2.0.0"}

@app.get("/health", tags=["Health"])
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}
