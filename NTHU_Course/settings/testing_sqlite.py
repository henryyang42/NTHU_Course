'''
A configuration for testing in travis CI with sqlite3
'''

from .default import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # https://docs.djangoproject.com/en/1.10/topics/testing/overview/#the-test-database
        # django uses in memory database for testing
        'NAME': ':memory:'
    }
}
