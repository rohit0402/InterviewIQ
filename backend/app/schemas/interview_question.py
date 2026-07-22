from pydantic import BaseModel, ConfigDict


class InterviewQuestionResponse(BaseModel):

    id: int

    question: str

    topic: str

    difficulty: str

    sequence: int

    model_config = ConfigDict(from_attributes=True)