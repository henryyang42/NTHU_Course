import os
from django.core.wsgi import get_wsgi_application
"""
WSGI config for NTHU_Course project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NTHU_Course.settings.default")

application = get_wsgi_application()


if os.environ['DJANGO_SETTINGS_MODULE'] == 'NTHU_Course.settings.heroku':
    from dj_static import Cling
    application = Cling(application)
