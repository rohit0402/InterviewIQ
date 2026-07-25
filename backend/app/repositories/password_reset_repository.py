from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.password_reset_token import PasswordResetToken


class PasswordResetRepository:

    @staticmethod
    def create(
        db: Session,
        token: PasswordResetToken,
    ) -> PasswordResetToken:
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    @staticmethod
    def get_by_hash(
        db: Session,
        token_hash: str,
    ) -> PasswordResetToken | None:
        stmt = select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash
        )
        return db.scalar(stmt)

    @staticmethod
    def invalidate_user_tokens(
        db: Session,
        user_id: int,
    ):
        tokens = (
            db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used == False,
            )
            .all()
        )

        for token in tokens:
            token.used = True

        db.commit()

    @staticmethod
    def mark_used(
        db: Session,
        token: PasswordResetToken,
    ):
        token.used = True
        db.commit()
        db.refresh(token)
        return token