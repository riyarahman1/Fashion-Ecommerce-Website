"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*6_z-pet9vwt3)#g=$sz#o8dloz&x59bwb*(j7r0aiu5v^^hi+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "cartapp",
    "category",
    "myadmin",
    "product",
    "userside",
    'order',
    'paypal.standard.ipn',
 
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['Template'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cartapp.contextprocessor.extras",
            ],
        },
    },
]

WSGI_APPLICATION = "shop.wsgi.application"
RAZOR_KEY_ID=config('RAZOR_KEY_ID')
RAZOR_KEY_SECRET=config("RAZOR_KEY_SECRET")
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
   'default'   : {
    'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
    'NAME'     : 'myprojectfinal',
    'USER'     : 'postgres',
    'PASSWORD' : '12345',
    'HOST'     : 'localhost',
    'PORT'     : '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

AUTH_USER_MODEL = 'accounts.Account'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS= [
    os.path.join(BASE_DIR,"static")
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'



ACCOUNT_SID=config('ACCOUNT_SID')
AUTH_TOKEN=config('AUTH_TOKEN')
COUNTRY_CODE='+91'
TWILIO_PHONE_NUMBER=config('TWILIO_PHONE_NUMBER')
SERVICES=config('SERVICES')



PAYPAL_RECEIVER_EMAIL = 'riyabusiness@gmail.com'

PAYPAL_TEST = True