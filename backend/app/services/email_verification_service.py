from fastapi import HTTPException
from datetime import datetime, timezone
from app.email.token_service import TokenService
from app.models.email_verification_token import (
    EmailVerificationToken,
)
from app.repositories.email_verification_repository import (
    EmailVerificationRepository,
)
from app.email.email_service import EmailService
from app.repositories.user_repository import UserRepository


class EmailVerificationService:

    @staticmethod
    def create_token(
        db,
        user,
    ) -> str:

        EmailVerificationRepository.invalidate_user_tokens(
            db,
            user.id,
        )

        raw_token, token_hash = (
            TokenService.generate_token()
        )

        EmailVerificationRepository.create(
            db,
            EmailVerificationToken(
                user_id=user.id,
                token_hash=token_hash,
            ),
        )

        return raw_token

    @staticmethod
    def verify_token(
        db,
        token: str,
    ):

        token_hash = TokenService.hash_token(token)

        verification = (
            EmailVerificationRepository.get_by_hash(
                db,
                token_hash,
            )
        )

        if verification is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid verification token.",
            )

        if verification.used:
            raise HTTPException(
                status_code=400,
                detail="Token already used.",
            )

        if verification.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=400,
                detail="Token expired.",
            )

        user = UserRepository.get_by_id(
            db,
            verification.user_id,
        )

        user.is_verified = True

        verification.used = True

        db.commit()

        return user

    @staticmethod
    def resend_verification(
        db,
        email,
    ):
        user = UserRepository.get_by_email(
            db,
            email,
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        if user.is_verified:
            raise ValueError(
                "Email already verified."
            )

        token = EmailVerificationService.create_token(
            db,
            user,
        )

        EmailService.send_verification_email(
            user.email,
            token,
        )

        return {
            "message":
            "Verification email sent."
        }