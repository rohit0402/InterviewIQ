from sqlalchemy.orm import Session, joinedload
from app.models.interview_answer import InterviewAnswer
from app.models.interview_question import InterviewQuestion


class InterviewAnswerRepository:

    @staticmethod
    def create(db: Session, answer: InterviewAnswer,) -> InterviewAnswer:
        db.add(answer)
        db.commit()
        db.refresh(answer) 
        return answer
    
    @staticmethod
    def update(db: Session, answer: InterviewAnswer,) -> InterviewAnswer:
        db.commit()
        db.refresh(answer)
        return answer
    
    @staticmethod
    def get_by_id(db: Session, answer_id: int,) -> InterviewAnswer | None:
        return InterviewAnswer.query.filter_by(InterviewAnswer.id == answer_id).first()
    
    @staticmethod
    def get_by_question(db: Session, question_id: int,) -> InterviewAnswer | None:
        return InterviewAnswer.query.filter_by(InterviewAnswer.question_id == question_id).first()
    
    @staticmethod 
    def get_all_by_interview(db: Session, interview_id: int,) -> list[InterviewAnswer]:
        return db.query(InterviewAnswer).join(InterviewQuestion).options(joinedload(InterviewAnswer.question)).filter_by(InterviewQuestion.interview_id == interview_id).order_by(InterviewQuestion.sequence).all()
    
    @staticmethod
    def delete(db: Session, answer: InterviewAnswer,) -> None:
        db.delete(answer)
        db.commit()

    @staticmethod
    def get_interview_history(db: Session, interview_id: int,):
        return db.query(InterviewQuestion).options(joinedload(InterviewQuestion.answer)).filter(InterviewQuestion.interview_id == interview_id).order_by(InterviewQuestion.sequence).all()
    