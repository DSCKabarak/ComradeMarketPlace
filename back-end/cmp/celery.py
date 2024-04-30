import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"cmp.settings.{os.getenv('SETTINGS')}")
app = Celery("cmp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
