import uuid

from app.core.config import settings
from app.tests.utils.db import verify_user
API = settings.api_v1_prefix


def unique_user():
    uid = uuid.uuid4().hex[:8]

    return {
        "full_name": f"Test User {uid}",
        "email": f"{uid}@example.com",
        "password": "Password@123",
    }


def register(client, data):
    return client.post(
        f"{API}/auth/register",
        json=data,
    )


def login(client, email, password):
    return client.post(
        f"{API}/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


def refresh(client):
    return client.post(f"{API}/auth/refresh")


def logout(client):
    return client.post(f"{API}/auth/logout")

def authenticated_user(client):
    user = unique_user()

    register(client, user)
    verify_user(user["email"])

    token = login(
        client,
        user["email"],
        user["password"],
    ).json()["access_token"]

    return user, token