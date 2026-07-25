from datetime import datetime, timedelta

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True,)

    token_hash: Mapped[str] = mapped_column(String(64),nullable=False,unique=True)

    used: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False,)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.utcnow() + timedelta(hours=24),)

    user: Mapped["User"] = relationship("User")