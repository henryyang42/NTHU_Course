from NTHU_Course.settings.default import *  # noqa

ALLOWED_HOSTS += [
    '.c9.io',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('IP', '0.0.0.0'),
        'OPTIONS': {
            'read_default_file': CONFIG_PATH,
        },
    }
}

MIDDLEWARE_CLASSES += (
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)
