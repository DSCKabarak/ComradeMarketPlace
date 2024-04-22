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
