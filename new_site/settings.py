import os
from pathlib import Path

from django.shortcuts import render

from .formatters import CustomJsonFormatter
from pythonjsonlogger.jsonlogger import JsonFormatter
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') == 'True'

CSRF_TRUSTED_ORIGINS = [
    'http://doctors.readyschool.ru',
    'http://www.doctors.readyschool.ru',
    'https://www.doctors.readyschool.ru',
    'https://doctors.readyschool.ru',
    'http://testblogers.readyschool.ru',
    'https://testblogers.readyschool.ru',
    'http://www.testblogers.readyschool.ru',
    'https://www.testblogers.readyschool.ru',
    'http://127.0.0.1',
]

ADMIN_TITLE = GRAPPELLI_ADMIN_TITLE = 'MEDBLOGERS BASE'

ALLOWED_HOSTS = [
    'doctors.readyschool.ru',
    'www.doctors.readyschool.ru',
    'testblogers.readyschool.ru',
    'www.testblogers.readyschool.ru',
    '127.0.0.1',
    '81.200.144.45',
    'api.ipify.org',
    'localhost',
    '[::1]',
    '0.0.0.0',
    '188.225.56.163',
]

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
    'users',
    'docstar_site',
    'vpn',
    'infrastructure',
    'tickets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# User
AUTH_USER_MODEL = 'users.CustomUser'

# Login\logout
LOGIN_REDIRECT_URL = 'homepage'
LOGOUT_REDIRECT_URL = 'homepage'
SITE_ID = 1

TIME_INPUT_FORMATS = ['%H:%M']

# STATIC
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = 'staticfiles'

# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, 'docstar_site/docstar/user_photos')
MEDIA_URL = 'media/'

INTERNAL_IPS = [
    '127.0.0.1',
    '188.225.56.163',
    '81.200.144.45'
]

LIMIT_DOCTORS_ON_PAGE = 30

GK_KEY = os.getenv('GK_KEY')
GK_ACCOUNT_NAME = os.getenv('GK_ACCOUNT_NAME')
GK_GROUP_ID = os.getenv('GK_GROUP_ID')
GETCOURCE_TICKETS_TOKEN = os.getenv('GETCOURCE_TICKETS_TOKEN', None)
AVAILABLE_GET_TICKETS_IPS = os.getenv("TILDA_AVAILABLE_IPS", [])

VPN_PRICE = os.getenv('VPN_PRICE')

ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
SALEBOT_API_URL = f"https://chatter.salebot.pro/api/{os.environ.get('SALEBOT_API_KEY')}/callback"
GOOGLE_SHEET_URL = os.getenv('GOOGLE_SHEET_URL')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': os.path.join(BASE_DIR, 'docstar_cache'),
#     }
# }
