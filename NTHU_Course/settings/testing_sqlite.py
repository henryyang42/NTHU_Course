'''
A configuration for testing in travis CI with sqlite3
'''

from .default import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
        # NAME need not to be supplied,
        # django uses in memory database for testing
    }
}
