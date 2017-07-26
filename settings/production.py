from settings.base import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'agazeta',
        'USER': config('DATABASE_USER_PROD'),
        'PASSWORD': config('DATABASE_PASSWORD_PROD'),
        'HOST': config('DATABASE_URL_PROD'),
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
