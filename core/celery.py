import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whatsapp_sms.settings")
app = Celery("whatsapp_sms")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()