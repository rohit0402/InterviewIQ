from sqlalchemy.orm import Session

from app.models.user import User
from app.core.enum import InterviewStatus

from app.repositories.resume_repository import ResumeRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.interview_report_repository import InterviewReportRepository
from app.services.cache_service import CacheService

class DashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        current_user: User,
    ):

        resume = ResumeRepository.get_by_user_id(
            db,
            current_user.id,
        )

        interviews = InterviewRepository.get_by_user(
            db,
            current_user.id,
        )

        completed = [
            interview
            for interview in interviews
            if interview.status == InterviewStatus.COMPLETED
        ]

        reports = []

        for interview in completed:
            report = InterviewReportRepository.get_by_interview_id(
                db,
                interview.id,
            )

            if report:
                reports.append(report)

        average_score = None

        if reports:
            average_score = round(
                sum(
                    report.overall_score
                    for report in reports
                )
                / len(reports),
                2,
            )

        recent = []

        for interview in interviews[:5]:

            report = InterviewReportRepository.get_by_interview_id(
                db,
                interview.id,
            )

            recent.append(
                {
                    "id": interview.id,
                    "company_name": interview.company_name,
                    "job_role": interview.job_role,
                    "status": interview.status,
                    "overall_score": (
                        report.overall_score
                        if report
                        else None
                    ),
                }
            )

        cache_key = f"dashboard:{current_user.id}"
        cached=CacheService.get(cache_key)

        if cached:
            return cached

        dashboard= {
            "resume_uploaded": resume is not None,

            "total_interviews": len(interviews),

            "completed_interviews": len(completed),

            "in_progress_interviews": len(
                [
                    interview
                    for interview in interviews
                    if interview.status
                    == InterviewStatus.IN_PROGRESS
                ]
            ),

            "average_score": average_score,

            "recent_interviews": recent,
        }

        CacheService.set(
            cache_key,
            dashboard,
        )

        return dashboard