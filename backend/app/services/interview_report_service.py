from fastapi import HTTPException

from app.repositories.interview_report_repository import (
    InterviewReportRepository,
)
from app.repositories.interview_question_insight_repository import (
    InterviewQuestionInsightRepository,
)
from app.schemas.interview import (
    InterviewReportResponse,
    QuestionReportResponse,
)


class InterviewReportService:

    @staticmethod
    def build_report_response(
        db,
        interview,
    ) -> InterviewReportResponse:

        report = InterviewReportRepository.get_by_interview_id(
            db,
            interview.id,
        )

        if report is None:
            raise HTTPException(
                status_code=404,
                detail="Interview report not found.",
            )

        question_reports = []

        for question in interview.questions:

            if question.answer is None:
                continue

            insight = (
                InterviewQuestionInsightRepository.get_by_question_id(
                    db,
                    question.id,
                )
            )

            question_reports.append(
                QuestionReportResponse(
                    question=question.question,
                    topic=question.topic,
                    difficulty=question.difficulty,

                    candidate_answer=question.answer.answer,

                    score=question.answer.score,
                    feedback=question.answer.feedback,

                    ideal_answer=(
                        insight.ideal_answer
                        if insight
                        else ""
                    ),

                    key_learning_points=(
                        insight.key_learning_points
                        if insight
                        else []
                    ),
                )
            )

        return InterviewReportResponse(
            overall_score=report.overall_score,
            communication_score=report.communication_score,
            technical_score=report.technical_score,
            problem_solving_score=report.problem_solving_score,

            strengths=report.strengths,
            weaknesses=report.weaknesses,

            summary=report.summary,

            hiring_recommendation=report.hiring_recommendation,

            improvement_plan=report.improvement_plan,

            question_reports=question_reports,
        )