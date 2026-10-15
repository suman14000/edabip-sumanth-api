def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "EDABIP Reports API is running"


def test_reports_without_token_return_401(client):
    response = client.get("/api/reports")
    assert response.status_code == 401


def test_viewer_can_read_reports(
    client, viewer_headers, report_record
):
    response = client.get(
        "/api/reports",
        headers=viewer_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_viewer_cannot_rerun_report(
    client, viewer_headers, report_record
):
    response = client.post(
        f"/api/reports/{report_record.id}/rerun",
        headers=viewer_headers,
    )

    assert response.status_code == 403


def test_invalid_report_input_returns_422(client, admin_headers):
    response = client.post(
        "/api/reports",
        headers=admin_headers,
        json={
            "report_name": "",
            "module": "Sales",
            "report_type": "Scheduled",
            "owner": "Test",
            "status": "Completed",
            "run_time_seconds": 5,
        },
    )

    assert response.status_code == 422


def test_missing_report_returns_404(client, viewer_headers):
    response = client.get(
        "/api/reports/999999",
        headers=viewer_headers,
    )

    assert response.status_code == 404


def test_csv_export_has_expected_header(
    client, viewer_headers, activity_record
):
    response = client.get(
        "/api/report-activity/export/csv",
        headers=viewer_headers,
    )

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]

    first_line = response.text.splitlines()[0]

    assert first_line == (
        "id,report_id,activity_type,activity_status,message,"
        "execution_time_seconds,executed_by,created_at"
    )


def test_register_and_login(client):
    registration = client.post(
        "/api/auth/register",
        json={
            "name": "New Viewer",
            "email": "newviewer@example.com",
            "password": "StrongPass123!",
        },
    )

    assert registration.status_code == 201
    assert registration.json()["role"] == "Viewer"
    assert "hashed_password" not in registration.json()

    login = client.post(
        "/api/auth/login",
        json={
            "email": "newviewer@example.com",
            "password": "StrongPass123!",
        },
    )

    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert login.json()["access_token"]


def test_wrong_password_returns_401(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Login Test",
            "email": "login@example.com",
            "password": "StrongPass123!",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "WrongPass123!",
        },
    )

    assert response.status_code == 401


def test_admin_can_rerun_report(
    client, admin_headers, report_record
):
    response = client.post(
        f"/api/reports/{report_record.id}/rerun",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Scheduled"


def test_activity_list_requires_token(client):
    response = client.get("/api/report-activity")
    assert response.status_code == 401


def test_invalid_sort_column_returns_422(client, viewer_headers):
    response = client.get(
        "/api/reports?sort_by=not_a_column",
        headers=viewer_headers,
    )

    assert response.status_code == 422