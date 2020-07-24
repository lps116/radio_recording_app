"""
Django settings for radio_app project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ
import dj_database_url

# https://stackoverflow.com/questions/54721931/improperlyconfigured-set-the-xxxx-environment-variable-django-environ
# Might have to set up path at some point

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECRET_KEY = '3-timcn76gx#-0mechn8x_8w5e%*me$+f#&rytg#^#z49d2fha'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == "True"

# ALLOWED_HOSTS = ['soundcapture.herokuapp.com/', '127.0.0.1', '0.0.0.0']
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home.apps.HomeConfig',
    'register.apps.RegisterConfig',
    'recordings.apps.RecordingsConfig',
    'account.apps.AccountConfig',
    'django_filters',
    'widget_tweaks',
    'crispy_forms',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'radio_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'radio_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'radioAppDB',
        'USER' : 'linus.strobel',
        'PASSWORD' : 'demo1234',
        'HOST' : 'localhost',
        'PORT' : '5432'
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

# info of media files
# https://overiq.com/django-1-10/handling-media-files-in-django/
MEDIA_ROOT = os.path.join(BASE_DIR, '')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Celery Settings
# https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
# CELERY_BROKER_URL = 'redis://h:pde3be7906537df051b7dafd1a0463bb5a06e75f7346968b68c65db8688a61c1f@ec2-23-21-1-196.compute-1.amazonaws.com:14969'
# CELERY_RESULT_BACKEND = 'redis://h:pde3be7906537df051b7dafd1a0463bb5a06e75f7346968b68c65db8688a61c1f@ec2-23-21-1-196.compute-1.amazonaws.com:14969'
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'


CRISPY_TEMPLATE_PACK = 'bootstrap4'





