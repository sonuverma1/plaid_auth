import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plaid_auth.settings')

app = Celery('plaid_auth')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
