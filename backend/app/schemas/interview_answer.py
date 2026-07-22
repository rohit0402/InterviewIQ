
from pydantic import BaseModel, ConfigDict


class InterviewAnswerCreate(BaseModel):
    answer: str


class InterviewAnswerResponse(BaseModel):
    id: int
    answer: str
    score: float | None
    feedback: str | None

    model_config = ConfigDict(from_attributes=True)


class AnswerSubmittedResponse(BaseModel):
    message: str