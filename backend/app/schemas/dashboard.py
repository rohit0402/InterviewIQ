from pydantic import BaseModel
from app.core.enum import InterviewStatus


class RecentInterview(BaseModel):
    id: int
    company_name: str
    job_role: str
    status: InterviewStatus
    overall_score: float | None


class DashboardResponse(BaseModel):
    resume_uploaded: bool

    total_interviews: int

    completed_interviews: int

    in_progress_interviews: int

    average_score: float | None

    recent_interviews: list[RecentInterview]