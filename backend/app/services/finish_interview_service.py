import logging

from fastapi import HTTPException

from app.ai.ai_service import AIService
from app.models.interview import InterviewStatus
from app.models.interview_question_insight import InterviewQuestionInsight
from app.models.interview_report import InterviewReport
from app.repositories.interview_question_insight_repository import (
    InterviewQuestionInsightRepository,
)
from app.repositories.interview_report_repository import (
    InterviewReportRepository,
)

logger = logging.getLogger(__name__)


class FinishInterviewService:

    @staticmethod
    def finish(
        db,
        interview,
        resume_analysis,
        interview_analysis,
    ):
        existing_report = InterviewReportRepository.get_by_interview_id(
            db,
            interview.id,
        )

        if interview.status == InterviewStatus.COMPLETED:
            return existing_report

        if interview.status != InterviewStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=400,
                detail="Interview is not in progress.",
            )

        answered_questions = [
            question
            for question in interview.questions
            if question.answer is not None
        ]

        if not answered_questions:
            raise HTTPException(
                status_code=400,
                detail="No interview answers submitted.",
            )

        history = [
            {
                "question": question.question,
                "candidate_answer": question.answer.answer,
                "score": question.answer.score,
                "feedback": question.answer.feedback,
            }
            for question in answered_questions
        ]

        ai = AIService()

        try:
            result = ai.generate_final_report(
                resume_analysis=resume_analysis,
                interview_analysis=interview_analysis,
                interview_history=history,
            )

            if len(result.question_insights) != len(answered_questions):
                raise ValueError(
                    "AI returned incorrect number of question insights."
                )

            for question, insight in zip(
                answered_questions,
                result.question_insights,
            ):
                existing_insight = (
                    InterviewQuestionInsightRepository.get_by_question_id(
                        db,
                        question.id,
                    )
                )

                if existing_insight is None:
                    InterviewQuestionInsightRepository.create(
                        db,
                        InterviewQuestionInsight(
                            interview_question_id=question.id,
                            ideal_answer=insight.ideal_answer,
                            key_learning_points=insight.key_learning_points,
                        ),
                    )

            report = InterviewReport(
                interview_id=interview.id,
                overall_score=result.overall_score,
                communication_score=result.communication_score,
                technical_score=result.technical_score,
                problem_solving_score=result.problem_solving_score,
                strengths=result.strengths,
                weaknesses=result.weaknesses,
                summary=result.summary,
                hiring_recommendation=result.hiring_recommendation,
                improvement_plan=result.improvement_plan,
            )

            report = InterviewReportRepository.create(
                db,
                report,
            )

            interview.status = InterviewStatus.COMPLETED

            db.commit()

            db.refresh(report)

            return report

        except Exception:
            db.rollback()

            logger.exception(
                "Failed to generate interview report"
            )

            raise HTTPException(
                status_code=500,
                detail="Failed to generate interview report.",
            )