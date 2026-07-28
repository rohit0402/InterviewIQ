import uuid

def unique_user_data():
    uid = uuid.uuid4().hex[:8]

    return {
        "username": f"user_{uid}",
        "email": f"{uid}@test.com",
        "password": "Password@123"
    }