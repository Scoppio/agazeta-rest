from settings.base import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Circle CI mysql image/service config
DEBUG = True
CIRCLECI = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'circle_test',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
