from app.tests.utils.auth import register, unique_user
from unittest.mock import patch
@patch("app.services.auth_service.send_verification_email_task.delay")
def test_register_success(mock_delay,client):
    user = unique_user()

    response = register(client, user)

    assert response.status_code == 201

    body = response.json()
    assert isinstance(body["id"],int)
    assert body["email"] == user["email"]
    assert body["full_name"] == user["full_name"]
    assert body["is_active"] is True
    assert body["is_verified"] is False

    assert "created_at" in body
    assert "updated_at" in body

    mock_delay.assert_called_once()

@patch("app.services.auth_service.send_verification_email_task.delay")
def test_register_duplicate_email(mock_delay,client):
    user = unique_user()
    register(client, user)
    mock_delay.reset_mock()
    response = register(client, user)
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"
    mock_delay.assert_not_called()

def test_register_invalid_email(client):
    user = unique_user()

    user["email"] = "abc"

    response = register(client, user)

    assert response.status_code == 422

def test_register_missing_email(client):
    user = unique_user()

    del user["email"]

    response = register(client, user)

    assert response.status_code == 422

def test_register_missing_password(client):
    user = unique_user()

    del user["password"]

    response = register(client, user)

    assert response.status_code == 422

def test_register_missing_full_name(client):
    user = unique_user()

    del user["full_name"]

    response = register(client, user)

    assert response.status_code == 422

def test_register_empty_full_name(client):
    user = unique_user()

    user["full_name"] = ""

    response = register(client, user)

    assert response.status_code in (400, 422)


def test_register_empty_payload(client):
    response = client.post(
        "/api/v1/auth/register",
        json={},
    )

    assert response.status_code == 422

def test_register_invalid_json(client):
    response = client.post(
        "/api/v1/auth/register",
        data="invalid",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422