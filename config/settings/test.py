from . import *

TESTING = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST_CHARSET": "utf8",
    },
    "second": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST_CHARSET": "utf8",
    }
}

INSTALLED_APPS += ['rest_framework.authtoken']

# Disable migrations during tests
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

EMAIL_FILE_PATH = root('logs/emails')
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.GXTokenAuthentication',
    ),
}
