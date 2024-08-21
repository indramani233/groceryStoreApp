from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

celery_app.conf.update(
    result_backend='redis://localhost:6379/0',
    #timezone='UTC',
    # Other Celery configurations...
)

celery_app.autodiscover_tasks(['celery_tasks'])
