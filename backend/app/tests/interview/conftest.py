from types import SimpleNamespace

import pytest

from app.database.session import SessionLocal
from app.models.user import User
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.core.enum import ResumeStatus
from app.tests.utils.auth import authenticated_user
from app.models.interview import Interview
from app.models.interview_analysis import InterviewAnalysis
from app.core.enum import InterviewStatus
from app.models.interview_question import InterviewQuestion
from app.ai.ai_service import AIService


@pytest.fixture
def mock_ai(monkeypatch):

    monkeypatch.setattr(
        AIService,
        "generate_first_question",
        lambda self, *args, **kwargs: SimpleNamespace(
            question="Tell me about yourself.",
            topic="Introduction",
            difficulty="Easy",
        ),
    )

    monkeypatch.setattr(
        AIService,
        "evaluate_answer",
        lambda self, *args, **kwargs: SimpleNamespace(
            score=8,
            feedback="Good answer",
        ),
    )

    monkeypatch.setattr(
        AIService,
        "generate_next_question",
        lambda self, *args, **kwargs: SimpleNamespace(
            question="Explain FastAPI.",
            topic="Backend",
            difficulty="Medium",
        ),
    )

    monkeypatch.setattr(
        AIService,
        "generate_final_report",
        lambda self, *args, **kwargs: SimpleNamespace(
            overall_score=85,
            overall_feedback="Excellent",
            strengths=["Python"],
            weaknesses=["None"],
            recommendation="Hire",
        ),
    )


@pytest.fixture
def ready_user(client):
    user_data, token = authenticated_user(client)

    db = SessionLocal()

    try:
        db_user = (
            db.query(User)
            .filter(User.email == user_data["email"])
            .first()
        )

        resume = Resume(
            user_id=db_user.id,
            original_filename="resume.pdf",
            stored_filename="resume.pdf",
            raw_text="Python FastAPI PostgreSQL Docker Redis",
            file_size=100,
            file_path="/tmp/resume.pdf",
            mime_type="application/pdf",
            status=ResumeStatus.COMPLETED,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        analysis = ResumeAnalysis(
            resume_id=resume.id,
            summary="Experienced backend developer",
            skills=["Python", "FastAPI", "PostgreSQL"],
            experience=[],
            education=[],
            projects=[],
            strengths=["Problem Solving"],
            weaknesses=[],
            ats_score=90,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return SimpleNamespace(
            user=db_user,
            resume=resume,
            token=token,
        )

    finally:
        db.close()


@pytest.fixture
def started_interview(client, ready_interview, monkeypatch):

    monkeypatch.setattr(
        "app.services.question_service.AIService.generate_first_question",
        lambda self, resume_analysis, job_description, interview_analysis: SimpleNamespace(
            question="Tell me about yourself.",
            topic="Introduction",
            difficulty="Easy",
        ),
    )

    response = client.post(
        f"/api/v1/interviews/{ready_interview.id}/start",
        headers={
            "Authorization": f"Bearer {ready_interview.token}",
        },
    )

    assert response.status_code in (200, 201), response.json()

    body = response.json()

    return SimpleNamespace(
        id=ready_interview.id,
        token=ready_interview.token,
        question_id=body["id"],
    )


@pytest.fixture
def ready_interview(client, ready_user, monkeypatch):
    # Don't enqueue Celery
    monkeypatch.setattr(
        "app.services.interview_service.process_interview_task.delay",
        lambda interview_id: None,
    )

    response = client.post(
        "/api/v1/interviews/",
        headers={
            "Authorization": f"Bearer {ready_user.token}",
        },
        json={
            "company_name": "Google",
            "job_role": "Software Engineer",
            "experience_level": "Fresher",
            "job_description": "Backend Developer",
        },
    )

    assert response.status_code == 202

    interview_id = response.json()["id"]

    db = SessionLocal()

    try:
        interview = db.get(Interview, interview_id)

        analysis = InterviewAnalysis(
            interview_id=interview.id,
            matching_skills=["Python", "FastAPI"],
            missing_skills=[],
            strengths=["Backend"],
            weaknesses=[],
            overall_feedback="Good match",
        )

        db.add(analysis)

        interview.status = InterviewStatus.READY

        db.commit()
        db.refresh(interview)
        db.refresh(interview)

        print("Fixture status:", interview.status)

        check = db.get(Interview, interview.id)
        print("DB status:", check.status)

        return SimpleNamespace(
            id=interview.id,
            token=ready_user.token,
            interview=interview,
        )

    finally:
        db.close()

@pytest.fixture
def ready_question(started_interview):
    return SimpleNamespace(
        id=started_interview.question_id,
        token=started_interview.token,
    )

@pytest.fixture
def ready_finished_interview(client, started_interview, mock_ai):

    response = client.post(
        f"/api/v1/interviews/question/{started_interview.question_id}/answer",
        headers={
            "Authorization": f"Bearer {started_interview.token}"
        },
        json={
            "answer": "My answer"
        },
    )

    assert response.status_code == 200

    return SimpleNamespace(
        id=started_interview.id,
        token=started_interview.token,
    )