from sqlalchemy.orm import Session

from app.ai.ai_service import AIService
from app.models.interview import Interview
from app.models.interview_report import InterviewReport
from app.models.interview_question_insight import InterviewQuestionInsight

from app.repositories.interview_report_repository import (
    InterviewReportRepository,
)
from app.repositories.interview_question_insight_repository import (
    InterviewQuestionInsightRepository,
)


class ReportService:

    @staticmethod
    def generate(
        db: Session,
        interview: Interview,
    ):

        try:

            resume_analysis = interview.resume.analysis
            interview_analysis = interview.analysis

            history = []

            for question in sorted(
                interview.questions,
                key=lambda q: q.sequence,
            ):

                history.append(
                    {
                        "question": question.question,
                        "answer": (
                            question.answer.answer
                            if question.answer
                            else ""
                        ),
                        "score": (
                            question.answer.score
                            if question.answer
                            else 0
                        ),
                        "feedback": (
                            question.answer.feedback
                            if question.answer
                            else ""
                        ),
                    }
                )

            ai = AIService()

            report = ai.generate_final_report(
                resume_analysis=resume_analysis,
                interview_analysis=interview_analysis,
                interview_history=history,
            )

            for question, insight in zip(
                sorted(interview.questions, key=lambda q: q.sequence),
                report.question_insights,
            ):

                InterviewQuestionInsightRepository.create(
                    db,
                    InterviewQuestionInsight(
                        interview_question_id=question.id,
                        ideal_answer=insight.ideal_answer,
                        key_learning_points=insight.key_learning_points,
                    ),
                )

            InterviewReportRepository.create(
                db,
                InterviewReport(
                    interview_id=interview.id,
                    overall_score=report.overall_score,
                    communication_score=report.communication_score,
                    technical_score=report.technical_score,
                    problem_solving_score=report.problem_solving_score,
                    strengths=report.strengths,
                    weaknesses=report.weaknesses,
                    summary=report.summary,
                    hiring_recommendation=report.hiring_recommendation,
                    improvement_plan=report.improvement_plan,
                ),
            )

            db.commit()

        except Exception:
            db.rollback()
            raise