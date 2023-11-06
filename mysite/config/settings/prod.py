from .base import *

ALLOWED_HOSTS = ['*']

STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(config('REDIS_HOST'), 6379)],
        },
    },
}

CSRF_TRUSTED_ORIGINS = ['http://localhost:99', 'http://10.0.0.113:99']

NPM_BIN_PATH = config('NPM_BIN_PATH')