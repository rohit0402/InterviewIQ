from app.tests.utils.auth import authenticated_user


def test_create_interview_unauthorized(client):
    response = client.post(
        "/api/v1/interviews/",
        json={
            "company_name": "Google",
            "job_role": "Software Engineer",
            "experience_level": "Fresher",
            "job_description": "Backend Developer",
        },
    )

    assert response.status_code == 401


def test_get_my_interviews_unauthorized(client):
    response = client.get("/api/v1/interviews/")

    assert response.status_code == 401


def test_get_interview_not_found(client):
    _, token = authenticated_user(client)

    response = client.get(
        "/api/v1/interviews/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found."


def test_delete_interview_not_found(client):
    _, token = authenticated_user(client)

    response = client.delete(
        "/api/v1/interviews/999999",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found."


def test_finish_interview_not_found(client):
    _, token = authenticated_user(client)

    response = client.post(
        "/api/v1/interviews/999999/finish",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found."


def test_get_status_not_found(client):
    _, token = authenticated_user(client)

    response = client.get(
        "/api/v1/interviews/999999/status",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    # Your current implementation doesn't check for None before interview.user_id,
    # so this may currently return 500 instead of 404.
    # After fixing the router, keep this assertion:
    assert response.status_code == 404
    assert response.json()["detail"] == "Interview not found."


