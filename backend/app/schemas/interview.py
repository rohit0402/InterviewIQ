from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enum import InterviewStatus


class InterviewCreate(BaseModel):
    company_name: str
    job_role: str
    experience_level: str
    job_description: str


class InterviewResponse(BaseModel):
    id: int
    company_name: str
    job_role: str
    experience_level: str
    job_description: str
    required_skills: list[str]
    match_score: float | None
    status: InterviewStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)