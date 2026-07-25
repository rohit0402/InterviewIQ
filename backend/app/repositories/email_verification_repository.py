from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.email_verification_token import EmailVerificationToken


class EmailVerificationRepository:

    @staticmethod
    def create(
        db: Session,
        token: EmailVerificationToken,
    ) -> EmailVerificationToken:
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    @staticmethod
    def get_by_hash(
        db: Session,
        token_hash: str,
    ) -> EmailVerificationToken | None:
        stmt = select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == token_hash
        )
        return db.scalar(stmt)

    @staticmethod
    def mark_used(db: Session, token):
        token.used = True
        db.commit()
        db.refresh(token)
        return token

    @staticmethod
    def invalidate_user_tokens(
        db: Session,
        user_id: int,
    ):
        tokens = (
            db.query(EmailVerificationToken)
            .filter(
                EmailVerificationToken.user_id == user_id,
                EmailVerificationToken.used == False,
            )
            .all()
        )

        for token in tokens:
            token.used = True

        db.commit()