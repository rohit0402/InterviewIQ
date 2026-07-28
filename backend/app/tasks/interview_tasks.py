from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from app.tasks.base import BaseTask

from app.repositories.interview_repository import InterviewRepository
from app.services.interview_analysis_service import (
    InterviewAnalysisService,
)
from app.core.enum import InterviewStatus


@celery_app.task(
    bind=True,
    base=BaseTask,
)
def process_interview_task(
    self,
    interview_id: int,
):

    db: Session = SessionLocal()

    interview = None

    try:

        interview = InterviewRepository.get_by_id(
            db,
            interview_id,
        )

        if interview is None:
            return

        InterviewRepository.update_status(
            db,
            interview,
            InterviewStatus.ANALYZING,
        )

        InterviewAnalysisService.analyze(
            db,
            interview,
        )

        InterviewRepository.update_status(
            db,
            interview,
            InterviewStatus.READY,
        )

    except Exception:

        if interview is not None:

            InterviewRepository.update_status(
                db,
                interview,
                InterviewStatus.FAILED,
            )

        raise

    finally:

        db.close()