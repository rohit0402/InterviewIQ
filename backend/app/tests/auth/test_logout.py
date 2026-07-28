from app.tests.utils.auth import (
    unique_user,
    register,
    login,
)

from app.database.session import SessionLocal
from app.models.user import User


def test_logout_success(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200

def test_logout_without_cookie(client):
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 401

def test_logout_invalid_cookie(client):
    client.cookies.set(
        "refresh_token",
        "invalid-token"
    )

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 401

def test_logout_clears_cookie(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200

    cookie = response.headers.get("set-cookie")

    assert cookie is not None
    assert "refresh_token=" in cookie
    assert "Max-Age=0" in cookie or "expires=" in cookie.lower()

def test_refresh_after_logout_fails(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    logout = client.post("/api/v1/auth/logout")

    assert logout.status_code == 200

    refresh = client.post("/api/v1/auth/refresh")

    assert refresh.status_code == 401

def test_double_logout(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    client.post("/api/v1/auth/logout")

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 401

def test_logout_removes_refresh_token_from_db(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    login(client, user["email"], user["password"])

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()

    assert db_user.refresh_token is None

    db.close()