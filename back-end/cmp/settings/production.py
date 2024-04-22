from .base import *

DEBUG = False

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

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
