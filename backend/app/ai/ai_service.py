import json

from pydantic import ValidationError
from app.ai.prompts import (
    resume_analysis_prompt,
    job_description_analysis_prompt,
    resume_job_match_prompt,
    first_interview_question_prompt,
    next_question_prompt,
    final_interview_report_prompt,
    evaluate_answer_prompt,
)
from app.ai.providers.factory import ProviderFactory
from app.ai.schemas import ResumeAnalysisResult, JobDescription,ResumeJobMatch,FinalInterviewReport,EvaluateAnswerResponse,InterviewQuestionGeneration
from app.core.config import settings


class AIService:

    def __init__(self):
        self.provider = ProviderFactory.create(settings.AI_PROVIDER)

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)

    def analyze_resume(self, resume_text: str) -> ResumeAnalysisResult:
        prompt = resume_analysis_prompt(resume_text)
        response = self.provider.generate(prompt)
        try:
            data = json.loads(response)
            return ResumeAnalysisResult.model_validate(data)
        except json.JSONDecodeError:
            raise ValueError("AI returned invalid JSON.")
        except ValidationError as e:
            raise ValueError(f"Invalid AI response: {e}")
        

    def analyze_job_description(self,job_description: str,) -> JobDescription:
        prompt = job_description_analysis_prompt(job_description)
        response = self.provider.generate(prompt)
        return JobDescription.model_validate_json(response)
    

    def compare_resume_with_job(self,resume_analysis: dict,job_description: str,) -> ResumeJobMatch:
        resume_data = {
            "summary": resume_analysis.summary,
            "skills": resume_analysis.skills,
            "experience": resume_analysis.experience,
            "education": resume_analysis.education,
            "projects": resume_analysis.projects,
            "strengths": resume_analysis.strengths,
            "weaknesses": resume_analysis.weaknesses,
            "ats_score": resume_analysis.ats_score,
        }
        prompt = resume_job_match_prompt(resume_data,job_description,)
        response = self.provider.generate(prompt)
        return ResumeJobMatch.model_validate_json(response)
    
    def generate_first_question(self,resume_analysis,job_description,interview_analysis,) -> InterviewQuestionGeneration:

        prompt = first_interview_question_prompt(
            resume_analysis,
            job_description,
            interview_analysis,
        )
        response = self.generate(prompt)
        return InterviewQuestionGeneration.model_validate_json(response)
    
    def generate_next_question(self,resume_analysis,job_description,interview_analysis,interview_history,) -> InterviewQuestionGeneration:

        prompt = next_question_prompt(
            resume_analysis=resume_analysis,
            job_description=job_description,
            interview_analysis=interview_analysis,
            interview_history=interview_history,
        )

        response = self.generate(prompt)

        return InterviewQuestionGeneration.model_validate_json(response)

    
    def generate_final_report(self,resume_analysis,interview_analysis,interview_history):
        prompt=final_interview_report_prompt(resume_analysis,interview_analysis,interview_history)
        response=self.provider.generate(prompt)
        return FinalInterviewReport.model_validate_json(response)
    
    def evaluate_answer(self, resume_analysis,job_description,interview_analysis,interview_history,current_question,current_answer,) -> EvaluateAnswerResponse:

        prompt = evaluate_answer_prompt(
            resume_analysis=resume_analysis,
            job_description=job_description,
            interview_analysis=interview_analysis,
            interview_history=interview_history,
            current_question=current_question,
            current_answer=current_answer,
        )

        response = self.generate(prompt)

        return EvaluateAnswerResponse.model_validate_json(response)