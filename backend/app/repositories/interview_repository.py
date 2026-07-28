from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.core.enum import InterviewStatus

class InterviewRepository:

    @staticmethod
    def create(db: Session, interview: Interview) -> Interview:
        db.add(interview)
        db.commit()
        db.refresh(interview)
        return interview

    @staticmethod
    def get_by_id(db: Session, interview_id: int) -> Interview | None:
        return (db.query(Interview).filter(Interview.id == interview_id).first())

    @staticmethod
    def get_by_user(db: Session, user_id: int) -> list[Interview]:
        return (db.query(Interview).filter(Interview.user_id == user_id).order_by(Interview.created_at.desc()).all())

    @staticmethod
    def delete(db: Session, interview: Interview):
        db.query(Interview).filter(
            Interview.id == interview.id
        ).delete(synchronize_session=False)
        db.commit()

    @staticmethod
    def update_status(
        db: Session,
        interview: Interview,
        status: InterviewStatus,
    ) -> Interview:
        interview.status = status
        db.commit()
        db.refresh(interview)
        return interview