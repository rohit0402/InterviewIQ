from app.ai.ai_service import AIService
from app.models.interview_question import InterviewQuestion
from app.repositories.interview_question_repository import InterviewQuestionRepository

class QuestionService:

    @staticmethod
    def generate_first_question(db,interview,resume_analysis,interview_analysis):
        ai=AIService()

        result=ai.generate_first_question(resume_analysis=resume_analysis,job_description=interview.job_description,interview_analysis=interview_analysis)
        question=InterviewQuestion(interview_id=interview.id,question=result.question,topic=result.topic,difficulty=result.difficulty,sequence=1)

        return InterviewQuestionRepository.create(db,question)