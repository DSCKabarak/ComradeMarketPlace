from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": cmp_db_name,
        "USER": cmp_db_user,
        "PASSWORD": cmp_db_password,
        "HOST": cmp_db_host,
        "PORT": cmp_db_port,
    }
}


# celery settings
# CELERY_BROKER_URL = "amqp://localhost"
# CELERY_RESULT_BACKEND = "amqp://localhost"

# email settings
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS").lower() == "true"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
