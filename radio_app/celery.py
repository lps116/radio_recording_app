import os
from celery import Celery
# setting up celery task queue
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radio_app.settings')

celery_app = Celery('radio_app')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
