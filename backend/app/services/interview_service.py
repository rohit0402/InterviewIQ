from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.models.interview import Interview
from app.models.resume import Resume
from app.models.user import User
from app.ai.ai_service import AIService
from app.schemas.interview import (InterviewCreate,)
from app.repositories.resume_repository import ResumeRepository
from app.repositories.interview_repository import InterviewRepository
from app.models.interview_analysis import InterviewAnalysis
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.repositories.interview_analysis_repository import InterviewAnalysisRepository  
from app.services.question_service import QuestionService
from app.core.enum import InterviewStatus
class InterviewService:

    @staticmethod
    def create_interview(db: Session,current_user: User,interview_data: InterviewCreate,) -> Interview:

        resume = ResumeRepository.get_by_user_id(db, current_user.id)

        if resume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )
        ai_service = AIService()
        
        jd_analysis = ai_service.analyze_job_description(
            interview_data.job_description
        )
        
        resume_analysis = resume.analysis
        if resume_analysis is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="resume analysis not found")
        
        match=ai_service.compare_resume_with_job(resume_analysis=resume_analysis,job_description=interview_data.job_description)

        interview = Interview(
            user_id=current_user.id,
            resume_id=resume.id,
            company_name=interview_data.company_name,
            job_role=interview_data.job_role,
            experience_level=interview_data.experience_level,
            job_description=interview_data.job_description,
            required_skills=jd_analysis.required_skills,
            match_score=match.match_score,
        )
        interview=InterviewRepository.create(db,interview)
        InterviewAnalysisRepository.create(db,InterviewAnalysis(interview_id=interview.id,matching_skills=match.matching_skills,missing_skills=match.missing_skills,strengths=match.strengths,weaknesses=match.weaknesses,overall_feedback=match.overall_feedback))

        return interview
    @staticmethod
    def get_interview(db: Session,interview_id: int,) -> Interview:

        interview = InterviewRepository.get_by_id(db,interview_id,)

        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found",
            )

        return interview
    
    @staticmethod
    def start_interview(db,interview):
        question=QuestionService.generate_first_question(db=db,interview=interview,resume_analysis=interview.resume.analysis,interview_analysis=interview.analysis)
        interview.status=InterviewStatus.IN_PROGRESS
        db.commit()
        db.refresh(interview)
        return question