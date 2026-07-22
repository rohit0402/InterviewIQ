from sqlalchemy.orm import Session

from app.models.interview_analysis import InterviewAnalysis


class InterviewAnalysisRepository:

    @staticmethod
    def create(db: Session, analysis: InterviewAnalysis):
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    @staticmethod
    def get_by_interview_id(db: Session, interview_id: int):
        return (db.query(InterviewAnalysis).filter( InterviewAnalysis.interview_id == interview_id).first())