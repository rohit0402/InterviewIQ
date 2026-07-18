from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Integer,Text,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.resume import Resume

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int]=mapped_column(primary_key=True)
    resume_id: Mapped[int]=mapped_column(ForeignKey("resumes.id"),unique=True,index=True,nullable=False)
    raw_text:Mapped[str]=mapped_column(Text,nullable=False)
    summary:Mapped[str | None]=mapped_column(Text,nullable=True)
    skills:Mapped[str | None]=mapped_column(Text,nullable=True)
    experience:Mapped[str | None]=mapped_column(Text,nullable=True)
    education:Mapped[str | None]=mapped_column(Text,nullable=True)
    projects:Mapped[str | None]=mapped_column(Text,nullable=True)
    strengths:Mapped[str | None]=mapped_column(Text,nullable=True)
    weaknesses:Mapped[str | None]=mapped_column(Text,nullable=True)
    ats_score:Mapped[int | None]=mapped_column(Integer,nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    resume:Mapped["Resume"]=relationship("Resume",back_populates="analysis")
