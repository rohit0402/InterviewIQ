from fastapi import APIRouter
from app.core.config import settings
router=APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return{
        "status":"healthy",
        "project_name":settings.project_name,
        "version":settings.version
    }

