from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.interview import Interview


class InterviewAnalysis(Base):
    __tablename__ = "interview_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    interview_id: Mapped[int] = mapped_column(ForeignKey("interviews.id", ondelete="CASCADE"),unique=True,nullable=False,)

    matching_skills: Mapped[list] = mapped_column(JSONB)

    missing_skills: Mapped[list] = mapped_column(JSONB)

    strengths: Mapped[list] = mapped_column(JSONB)

    weaknesses: Mapped[list] = mapped_column(JSONB)

    overall_feedback: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.utcnow,)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow,)

    interview = relationship("Interview",back_populates="analysis",
    )