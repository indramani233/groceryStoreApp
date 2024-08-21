from celery.schedules import crontab
from celery import Celery
from .daily_reminder import send_daily_reminder

app = Celery('scheduler', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'send_daily_reminder': {
        'task': 'celery_tasks.daily_reminder.send_daily_reminder',
        'schedule': crontab(hour=18, minute=0),  # Define your desired time
    },
    
    'generate_monthly_report': {
        'task': 'celery_tasks.monthly_report.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),  # Run on the first day of the month
    },
}

app.conf.timezone = 'UTC'
