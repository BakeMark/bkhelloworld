import environ

from .django import *
# from .bootstrap import *

# from .celery  import *
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()

DEBUG = env('DEBUG', default=True)
SECRET_KEY = env('SECRET_KEY')
GREETINGS = env('GREETINGS', default=None)  # test env file

ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS')]


INSTALLED_APPS.extend([

    'bootstrap3',
    'core',
    # add apps here
])
if DEBUG:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = ['127.0.0.1', ]

DATABASES = {
    'default': env.db(),


}

SERVER_EMAIL = env.str('SERVER_EMAIL', default='')
SERVER_URL = env.url('SERVER_URL', default='')

EMAIL_HOST = env.str('EMAIL_HOST', default=None)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=False)
EMAIL_SENDER = env.str('EMAIL_SENDER', default='')
EMAIL_ADMIN = env.str('EMAIL_ADMIN', default='')

DATETIME_FORMAT = 'N j, Y'
DATE_FORMAT = 'N j, Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, '../../assets/media/'))
MEDIA_ROOT = BASE_DIR.joinpath(Path('../../assets/media/').resolve())
# STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, '../../assets/static/'))
STATIC_ROOT = BASE_DIR.joinpath((Path('../../assets/static/').resolve()))

STATICFILES_DIRS = [
    # os.path.normpath(os.path.join(BASE_DIR, "../static/")),
    BASE_DIR.joinpath(Path('../static/').resolve())
]

# if DEBUG:
#     print("DATABASES = {}".format(DATABASES))
