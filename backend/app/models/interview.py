from datetime import datetime
from sqlalchemy import  Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship,mapped_column,Mapped
from sqlalchemy.dialects.postgresql import JSONB
from typing import TYPE_CHECKING
from app.database.base import Base
from app.core.enum import  InterviewStatus

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.resume import Resume
    from app.models.interview_analysis import InterviewAnalysis
    from app.models.interview_question import InterviewQuestion
    from app.models.interview_report import InterviewReport


class Interview(Base):
    __tablename__ = "interviews"
    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    resume_id:Mapped[int]=mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"),nullable=False)
    company_name:Mapped[str]=mapped_column(String(255),nullable=False)
    job_role:Mapped[str]=mapped_column(String(255),nullable=False)
    experience_level:Mapped[str]=mapped_column(String(255),nullable=False)
    job_description:Mapped[str]=mapped_column(Text,nullable=False)
    required_skills:Mapped[list[str]]=mapped_column(JSONB,nullable=False,default=list)
    match_score:Mapped[float | None]=mapped_column(Float,nullable=True)
    status:Mapped[InterviewStatus]=mapped_column(default=InterviewStatus.CREATED,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,)

    user:Mapped["User"]=relationship("User",back_populates="interviews")
    resume:Mapped["Resume"]=relationship("Resume",back_populates="interviews")
    analysis:Mapped["InterviewAnalysis"]=relationship("InterviewAnalysis",back_populates="interview",uselist=False,cascade="all,delete-orphan")
    questions:Mapped[list["InterviewQuestion"]]=relationship("InterviewQuestion",back_populates="interview",cascade="all,delete-orphan")
    report:Mapped["InterviewReport"]=relationship("InterviewReport",back_populates="interview",uselist=False)