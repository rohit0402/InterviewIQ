from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Integer,String,Text
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

from app.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.interview import Interview
    from app.models.interview_answer import InterviewAnswer
    from app.models.interview_question_insight import InterviewQuestionInsight


class InterviewQuestion(Base):
    __tablename__= "interview_questions"

    id:Mapped[int]=mapped_column(primary_key=True)
    interview_id:Mapped[int]=mapped_column(ForeignKey("interviews.id",ondelete="CASCADE"),nullable=False,index=True)
    question:Mapped[str]=mapped_column(Text,nullable=False)
    topic:Mapped[str]=mapped_column(String(100),nullable=False)
    difficulty:Mapped[str]=mapped_column(String(100),nullable=False)
    sequence:Mapped[int]=mapped_column(Integer,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    interview:Mapped["Interview"]=relationship("Interview",back_populates="questions")
    answer: Mapped["InterviewAnswer"] = relationship("InterviewAnswer",back_populates="question",uselist=False,cascade="all, delete-orphan",single_parent=True,)
    insight: Mapped["InterviewQuestionInsight"] = relationship("InterviewQuestionInsight",back_populates="question",uselist=False,cascade="all, delete-orphan",single_parent=True,)