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

class QuestionReportResponse(BaseModel):
    question: str
    topic: str
    difficulty: str

    candidate_answer: str

    score: float
    feedback: str

    ideal_answer: str

    key_learning_points: list[str]


class InterviewReportResponse(BaseModel):
    overall_score: float
    communication_score: float
    technical_score: float
    problem_solving_score: float

    strengths: list[str]
    weaknesses: list[str]

    summary: str

    hiring_recommendation: str

    improvement_plan: list[str]

    question_reports: list[QuestionReportResponse]

    model_config = ConfigDict(from_attributes=True)