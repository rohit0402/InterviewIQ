from app.tests.utils.auth import (
    unique_user,
    register,
)

from app.database.session import SessionLocal
from app.models.user import User

def test_forgot_password_success(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    db_user.is_verified = True

    db.commit()
    db.close()

    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"]
        },
    )

    assert response.status_code == 200


def test_forgot_password_unknown_email(client):
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": "unknown@test.com"
        },
    )

    assert response.status_code == 404

def test_forgot_password_invalid_email(client):
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": "abc"
        },
    )

    assert response.status_code == 422

def test_forgot_password_missing_email(client):
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={}
    )

    assert response.status_code == 422

def test_forgot_password_empty_email(client):
    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": ""
        },
    )

    assert response.status_code in (400, 422)

def test_forgot_password_creates_reset_token(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    db_user.is_verified = True

    db.commit()
    db.close()

    response = client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"]
        },
    )

    assert response.status_code == 200

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    assert db_user.reset_password_token is not None

    db.close()



def test_forgot_password_creates_token_expiry(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    db_user.is_verified = True

    db.commit()
    db.close()

    client.post(
        "/api/v1/auth/forgot-password",
        json={
            "email": user["email"]
        },
    )

    db = SessionLocal()

    db_user = db.query(User).filter(
        User.email == user["email"]
    ).first()

    assert db_user.reset_password_token_expires_at is not None

    db.close()