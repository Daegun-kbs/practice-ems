from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': config('DB_PORT'),
    }
}

CHANNEL_LAYERS = {
    
}

NPM_BIN_PATH ='C:/Program Files/nodejs/npm.cmd'