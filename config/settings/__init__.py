"""Main settings for project Bitrix-API"""
import environ

root = environ.Path(__file__) - 3
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(root('.env'))

# ROOT Directory
BASE_DIR = root()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'rest_framework',

    'clients',
    'users',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("BX_DB_NAME"),
        "USER": env("BX_DB_USER"),
        "PASSWORD": env("BX_DB_PASSWORD"),
        "PORT": "",
        "HOST": env("BX_DB_HOST"),
        'TEST': {
            'CHARSET': 'utf8',
        },
        'AUTOCOMMIT': True,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    'second': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("GX_DB_NAME"),
        "USER": env("GX_DB_USER"),
        "PASSWORD": env("GX_DB_PASSWORD"),
        "PORT": "",
        "HOST": env("GX_DB_HOST"),
        'TEST': {
            'CHARSET': 'utf8',
        },
        'AUTOCOMMIT': True,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AUTH_USER_MODEL = 'users.User'

# Password validation

AUTH_PASSWORD_VALIDATORS = []

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'


# REST Framework configuration

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.GXTokenAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': '%b %d %H:%M:%S',
        },
    },
    'handlers': {
        # Mute
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        # Sends all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'actions': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': root('logs/actions.log'),
            'formatter': 'verbose',
        },
        'errors': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': root('logs/errors.log'),
            'formatter': 'verbose',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': root('logs/debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['errors'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'actions': {
            'handlers': ['actions', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'db': {
            'handlers': ['errors', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps': {
            'handlers': ['debug_file', 'errors'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


# Project settings
DEPARTMENT_BANK = 12
