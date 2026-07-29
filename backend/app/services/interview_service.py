from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.models.interview import Interview
from app.models.user import User
from app.schemas.interview import (InterviewCreate,)
from app.repositories.resume_repository import ResumeRepository
from app.repositories.interview_repository import InterviewRepository
from app.services.question_service import QuestionService
from app.core.enum import InterviewStatus
from app.tasks.interview_tasks import process_interview_task

class InterviewService:

    @staticmethod
    def create_interview(
        db: Session,
        current_user: User,
        interview_data: InterviewCreate,
    ) -> Interview:

        resume = ResumeRepository.get_by_user_id(
            db,
            current_user.id,
        )

        if resume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )

        if resume.analysis is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume analysis not found",
            )

        interview = Interview(
            user_id=current_user.id,
            resume_id=resume.id,
            company_name=interview_data.company_name,
            job_role=interview_data.job_role,
            experience_level=interview_data.experience_level,
            job_description=interview_data.job_description,

            # These will be filled by the background task
            required_skills=[],
            match_score=None,

            status=InterviewStatus.PENDING,
        )

        interview = InterviewRepository.create(
            db,
            interview,
        )

        try:

            process_interview_task.delay(
                interview.id,
            )

        except Exception:

            InterviewRepository.update_status(
                db=db,
                interview=interview,
                status=InterviewStatus.FAILED,
            )

            raise

        return interview


    
    @staticmethod
    def get_interview(db: Session,interview_id: int,) -> Interview:

        interview = InterviewRepository.get_by_id(db,interview_id,)

        if interview is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found.",
            )

        return interview
    
    @staticmethod
    def start_interview(db,interview):
        if interview.status != InterviewStatus.READY:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Interview is not ready to start",)
        question=QuestionService.generate_first_question(db=db,interview=interview,resume_analysis=interview.resume.analysis,interview_analysis=interview.analysis)
        InterviewRepository.update_status(
            db=db,
            interview=interview,
            status=InterviewStatus.IN_PROGRESS,
        )
        print("Router status:", interview.status)

        return question

    @staticmethod
    def get_user_interviews(
        db: Session,
        current_user: User,
    ) -> list[Interview]:
        return InterviewRepository.get_by_user(
            db=db,
            user_id=current_user.id,
        )
    @staticmethod
    def delete_interview(db: Session, interview: Interview):
        InterviewRepository.delete(db, interview)