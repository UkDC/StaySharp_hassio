"""
Django settings for StaySharp project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url
import psycopg2
import django_heroku

USE_TZ = True

TIME_ZONE = "Europe/Kiev"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-mm7+ac%ujk@w#l_&j+zf5nmb^0ms(^k*&s)_y%bo6*ntwpm5*f"

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'm�j9tax!laЭ�l 8оЬt2_+QЭ�)5%a;jбyjpkaq')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "stay_sharp.apps.StaySharpConfig",
    "django_extensions",
    'debug_toolbar',
    'crispy_forms',
    'import_export',
    'psycopg2',
    'django_cleanup',
    'dj_database_url',
    'social.apps.django_app.default',
    'social_django',
    'django_celery_results',
    'django_celery_beat',
    'broker',
    'info_ss',
    'flower',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = "StaySharp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "StaySharp.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        'TIME_ZONE': TIME_ZONE,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'i5205205i@gmail.com'
EMAIL_HOST_PASSWORD = "czpmthctlaiqrkth"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_USE_SSL = True

# Heroku: Обновление конфигурации базы данных из $DATAВASE_URL. import dj_database_url
dЬ_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(dЬ_from_env)

# Статичные файлы (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# Абсолютный путь к каталогу, в котором collectstatic # будет собирать статические файлы для развертывания.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# django_heroku.settings(locals())

# CELERY_BROKER_URL = 'amqp://guest:guest@localhost'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'amqps://cpqhujiw:j7WoBS4lDR345rsJmAsfgPP9Y1xbBzdK@woodpecker.rmq.cloudamqp.com/cpqhujiw'
CELERY_BROKER_POOL_LIMIT = 1
CELERY_BROKER_HEARTBEAT = None
CELERY_BROKER_CONNECTION_TIMEOUT = 30
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_EVENT_QUEUE_EXPIRES = 60
CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TIMEZONE = "Europe/Kiev"
