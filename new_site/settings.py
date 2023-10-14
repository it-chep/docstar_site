import os
from pathlib import Path

from django.shortcuts import render

from .formatters import CustomJsonFormatter
from pythonjsonlogger.jsonlogger import JsonFormatter
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

CSRF_TRUSTED_ORIGINS = ['http://docstar.readyschool.ru', 'http://www.docstar.readyschool.ru',
                        'https://www.docstar.readyschool.ru', 'https://docstar.readyschool.ru', 'http://127.0.0.1', ]

#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['docstar.readyschool.ru', 'www.docstar.readyschool.ru',
                  '127.0.0.1', '81.200.144.45', 'api.ipify.org', 'localhost',
                  'localhost127.0.0.1[::1]']

SERVER_EMAIL = os.getenv('SERVER_EMAIL')
ADMINS = [(os.getenv('ADMIN_NAME'), SERVER_EMAIL)]

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',

    'debug_toolbar',
    'users.apps.UsersConfig',
    'docstar_site.apps.DocstarSiteConfig',
    'vpn.apps.VpnConfig',

    'allauth',
    'allauth.account',
    'guardian'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'new_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

WSGI_APPLICATION = 'new_site.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db (копия).sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'Ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# User
AUTH_USER_MODEL = 'users.CustomUser'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

# Login\logout
LOGIN_REDIRECT_URL = 'homepage'
LOGOUT_REDIRECT_URL = 'homepage'
SITE_ID = 1

TIME_INPUT_FORMATS = ['%H:%M']

STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static'
# ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'docstar_site/docstar/user_photos')
MEDIA_URL = 'user_photos/'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
    '81.200.144.45'
]
# #
# LOGGING = {
#     'version': 1,
#     'disabled_existing_loggers': False,
#
#     'formatters': {
#         'main_format': {
#             'format': '{asctime} - {levelname} - {module} - {filename} - {message}',
#             'style': "{"
#         },
#         'json_formatter': {
#           '()': CustomJsonFormatter,
#         },
#     },
#
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'main_format',
#         },
#         'file': {
#             'class': 'logging.FileHandler',
#             'formatter': 'json_formatter',
#             'filename': 'information.log'
#         },
#     },
#
#     'loggers': {
#         'main': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'docstar_cache'),
    }
}
