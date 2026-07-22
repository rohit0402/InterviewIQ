from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ResumeAnalysisResponse(BaseModel):
    summary: str | None

    skills: list[str] | None

    education: list[dict[str, Any]] | None

    experience: list[dict[str, Any]] | None

    projects: list[dict[str, Any]] | None

    strengths: list[str] | None

    weaknesses: list[str] | None

    ats_score: int | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)