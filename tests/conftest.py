import os

# Provide a test-only secret before importing the application.
os.environ.setdefault(
    "JWT_SECRET_KEY",
    "pytest_only_secret_key_do_not_use_in_production_123456",
)
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite:///./test_edabip_reports.db",
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.core.security import hash_password, create_access_token
from app.models import Report, ReportActivity, ReportTemplate, ReportSchedule, User


@pytest.fixture()
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def viewer(test_db):
    user = User(
        name="Test Viewer",
        email="viewer@example.com",
        hashed_password=hash_password("ViewerPass123!"),
        role="Viewer",
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture()
def admin(test_db):
    user = User(
        name="Test Admin",
        email="admin@example.com",
        hashed_password=hash_password("AdminPass123!"),
        role="Admin",
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture()
def viewer_headers(viewer):
    token = create_access_token(viewer.id, viewer.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_headers(admin):
    token = create_access_token(admin.id, admin.role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def report_record(test_db):
    report = Report(
        report_name="Monthly Sales",
        module="Sales",
        report_type="Scheduled",
        owner="Sumanth",
        status="Completed",
        run_time_seconds=12.5,
    )
    test_db.add(report)
    test_db.commit()
    test_db.refresh(report)
    return report


@pytest.fixture()
def activity_record(test_db, report_record):
    activity = ReportActivity(
        report_id=report_record.id,
        activity_type="Execution",
        activity_status="Success",
        message="Report completed successfully",
        execution_time_seconds=12.5,
        executed_by="Test Admin",
    )
    test_db.add(activity)
    test_db.commit()
    test_db.refresh(activity)
    return activity