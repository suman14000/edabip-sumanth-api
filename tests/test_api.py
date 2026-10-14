from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "EDABIP Reports API is running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_get_reports():
    response = client.get("/api/reports")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_report_summary():
    response = client.get("/api/reports/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_reports" in data
    assert "completed_reports" in data
    assert "failed_reports" in data
    assert "scheduled_reports" in data
    assert "average_run_time" in data


def test_type_distribution():
    response = client.get(
        "/api/reports/type-distribution"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_status_distribution():
    response = client.get(
        "/api/reports/status-distribution"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)