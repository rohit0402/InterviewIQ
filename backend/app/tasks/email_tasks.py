from app.core.celery_app import celery_app


@celery_app.task
def hello():
    print("Hello from Celery!")
    return "Done"