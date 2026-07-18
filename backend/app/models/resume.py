from datetime import datetime
from sqlalchemy import Boolean,DateTime,String,func,Integer,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database.base import Base
from app.core.enum import ResumeStatus
from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from app.models.user import User
    from app.models.resume_analysis import ResumeAnalysis
class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[int]=mapped_column(primary_key=True,index=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"),unique=True,index=True,nullable=False)
    original_filename: Mapped[str]=mapped_column(String(255),nullable=False)
    stored_filename: Mapped[str]=mapped_column(String(255),nullable=False)
    file_size: Mapped[int]=mapped_column(Integer(),nullable=False)
    file_path: Mapped[str]=mapped_column(String(500),nullable=False)
    mime_type: Mapped[str]=mapped_column(String(255),nullable=False)
    status: Mapped[str]=mapped_column(String(20),default=ResumeStatus.UPLOADED.value,nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    owner:Mapped["User"]=relationship("User",back_populates="resume")
    analysis:Mapped["ResumeAnalysis"]=relationship("ResumeAnalysis",back_populates="resume",uselist=False,cascade="all,delete-orphan")