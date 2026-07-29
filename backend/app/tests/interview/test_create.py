

def test_create_interview(client, ready_user, monkeypatch):
    monkeypatch.setattr(
        "app.services.interview_service.process_interview_task.delay",
        lambda interview_id: None,
    )

    response = client.post(
        "/api/v1/interviews/",
        headers={"Authorization": f"Bearer {ready_user.token}"},
        json={
            "company_name": "Google",
            "job_role": "Software Engineer",
            "experience_level": "Fresher",
            "job_description": "Backend Developer",
        },

    )

    assert response.status_code == 202

    body = response.json()

    assert body["company_name"] == "Google"
    assert body["job_role"] == "Software Engineer"

def test_create_interview_unauthorized(client):
    response = client.post(
        "/api/v1/interviews/",
        json={
            "company_name": "Google",
            "job_role": "SDE",
            "experience_level": "Fresher",
            "job_description": "Backend",
        },
    )

    assert response.status_code == 401

def test_get_my_interviews(client, ready_user):
    response = client.get(
        "/api/v1/interviews/",
        headers={
            "Authorization": f"Bearer {ready_user.token}"
        },
    )

    assert response.status_code == 200

def test_get_interview(client, ready_interview):
    response = client.get(
        f"/api/v1/interviews/{ready_interview.id}",
        headers={
            "Authorization": f"Bearer {ready_interview.token}"
        },
    )

    assert response.status_code == 200

def test_get_interview_not_found(client, ready_user):
    response = client.get(
        "/api/v1/interviews/999999",
        headers={
            "Authorization": f"Bearer {ready_user.token}"
        },
    )

    assert response.status_code == 404

def test_delete_interview(client, ready_interview):
    response = client.delete(
        f"/api/v1/interviews/{ready_interview.id}",
        headers={
            "Authorization": f"Bearer {ready_interview.token}"
        },
    )

    assert response.status_code == 204

def test_start_interview(client, ready_interview, mock_ai):

    response = client.post(
        f"/api/v1/interviews/{ready_interview.id}/start",
        headers={
            "Authorization": f"Bearer {ready_interview.token}"
        },
    )

    assert response.status_code in (200, 201), response.json()
def test_submit_answer(client, ready_question, mock_ai):

    response = client.post(
        f"/api/v1/interviews/question/{ready_question.id}/answer",
        headers={
            "Authorization": f"Bearer {ready_question.token}"
        },
        json={
            "answer": "My answer"
        },
    )

    assert response.status_code == 200

def test_finish_interview(client, ready_finished_interview):

    response = client.post(
        f"/api/v1/interviews/{ready_finished_interview.id}/finish",
        headers={
            "Authorization": f"Bearer {ready_finished_interview.token}"
        },
    )

    assert response.status_code == 202

def test_interview_status(client, ready_interview):
    response = client.get(
        f"/api/v1/interviews/{ready_interview.id}/status",
        headers={
            "Authorization": f"Bearer {ready_interview.token}"
        },
    )

    assert response.status_code == 200

    assert "status" in response.json()