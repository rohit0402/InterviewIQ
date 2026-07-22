from pydantic import BaseModel, Field,AliasChoices


class Experience(BaseModel):
    role: str|None=None
    company: str|None=None
    description: str|None=None
    duration: str|None=None


class Project(BaseModel):
    name: str = Field(
        validation_alias=AliasChoices("name", "title")
    )
    description: str


class Education(BaseModel):
    degree: str
    institute: str = Field(
        validation_alias=AliasChoices(
            "institute",
            "institution",
            "school",
            "college",
        )
    )
    year: str | None = None

#ge and le are used to specify the range of values for the field.
class ResumeAnalysisResult(BaseModel):
    summary: str
    skills: list[str] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    ats_score: int = Field(ge=0, le=100)

class JobDescription(BaseModel):
    company_name: str
    job_role: str
    experience_level: str
    required_skills: list[str]

class ResumeJobMatch(BaseModel):
    match_score: int
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    overall_feedback: str


class InterviewQuestionGeneration(BaseModel):
    question: str
    topic: str
    difficulty: str
    reasoning: str


class EvaluateAnswerResponse(BaseModel):
    score: float = Field(ge=0, le=10)
    feedback: str
    reasoning: str


class FinalInterviewReport(BaseModel):
    overall_score: float
    communication_score: float
    technical_score: float
    problem_solving_score: float
    strengths: list[str]
    weaknesses: list[str]
    summary: str
    hiring_recommendation: str
    improvement_plan: list[str]
    
