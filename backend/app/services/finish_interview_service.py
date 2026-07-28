from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enum import InterviewStatus
from app.models.interview import Interview
from app.repositories.interview_report_repository import (
    InterviewReportRepository,
)
from app.repositories.interview_repository import InterviewRepository
from app.tasks.report_tasks import generate_report_task


class FinishInterviewService:

    @staticmethod
    def finish(
        db: Session,
        interview: Interview,
    ):

        existing_report = InterviewReportRepository.get_by_interview_id(
            db,
            interview.id,
        )

        if existing_report is not None:
            return existing_report

        if interview.status != InterviewStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interview is not in progress.",
            )

        answered_questions = [
            question
            for question in interview.questions
            if question.answer is not None
        ]

        if not answered_questions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No interview answers submitted.",
            )

        InterviewRepository.update_status(
            db=db,
            interview=interview,
            status=InterviewStatus.FINISHED,
        )

        try:
            generate_report_task.delay(interview.id)

        except Exception:

            InterviewRepository.update_status(
                db=db,
                interview=interview,
                status=InterviewStatus.FAILED,
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to queue report generation.",
            )

        return {
            "message": "Interview completed successfully. Report generation started."
        }