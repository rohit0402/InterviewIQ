from app.tests.utils.auth import (
    unique_user,
    register,
    login,
)

from app.database.session import SessionLocal
from app.models.user import User

def test_reset_password_success(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    db_user.is_verified = True

    db.commit()

    client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"]
        },
    )

    db.refresh(db_user)

    token = db_user.reset_password_token

    db.close()

    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!"
        },
    )

    assert response.status_code == 200

def test_login_after_password_reset(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    db_user.is_verified = True

    db.commit()

    client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"]
        },
    )

    db.refresh(db_user)

    token = db_user.reset_password_token

    db.close()

    client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!"
        },
    )

    response = login(
        client,
        user["email"],
        "NewPassword123!",
    )

    assert response.status_code == 200

def test_old_password_fails_after_reset(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    db_user.is_verified = True

    db.commit()

    client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"]
        },
    )

    db.refresh(db_user)

    token = db_user.reset_password_token

    db.close()

    client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!"
        },
    )

    response = login(
        client,
        user["email"],
        user["password"],
    )

    assert response.status_code == 401

def test_reset_password_invalid_token(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": "invalid-token",
            "new_password": "NewPassword123!"
        },
    )

    assert response.status_code == 400

def test_reset_password_missing_token(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "new_password": "NewPassword123!"
        },
    )

    assert response.status_code == 422

def test_reset_password_missing_password(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": "abc"
        },
    )

    assert response.status_code == 422

def test_reset_password_empty_password(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": "abc",
            "new_password": ""
        },
    )

    assert response.status_code in (400, 422)

def test_reset_password_clears_token(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    db_user.is_verified = True

    db.commit()

    client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"]
        },
    )

    db.refresh(db_user)

    token = db_user.reset_password_token

    client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123!"
        },
    )

    db.refresh(db_user)

    assert db_user.reset_password_token is None

    db.close()