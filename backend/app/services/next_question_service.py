from app.ai.ai_service import AIService

from app.models.interview import Interview
from app.models.interview_question import InterviewQuestion

from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)
from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)

from app.schemas.interview_question import InterviewQuestionResponse


class NextQuestionService:

    @staticmethod
    def generate(
        db,
        interview: Interview,
        resume_analysis,
        interview_analysis,
    ) -> InterviewQuestionResponse:

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

        last_question = history[-1]

        ai = AIService()

        result = ai.generate_next_question(
            resume_analysis=resume_analysis,
            job_description=interview.job_description,
            interview_analysis=interview_analysis,
            interview_history=conversation,
        )

        next_question = InterviewQuestion(
            interview_id=interview.id,
            question=result.question,
            topic=result.topic,
            difficulty=result.difficulty,
            sequence=last_question.sequence + 1,
        )

        next_question = InterviewQuestionRepository.create(
            db,
            next_question,
        )

        return InterviewQuestionResponse(
            id=next_question.id,
            question=next_question.question,
            topic=next_question.topic,
            difficulty=next_question.difficulty,
            sequence=next_question.sequence,
        )