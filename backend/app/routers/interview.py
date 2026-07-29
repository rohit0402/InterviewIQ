from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.enum import InterviewStatus
from app.auth.dependencies import get_current_user
from app.database.dependencies import get_db
from app.services.interview_report_service import InterviewReportService
from app.models.user import User
from app.services.next_question_service import NextQuestionService
from app.schemas.interview import ( InterviewCreate,InterviewResponse, InterviewReportResponse,QuestionReportResponse,)
from app.schemas.interview_question import InterviewQuestionResponse
from app.services.interview_service import InterviewService
from app.services.resume_service import ResumeService
from app.services.evaluation_service import EvaluationService
from app.repositories.interview_question_repository import InterviewQuestionRepository
from app.schemas.interview_answer import InterviewAnswerCreate,AnswerSubmittedResponse
from app.repositories.interview_repository import InterviewRepository
from app.services.finish_interview_service import FinishInterviewService
from app.repositories.interview_report_repository import InterviewReportRepository
from app.repositories.interview_question_insight_repository import InterviewQuestionInsightRepository

router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


@router.post("/",response_model=InterviewResponse,status_code=status.HTTP_202_ACCEPTED,)
def create_interview(interview_data: InterviewCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    resume = ResumeService.get_resume(db=db,current_user=current_user,)

    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resume not found.",)

    interview = InterviewService.create_interview(
        db=db,
        current_user=current_user,
        interview_data=interview_data,
    )

    return interview


@router.get("/",response_model=list[InterviewResponse],)
def get_my_interviews(db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    return InterviewService.get_user_interviews(db=db,current_user=current_user,)


@router.get("/{interview_id}", response_model=InterviewResponse,)
def get_interview(interview_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    interview = InterviewService.get_interview(db=db,interview_id=interview_id,)

    if interview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.",)

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied.",)

    return interview


@router.delete("/{interview_id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_interview(interview_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    interview = InterviewService.get_interview(db=db,interview_id=interview_id,)

    if interview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Interview not found.",)

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied.",)

    InterviewService.delete_interview(db=db,interview=interview,)

@router.post("/{interview_id}/start",response_model=InterviewQuestionResponse)
def start_interview(interview_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    interview = InterviewService.get_interview(db=db,interview_id=interview_id,)
    if interview.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_200_OK,detail="Access denied.",)
    
    return InterviewService.start_interview(db=db,interview=interview,)

@router.post("/question/{question_id}/answer",response_model=AnswerSubmittedResponse)
def submit_answer(question_id: int,answer: InterviewAnswerCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    question = InterviewQuestionRepository.get_by_id(db,question_id,)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Question not found.",)
    
    interview=question.interview

    if interview.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied.",)
    
    resume_analysis=interview.resume.analysis

    interview_analysis=interview.analysis

    return EvaluationService.submit_answer(db=db,question=question,answer_text=answer.answer,resume_analysis=resume_analysis,
            interview_analysis=interview_analysis,interview=interview,)

@router.post(
    "/{interview_id}/next-question",
    response_model=InterviewQuestionResponse,
)
def next_question(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interview = InterviewRepository.get_by_id(
        db,
        interview_id,
    )

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )

    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )

    return NextQuestionService.generate(
        db=db,
        interview=interview,
        resume_analysis=interview.resume.analysis,
        interview_analysis=interview.analysis,
    )

@router.post(
    "/{interview_id}/finish",
    status_code=status.HTTP_202_ACCEPTED,
)
def finish_interview(interview_id: int,db: Session = Depends(get_db),current_user = Depends(get_current_user),):
    interview=InterviewRepository.get_by_id(db,interview_id,)
    if interview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Interview not found.",)
    
    if interview.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied.",)
    
    FinishInterviewService.finish(
        db=db,
        interview=interview,
    )

    return {
        "message": "Interview finished successfully. Report generation started."
    }


@router.get(
    "/{interview_id}/report",
    response_model=InterviewReportResponse,
)
def get_interview_report(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interview = InterviewRepository.get_by_id(
        db, 
        interview_id,
    )

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )

    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )

    if interview.status == InterviewStatus.REPORT_GENERATING:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Report is still being generated.",
        )

    if interview.status == InterviewStatus.FAILED:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Report generation failed.",
        )

    report = InterviewReportRepository.get_by_interview_id(
        db,
        interview_id,
    )

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview report not found.",
        )

    question_reports = []

    for question in interview.questions:

        if question.answer is None:
            continue

        insight = (
            InterviewQuestionInsightRepository
            .get_by_question_id(
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

    return InterviewReportService.build_report_response(
    db=db,
    interview=interview,
)                                  

@router.get("/{interview_id}/status")
def get_interview_status(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interview = InterviewService.get_interview(db, interview_id)

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found.",
        )
    
    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    return {
        "status": interview.status,
    }