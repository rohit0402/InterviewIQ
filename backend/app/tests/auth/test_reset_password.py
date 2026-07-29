from app.tests.utils.auth import (
    unique_user,
    register,
    login,
)
from app.email.token_service import TokenService
from unittest.mock import patch
from app.models.password_reset_token import PasswordResetToken
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

    with patch(
        "app.tasks.email_tasks.send_password_reset_email_task.delay"
    ) as mock_email:

        client.post(
            "/api/v1/auth/forgot-password",
            json={
                "email": user["email"]
            },
        )

        raw_token = mock_email.call_args.args[1]

    db.close()

    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "password": "NewPassword123!"
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

    with patch(
        "app.tasks.email_tasks.send_password_reset_email_task.delay"
    ) as mock_email:

        client.post(
            "/api/v1/auth/forgot-password",
            json={
                "email": user["email"]
            },
        )

        raw_token = mock_email.call_args.args[1]

    db.close()

    client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "password": "NewPassword123!"
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

    with patch(
        "app.tasks.email_tasks.send_password_reset_email_task.delay"
    ) as mock_email:

        client.post(
            "/api/v1/auth/forgot-password",
            json={
                "email": user["email"]
            },
        )

        raw_token = mock_email.call_args.args[1]

    db.close()

    client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "password": "NewPassword123!"
        },
    )

    response = login(
        client,
        user["email"],
        user["password"],
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_reset_password_invalid_token(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": "invalid-token",
            "password": "NewPassword123!"
        },
    )

    assert response.status_code == 400

def test_reset_password_missing_token(client):
    response = client.post(
        "/api/v1/auth/reset-password",
        json={
            "password": "NewPassword123!"
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
            "password": ""
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

    with patch(
        "app.tasks.email_tasks.send_password_reset_email_task.delay"
    ) as mock_email:

        client.post(
            "/api/v1/auth/forgot-password",
            json={
                "email": user["email"]
            },
        )

        raw_token = mock_email.call_args.args[1]

    client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "password": "NewPassword123!"
        },
    )

    db.refresh(db_user)

    token_hash = TokenService.hash_token(raw_token)

    verification = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash
        )
        .first()
    )

    assert verification is not None
    assert verification.used is True


    db.close()