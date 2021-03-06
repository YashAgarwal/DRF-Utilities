"""
Django settings for startup project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!2q%pnj7brr%2(e89!e+=g4wm4(!g5!vxj#8)qk7!p2t(dic1p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'customer.apps.CustomerConfig',
    'common.apps.CommonConfig',
    'social.apps.SocialConfig',
    'messenger.apps.MessengerConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'startup.urls'

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

WSGI_APPLICATION = 'startup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = './media/'
MEDIA_URL = '/media/'
VERSIONS = ['v1']
BASE_URL = 'BASE_URL'
VERSIONED_BASE_URL = {
    'v1': 'BASE_URL/v1/'
}
VERSIONS = ['v1']
BASE_PORT = 'BASE_PORT'

FACEBOOK = {
    'data_url': 'https://graph.facebook.com/me?fields=id,cover,name,first_name,last_name,age_range,link,gender,locale,picture,timezone,updated_time,verified,email&access_token={platform_token}',
}
REQUIRES_FB_REVIEW = ['user_birthday', 'user_education_history', 'user_hometown',
                      'user_location', 'user_managed_groups', 'user_relationships', 'user_work_history']

GOOGLE = {
    'data_url': 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={platform_token}',
}

LINKEDIN = {
    'auth_url': 'https://www.linkedin.com/oauth/v2/accessToken',
    'auth_header': {
        'v1': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'grant_type': 'authorization_code',
            'code': '{code}',
            'redirect_uri': VERSIONED_BASE_URL['v1'] + 'customer/linkedin_auth',
            'client_id': 'client_id',
            'client_secret': 'client_secret'
        }
    },
    'data_url': 'https://api.linkedin.com/v1/people/~:(id,first-name,last-name,maiden-name,formatted-name,phonetic-first-name,phonetic-last-name,formatted-phonetic-name,headline,industry,current-share,num-connections,num-connections-capped,specialties,positions,picture-url,picture-urls::(original),site-standard-profile-request,api-standard-profile-request,public-profile-url,location:(name),summary)?format=json',
    'data_auth': {
        'Authorization': 'Bearer {platform_token}'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'give email here'
SENDER_EMAIL = 'give email here'
SERVER_EMAIL = 'give email here'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'give email here'
EMAIL_HOST_PASSWORD = 'give password here'
EMAIL_USE_TLS = True
