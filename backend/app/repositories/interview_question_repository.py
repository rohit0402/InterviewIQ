from sqlalchemy.orm import Session
from app.models.interview_question import InterviewQuestion

class InterviewQuestionRepository:

    @staticmethod
    def create(db: Session,question: InterviewQuestion,) -> InterviewQuestion:
        db.add(question)
        db.commit()
        db.refresh(question)
        return question
    
    @staticmethod
    def get_last_question(db: Session,interview_id: int,) -> InterviewQuestion:
        return InterviewQuestion.query.filter_by(interview_id=interview_id).order_by(InterviewQuestion.sequence.desc()).first()
    
    @staticmethod
    def get_by_id(db: Session,question_id: int,) -> InterviewQuestion | None:
        return db.query(InterviewQuestion).filter(InterviewQuestion.id == question_id).first()