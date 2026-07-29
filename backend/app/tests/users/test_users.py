from app.tests.utils.auth import (
    unique_user,
    register,
    login, 
)
from app.tests.utils.db import verify_user

from app.database.session import SessionLocal
from app.models.user import User


def test_get_current_user(client):
    user = unique_user()

    register(client, user)

    verify_user(user["email"])

    login_response = login(
        client,
        user["email"],
        user["password"],
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email"] == user["email"]
    assert body["full_name"] == user["full_name"]


def test_get_current_user_without_token(client):
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401

def test_admin_dashboard(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    db_user.is_verified = True
    db_user.role = "admin"

    db.commit()
    db.close()

    login_response = login(
        client,
        user["email"],
        user["password"],
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "admin dashboard"
    assert body["user"] == user["full_name"]

def test_admin_dashboard_forbidden(client):
    user = unique_user()

    register(client, user)

    verify_user(user["email"])

    login_response = login(
        client,
        user["email"],
        user["password"],
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403

def test_admin_dashboard_without_token(client):
    response = client.get("/api/v1/users/admin")

    assert response.status_code == 401

def test_admin_dashboard_invalid_token(client):
    response = client.get(
        "/api/v1/users/admin",
        headers={
            "Authorization": "Bearer abc"
        },
    )

    assert response.status_code == 401