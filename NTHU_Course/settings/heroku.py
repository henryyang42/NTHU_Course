import dj_database_url

from .default import *  # noqa


DATABASES['default'] = dj_database_url.config()  # noqa: F405

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECRET_KEY = os.environ['SECRET_KEY']  # noqa: F405

ALLOWED_HOSTS = ['*']
