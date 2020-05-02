"""Settings for development"""
# pylint: disable=unused-wildcard-import,wildcard-import
from .base import *
ALLOWED_HOSTS = ["0.0.0.0"]
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$sr-v9zx(s!!q)6*2!1#t_+-z5ku*$+=edf*gstxjwz3opj94n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '55432',
    }
}
