from app.ai.ai_service import AIService
from app.models.interview_answer import InterviewAnswer
from app.models.interview_question import InterviewQuestion

from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)

from app.schemas.interview_answer import AnswerSubmittedResponse


class EvaluationService:

    @staticmethod
    def submit_answer( db,
        question: InterviewQuestion,answer_text: str,resume_analysis,interview_analysis,interview,) -> AnswerSubmittedResponse:

        if question.answer:
            raise ValueError("Answer already submitted.")

        answer = InterviewAnswer(
            interview_question_id=question.id,
            answer=answer_text,
        )

        answer = InterviewAnswerRepository.create(
            db,
            answer,
        )

        history = InterviewAnswerRepository.get_interview_history(
            db,
            interview.id,
        )

        conversation = []

        for q in history:
            conversation.append(
                {
                    "question": q.question,
                    "answer": q.answer.answer if q.answer else None,
                }
            )

        ai = AIService()

        result = ai.evaluate_answer(
            resume_analysis=resume_analysis,
            job_description=interview.job_description,
            interview_analysis=interview_analysis,
            interview_history=conversation,
            current_question=question.question,
            current_answer=answer.answer,
        )

        answer.score = result.score
        answer.feedback = result.feedback

      

        InterviewAnswerRepository.update(
            db,
            answer,
        )

        return AnswerSubmittedResponse(
            message="Answer submitted successfully."
        )