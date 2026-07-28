from app.core.celery_app import celery_app
from app.tasks.base import BaseTask

@celery_app.task(
    bind=True,
    base=BaseTask,
)
def analyze_interview_task(
    self,
    interview_id: int,
):
    """
    Analyze interview with LLM.
    """
    pass