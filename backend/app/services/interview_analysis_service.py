from sqlalchemy.orm import Session

from app.ai.ai_service import AIService
from app.models.interview import Interview
from app.models.interview_analysis import InterviewAnalysis
from app.repositories.interview_analysis_repository import (
    InterviewAnalysisRepository,
)


class InterviewAnalysisService:

    @staticmethod
    def analyze(
        db: Session,
        interview: Interview,
    ):

        ai_service = AIService()

        # Analyze Job Description
        jd_analysis = ai_service.analyze_job_description(
            interview.job_description,
        )

        # Compare Resume with Job Description
        match = ai_service.compare_resume_with_job(
            resume_analysis=interview.resume.analysis,
            job_description=interview.job_description,
        )

        # Update Interview
        interview.required_skills = jd_analysis.required_skills
        interview.match_score = match.match_score

        # Existing Analysis?
        analysis = InterviewAnalysisRepository.get_by_interview_id(
            db,
            interview.id,
        )

        if analysis is None:

            analysis = InterviewAnalysis(
                interview_id=interview.id,
            )

            is_new = True

        else:

            is_new = False

        analysis.matching_skills = match.matching_skills
        analysis.missing_skills = match.missing_skills
        analysis.strengths = match.strengths
        analysis.weaknesses = match.weaknesses
        analysis.overall_feedback = match.overall_feedback

        if is_new:
            InterviewAnalysisRepository.create(
                db,
                analysis,
            )
        else:
            InterviewAnalysisRepository.update(
                db,
                analysis,
            )

        db.commit()
        db.refresh(interview)