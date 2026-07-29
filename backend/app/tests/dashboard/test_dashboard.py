from app.tests.utils.auth import authenticated_user


def test_get_dashboard(client):
    user, token = authenticated_user(client)

    response = client.get(
        "/api/v1/dashboard/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["resume_uploaded"] is False
    assert body["total_interviews"] == 0
    assert body["completed_interviews"] == 0
    assert body["in_progress_interviews"] == 0
    assert body["average_score"] is None
    assert body["recent_interviews"] == []


def test_get_dashboard_unauthorized(client):
    response = client.get("/api/v1/dashboard/")

    assert response.status_code == 401