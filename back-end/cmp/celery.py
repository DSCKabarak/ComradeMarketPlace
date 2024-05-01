import logging
import os

from celery import Celery
from celery.signals import after_setup_task_logger
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"cmp.settings.{os.getenv('SETTINGS')}")
app = Celery("cmp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


def setup_logging(**kwargs):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler = logging.FileHandler("log/celery.log")
    handler.setFormatter(formatter)

    logger = logging.getLogger("celery")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


after_setup_task_logger.connect(setup_logging)
