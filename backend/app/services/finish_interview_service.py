from datetime import datetime

from app.ai.ai_service import AIService

from app.models.interview import InterviewStatus
from app.models.interview_report import InterviewReport

from app.repositories.interview_report_repository import InterviewReportRepository



class FinishInterviewService:

    @staticmethod
    def finish(db,interview,resume_analysis,interview_analysis,):
        history = []
        for question in interview.questions:
            history.append(
                {
                    "question": question.question,
                    "answer": (
                        question.answer.answer
                        if question.answer
                        else None
                    ),
                    "score": (
                        question.answer.score
                        if question.answer
                        else None
                    ),
                }
            )

        ai = AIService()

        result = ai.generate_final_report(
            resume_analysis,
            interview_analysis,
            history,
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