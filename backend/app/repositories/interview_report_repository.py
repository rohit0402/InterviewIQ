from sqlalchemy.orm import Session

from app.models.interview_report import InterviewReport


class InterviewReportRepository:

    @staticmethod
    def create(
        db: Session,
        report: InterviewReport,
    ) -> InterviewReport:
        db.add(report)
        db.flush()
        db.refresh(report)
        return report

    @staticmethod
    def get_by_interview_id(
        db: Session,
        interview_id: int,
    ) -> InterviewReport | None:
        return (
            db.query(InterviewReport)
            .filter(InterviewReport.interview_id == interview_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        report: InterviewReport,
    ):
        db.flush()
        db.refresh(report)
        return report