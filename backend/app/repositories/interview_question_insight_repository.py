from sqlalchemy.orm import Session

from app.models.interview_question_insight import (
    InterviewQuestionInsight,
)


class InterviewQuestionInsightRepository:

    @staticmethod
    def create(
        db: Session,
        insight: InterviewQuestionInsight,
    ):
        db.add(insight)
        db.flush()
        db.refresh(insight)
        return insight

    @staticmethod
    def get_by_question_id(
        db: Session,
        question_id: int,
    ):
        return (
            db.query(InterviewQuestionInsight)
            .filter_by(
                interview_question_id=question_id
            )
            .first()
        )