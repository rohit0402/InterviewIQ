from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.resume import router as resume_router
from app.routers import interview
# from app.routers import interview_report
def create_app()->FastAPI:
    setup_logging()

    app=FastAPI(
        title=settings.project_name,
        version=settings.version
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router,prefix=settings.api_v1_prefix)
    app.include_router(auth_router,prefix=settings.api_v1_prefix)
    app.include_router(users_router,prefix=settings.api_v1_prefix)
    app.include_router(resume_router,prefix=settings.api_v1_prefix)
    app.include_router(interview.router,prefix=settings.api_v1_prefix)
    # app.include_router(interview_report.router,prefix=settings.api_v1_prefix)
    return app

app=create_app()