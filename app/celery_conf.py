from celery import Celery

celery = Celery('reports', broker='mongodb://localhost:27017/report_tasks')

celery.conf.update(
    CELERY_RESULT_BACKEND="mongodb",
    CELERY_MONGODB_BACKEND_SETTINGS={
        "host": "localhost",
        "port": 27017,
        "database": "report_tasks"
    })
