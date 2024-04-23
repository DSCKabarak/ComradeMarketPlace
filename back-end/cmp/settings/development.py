import os
from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("CMP_DB_NAME"),
        "USER": os.environ.get("CMP_DB_USER"),
        "PASSWORD": os.environ.get("CMP_DB_PASSWORD"),
        "HOST": os.environ.get("CMP_DB_HOST"),
        "PORT": os.environ.get("CMP_DB_PORT"),
    }
}
