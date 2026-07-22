from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Float,Text,Column,Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship,Mapped
from sqlalchemy.sql import func

from app.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.interview import Interview

    
class InterviewReport(Base):
    __tablename__ = "interview_reports"
    id=Column(Integer,primary_key=True,index=True)
    interview_id=Column(Integer,ForeignKey("interviews.id",ondelete="CASCADE"),nullable=False,unique=True,index=True)
    overall_score=Column(Float,nullable=False)
    communication_score=Column(Float,nullable=False)
    technical_score=Column(Float,nullable=False)
    problem_solving_score=Column(Float,nullable=False)
    
    strengths=Column(JSONB,nullable=False,default=list)
    weaknesses=Column(JSONB,nullable=False,default=list)

    summary=Column(Text,nullable=False)
    hiring_recommendation=Column(Text,nullable=False)
    improvement_plan=Column(JSONB,nullable=False,default=list)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    interview:Mapped["Interview"]=relationship("Interview",back_populates="report")