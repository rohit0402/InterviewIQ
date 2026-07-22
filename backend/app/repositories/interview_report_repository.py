from sqlalchemy.orm import Session
from app.models.interview_report import InterviewReport

class InterviewReportRepository:

    @staticmethod
    def create(db: Session,report: InterviewReport,) -> InterviewReport:
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
    
    @staticmethod
    def get_by_id(db:Session,interview_id: int,):
        return db.query(InterviewReport).filter_by(InterviewReport.interview_id == interview_id).first()