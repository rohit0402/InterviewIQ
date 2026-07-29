from unittest.mock import patch
from app.tests.utils.auth import (
    unique_user,
    register,
)

from app.database.session import SessionLocal
from app.models.user import User
from app.models.email_verification_token import EmailVerificationToken


def test_verify_email_success(client):
    user = unique_user()

    with patch(
        "app.tasks.email_tasks.send_verification_email_task.delay"
    ) as mock_email:

        register(client, user)

        # The second argument to delay(email, token) is the raw token
        raw_token = mock_email.call_args.args[1]

    response = client.get(
        f"/api/v1/auth/verify-email?token={raw_token}"
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

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid verification token."

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

    with patch(
        "app.tasks.email_tasks.send_verification_email_task.delay"
    ) as mock_email:

        register(client, user)

        raw_token = mock_email.call_args.args[1]

    client.get(
        f"/api/v1/auth/verify-email?token={raw_token}"
    )

    response = client.get(
        f"/api/v1/auth/verify-email?token={raw_token}"
    )

    assert response.status_code in (400, 409)

def test_verify_email_clears_token(client):
    user = unique_user()
    with patch(
        "app.tasks.email_tasks.send_verification_email_task.delay"
    ) as mock_email:

        register(client, user)

        raw_token = mock_email.call_args.args[1]

    client.get(
        f"/api/v1/auth/verify-email?token={raw_token}"
    )

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(User.email == user["email"])
        .first()
    )

    verification = (
        db.query(EmailVerificationToken)
        .filter(
            EmailVerificationToken.user_id == db_user.id
        )
        .first()
    )

    assert verification.used is True

    db.close()

from app.tests.utils.auth import login

def test_login_after_email_verification(client):
    user = unique_user()
    with patch(
        "app.tasks.email_tasks.send_verification_email_task.delay"
    ) as mock_email:

        register(client, user)

        raw_token = mock_email.call_args.args[1]

    client.get(
        f"/api/v1/auth/verify-email?token={raw_token}"
    )
    response = login(
        client,
        user["email"],
        user["password"],
    )

    assert response.status_code == 200