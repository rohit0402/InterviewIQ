from fastapi import APIRouter
from app.core.config import settings
from app.tasks.demo import add
router=APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return{
        "status":"healthy",
        "project_name":settings.project_name,
        "version":settings.version
    }



@router.get("/celery-test")
def celery_test():
    task = add.delay(10, 20)
    return {
        "task_id": task.id
    }

