import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

app = Celery('mailing')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_data-every-single-minute': {
        'task': 'main_app.tasks.start_mailing',
        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}





app.autodiscover_tasks()





# app = Celery('tasks', broker='redis://localhost:6379/0')
# app.conf.beat_schedule = {
#     'update_data-every-single-minute': {
#         'task': 'tasks.start_mailing',
#         'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#     },
# }
