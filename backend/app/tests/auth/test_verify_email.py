from app.tests.utils.auth import (
    unique_user,
    register,
)

from app.database.session import SessionLocal
from app.models.user import User


def test_verify_email_success(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    token = db_user.verification_token

    db.close()

    response = client.get(
        f"/api/v1/auth/verify-email?token={token}"
    )

    assert response.status_code == 200

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    assert db_user.is_verified is True

    db.close()

def test_verify_email_invalid_token(client):
    response = client.get(
        "/api/v1/auth/verify-email?token=invalid-token"
    )

    assert response.json()["detail"] == "Invalid verification token"
    assert response.status_code == 400

def test_verify_email_missing_token(client):
    response = client.get(
        "/api/v1/auth/verify-email"
    )

    assert response.status_code == 422

def test_verify_email_empty_token(client):
    response = client.get(
        "/api/v1/auth/verify-email?token="
    )

    assert response.status_code in (400, 422)

def test_verify_email_already_verified(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    token = db_user.verification_token

    db.close()

    client.get(
        f"/api/v1/auth/verify-email?token={token}"
    )

    response = client.get(
        f"/api/v1/auth/verify-email?token={token}"
    )

    assert response.status_code in (400, 409)

def test_verify_email_clears_token(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    token = db_user.verification_token

    db.close()

    client.get(
        f"/api/v1/auth/verify-email?token={token}"
    )

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    assert db_user.verification_token is None

    db.close()

from app.tests.utils.auth import login

def test_login_after_email_verification(client):
    user = unique_user()

    register(client, user)

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    token = db_user.verification_token

    db.close()

    client.get(
        f"/api/v1/auth/verify-email?token={token}"
    )

    response = login(
        client,
        user["email"],
        user["password"],
    )

    assert response.status_code == 200