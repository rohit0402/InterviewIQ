from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from app.tasks.base import BaseTask

from app.repositories.interview_repository import InterviewRepository
from app.services.report_service import ReportService
from app.core.enum import InterviewStatus


@celery_app.task(
    bind=True,
    base=BaseTask,
)
def generate_report_task(
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
            InterviewStatus.REPORT_GENERATING,
        )

        ReportService.generate(
            db,
            interview,
        )

        InterviewRepository.update_status(
            db,
            interview,
            InterviewStatus.REPORT_READY,
        )

    except Exception:

        if interview:

            InterviewRepository.update_status(
                db,
                interview,
                InterviewStatus.FAILED,
            )

        raise

    finally:

        db.close()