from app.models.user import User
from app.core.security import hash_password


def create_user(
    db,
    *,
    verified=True,
    password="Password@123",
    email="test@example.com",
    full_name="Test User",
):
    user = User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
        is_verified=verified,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user