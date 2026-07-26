from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interview_question import InterviewQuestion

class InterviewQuestionInsight(Base):
    __tablename__ = "interview_question_insights"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    interview_question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "interview_questions.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    ideal_answer: Mapped[str]

    key_learning_points: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    question: Mapped["InterviewQuestion"] = relationship(
    "InterviewQuestion",
    back_populates="insight",
)