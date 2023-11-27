"""
Django settings for fapp project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import json
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('pl', _('Polish')),
    # Dodaj więcej języków, jeśli to konieczne
]

LANGUAGE_CODE = 'pl'  # Domyślny język

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#46=!36k#+vrqvq2^ll82619)6z5f$en*t6fb(#%rwe=+yh+4("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "footapp",
    "bootstrapform",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "fapp.urls"

GOOGLE_MAPS_API_KEY = 'AIzaSyDwMapImzhfwehNNbCM8iNGa1E_P5Z8j-k'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
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

WSGI_APPLICATION = "fapp.wsgi.application"

# Database credentials loading
with open(os.path.join(BASE_DIR, "secrets.json")) as secrets_file:
    secrets = json.load(secrets_file)


def get_secret(setting, secrets=secrets):
    """Get secret setting"""
    try:
        return secrets[setting]
    except KeyError:
        raise TypeError("Set the {} setting".format(setting))


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DB_PASSWORD = get_secret("DB_PASSWORD")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "railway",
#         "USER": "postgres",
#         "PASSWORD": DB_PASSWORD,
#         "HOST": "containers-us-west-37.railway.app",
#         "PORT": "5977",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "railway",
        "USER": "postgres",
        "PASSWORD": "*baGcabEbCGa*d*c6C**e11A2fAf4E*c",
        "HOST": "viaduct.proxy.rlwy.net",
        "PORT": "38560",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'my_static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = 'my_media'

    

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = 'home'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'  # Wprowadź właściwy serwer SMTP
EMAIL_PORT = 587  # Port SMTP
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'matelakjakub7@gmail.com'  # Adres e-mail do wysyłania wiadomości
EMAIL_HOST_PASSWORD = 'xNFQ3ZcMGthyIrmU'  # Hasło do skrzynki e-mail