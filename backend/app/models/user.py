from datetime import datetime
from sqlalchemy import Boolean,DateTime,String,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database.base import Base
from app.core.enum import UserRole
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.resume import Resume
class User(Base):
    __tablename__ = "users"
    id: Mapped[int]=mapped_column(primary_key=True,index=True)
    full_name: Mapped[str]=mapped_column(String(100))
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True,nullable=False)
    hashed_password: Mapped[str]=mapped_column(String(255),nullable=False)
    is_active: Mapped[bool]=mapped_column(Boolean(),default=True)
    is_verified: Mapped[bool]=mapped_column(Boolean(),default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())    
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    role: Mapped[str]=mapped_column(String(20),default=UserRole.CANDIDATE.value)
    resume:Mapped["Resume"]=relationship("Resume",back_populates="owner",uselist=False,cascade="all,delete-orphan")