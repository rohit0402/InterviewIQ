from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Float,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.sql import func

from app.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.interview_question import InterviewQuestion

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"
    id:Mapped[int]=mapped_column(primary_key=True)
    interview_question_id:Mapped[int]=mapped_column(ForeignKey("interview_questions.id",ondelete="CASCADE"),nullable=False,unique=True,index=True)
    answer:Mapped[str]=mapped_column(Text,nullable=False)
    score:Mapped[float|None]=mapped_column(Float,nullable=True)
    feedback:Mapped[str|None]=mapped_column(Text,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    question:Mapped["InterviewQuestion"]=relationship("InterviewQuestion",back_populates="answer")