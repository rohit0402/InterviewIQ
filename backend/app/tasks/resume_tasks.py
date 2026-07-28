from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from app.tasks.base import BaseTask
from app.repositories.resume_repository import ResumeRepository
from app.services.resume_analysis_service import ResumeAnalysisService
from app.core.enum import ResumeStatus


@celery_app.task(
    bind=True,
    base=BaseTask,
)
def process_resume_task(
    self,
    resume_id: int,
):
    db: Session = SessionLocal()

    resume = None

    try:

        resume = ResumeRepository.get_by_id(
            db=db,
            resume_id=resume_id,
        )

        if resume is None:
            return

        ResumeRepository.update_status(
            db=db,
            resume=resume,
            status=ResumeStatus.PROCESSING,
        )

        ResumeAnalysisService.analyze_resume(
            db=db,
            resume=resume,
        )

        ResumeRepository.update_status(
            db=db,
            resume=resume,
            status=ResumeStatus.COMPLETED,
        )

    except Exception:

        if resume is not None:

            ResumeRepository.update_status(
                db=db,
                resume=resume,
                status=ResumeStatus.FAILED,
            )

        raise

    finally:

        db.close()