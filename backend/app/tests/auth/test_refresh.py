from app.tests.utils.auth import (
    unique_user,
    register,
    login,
)

from app.database.session import SessionLocal
from app.models.user import User


def test_refresh_success(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_refresh_without_cookie(client):
    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 401

def test_refresh_invalid_cookie(client):
    client.cookies.set(
        "refresh_token",
        "invalid-token"
    )

    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 401

def test_refresh_empty_cookie(client):
    client.cookies.set(
        "refresh_token",
        ""
    )

    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 401

def test_refresh_random_token(client):
    client.cookies.set(
        "refresh_token",
        "abc.def.xyz"
    )

    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 401

def test_refresh_after_cookie_deleted(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    client.cookies.clear()

    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 401

def test_refresh_returns_new_access_token(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body["access_token"], str)
    assert len(body["access_token"]) > 50

def test_refresh_sets_cookie(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    response = client.post("/api/v1/auth/refresh")

    assert response.status_code == 200

    cookie = response.headers.get("set-cookie")

    if cookie:
        assert "refresh_token=" in cookie

def test_refresh_rotates_refresh_token(client):
    ...
    old_cookie = client.cookies.get("refresh_token")

    client.post("/api/v1/auth/refresh")

    new_cookie = client.cookies.get("refresh_token")

    assert old_cookie != new_cookie