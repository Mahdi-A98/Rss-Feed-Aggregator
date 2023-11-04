# In the name of GOD
"""
Django settings for rss_feed project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from django.utils.translation import gettext_lazy as _

from celery.schedules import crontab
from dotenv import load_dotenv
from pathlib import Path
import logging
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#******************************************************************************************************************************
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
SECRET_KEY = os.environ.get('SECRET_KEY')
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#******************************************************************************************************************************

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'account',
    'rest_framework',
    'podcast',
    'feedback',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LogMiddleWare',
]

ROOT_URLCONF = 'rss_feed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'rss_feed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('NAME'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD')
    }
}
CACHES = {
    "default":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    "users_white_list":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "podcast.tasks.update_all_podcast",
        "schedule": crontab(minute="*/1"),
    },
}

JWT_CONF = {
    "token_prefix": "Bearer",
    "access_token_exp": 35,
    "refresh_token_exp": 720,
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True
USE_L10N = True

USE_TZ = True

LANGUAGES= [
    ("fa", _("Persian")),
    ("en", _("English")),
]
LOCALE_PATHS = [
BASE_DIR / "locale",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

AUTHENTICATION_BACKENDS = [
    'account.auth.UserAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
        ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'account.auth.JWTAuthentication',
    ]
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALL_CREDENTIALS = True

# celery sttings
CELERY_BROKER_URL =  os.environ.get('CELERY_BROKER_UR', "redis://redis:6379/0") 
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESUALT_BACKEND', "redis://redis:6379/1") 

ELASTICSEARCH_HOST = 'elasticsearch'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'elasticsearch:9200'
        # 'hosts': 'http://localhost:9200'
    },
}

RABBITMQ_HOST = "rabbitmq"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "user_actions_file_handler":{
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/user_actions.log",
            "formatter": "main_formatter",
        },
        "celery_file_handler":{
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/celery_tasks_logs.log",
            "formatter": "main_formatter",
        },
        "Api_file_handler":{
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/Api_endpoints_logs.log",
            "formatter": "main_formatter",
        },

        "user_actions_elastic_handler": {
            "level": "INFO",
            "host": f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}",
            "class": "core.log_handlers.ElasticHandler",
        },
        "Api_elastic_handler": {
            "level": "INFO",
            "host": f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}",
            "class": "core.log_handlers.ElasticHandler",
            "db_name": "Api_logs",
            "daily_index": True,
        },
        "celery_elastic_handler": {
            "level": "INFO",
            "host": f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}",
            "class": "core.log_handlers.ElasticHandler",
            "db_name": "celery_tasks",
            "daily_index": True,
        },
    },
    "formatters": {
        "main_formatter":{
            "format": "{levelname} || {asctime} || {module} || {process:d} || {thread:d} || {message}",
            "style": "{",
        },
    },
    "loggers": {
        "user_actions": {
            "handlers": ["user_actions_file_handler", "user_actions_elastic_handler"], 
            "level": "INFO",
            "propagate": False
        },
        "celery_tasks": {
            "handlers": ["celery_file_handler", "celery_elastic_handler"], 
            "level": "INFO",
            "propagate": False
        },
        "API_logger": {
            "handlers": ["Api_file_handler", "Api_elastic_handler"], 
            "level": "INFO",
            "propagate": False
        },
    }
}