from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.email.email_service import EmailService
from app.email.token_service import TokenService
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from datetime import datetime, timezone
from app.repositories.password_reset_repository import (
    PasswordResetRepository,
)
from app.repositories.user_repository import UserRepository


class PasswordResetService:

    @staticmethod
    def create_token(
        db: Session,
        user: User,
    ) -> str:
        """
        Generate a new password reset token.

        Any previously active reset tokens for this user
        are invalidated before creating a new one.
        """

        PasswordResetRepository.invalidate_user_tokens(
            db,
            user.id,
        )

        raw_token, token_hash = TokenService.generate_token()

        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
        )

        PasswordResetRepository.create(
            db,
            reset_token,
        )

        return raw_token

    @staticmethod
    def forgot_password(
        db: Session,
        email: str,
    ):
        """
        Send a password reset email if the user exists.

        Always returns the same response so attackers
        cannot determine whether an email exists.
        """

        user = UserRepository.get_by_email(
            db,
            email,
        )

        if user:
            token = PasswordResetService.create_token(
                db,
                user,
            )

            EmailService.send_password_reset_email(
                user.email,
                token,
            )

        return {
            "message": (
                "If an account exists, a password reset "
                "email has been sent."
            )
        }

    @staticmethod
    def reset_password(
        db: Session,
        token: str,
        new_password: str,
    ):
        """
        Validate reset token and update password.
        """

        token_hash = TokenService.hash_token(token)

        reset_token = PasswordResetRepository.get_by_hash(
            db,
            token_hash,
        )

        if reset_token is None:
            raise ValueError("Invalid reset token")

        if reset_token.used:
            raise ValueError("Reset token has already been used")

        current_time = datetime.now(timezone.utc)

        if reset_token.expires_at < current_time:
            raise ValueError("Reset token has expired")

        user = reset_token.user

        user.hashed_password = hash_password(
            new_password,
        )

        # Logout from every device
        user.refresh_token = None

        PasswordResetRepository.mark_used(
            db,
            reset_token,
        )

        db.commit()
        db.refresh(user)

        return {
            "message": "Password reset successfully"
        }