from app.tests.utils.auth import (
    unique_user,
    register,
    login,
)


def test_login_success(client):
    user = unique_user()

    register(client, user)

    # Verify email (replace with your helper if available)
    from app.database.session import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    response = login(client, user["email"], user["password"])

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"

    assert "refresh_token" in response.cookies


def test_login_wrong_password(client):
    user = unique_user()

    register(client, user)

    from app.database.session import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    response = login(
        client,
        user["email"],
        "WrongPassword123"
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid email or password"

def test_login_unknown_email(client):
    response = login(
        client,
        "unknown@test.com",
        "password123"
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid email or password"


def test_login_unverified_email(client):
    user = unique_user()

    register(client, user)

    response = login(
        client,
        user["email"],
        user["password"]
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Please verify your email before logging in."

def test_login_missing_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "password": "password123"
        },
    )

    assert response.status_code == 422


def test_login_missing_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "abc@test.com"
        },
    )

    assert response.status_code == 422

def test_login_empty_payload(client):
    response = client.post(
        "/api/v1/auth/login",
        json={}
    )

    assert response.status_code == 401

def test_login_empty_payload(client):
    response = client.post(
        "/api/v1/auth/login",
        json={}
    )

    assert response.status_code == 422

def test_login_empty_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "abc@test.com",
            "password": ""
        },
    )

    assert response.status_code in (400, 401, 422)

def test_login_sets_refresh_cookie(client):
    user = unique_user()

    register(client, user)

    from app.database.session import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user["email"]).first()
    db_user.is_verified = True
    db.commit()
    db.close()

    response = login(
        client,
        user["email"],
        user["password"]
    )

    assert response.status_code == 200

    cookie = response.headers.get("set-cookie")

    assert cookie is not None
    assert "refresh_token=" in cookie
    assert "HttpOnly" in cookie