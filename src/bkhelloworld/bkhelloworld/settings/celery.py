import environ

from bkhelloworld.settings.django import BASE_DIR
from pathlib import Path

env = environ.Env(
    CELERY_RESULT_EXPIRES=(int, 60480),
    CELERY_HIDE_TABLES=(bool, False),
)
environ.Env.read_env()

CELERY_BROKER_URL = env.str('CELERY_BROKER_URL') 
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_HIDE_TABLES = env.bool('CELERY_HIDE_TABLES')
CELERY_RESULT_EXPIRES = env.int('CELERY_RESULT_EXPIRES') or None
# settings below doesn't seem to work
CELERY_ENABLE_UTC = True
CELERYD_LOG_FILE = BASE_DIR.joinpath(Path("logs/celery_%n%I.log").resolve())
CELERYD_PID_FILE = BASE_DIR.joinpath(Path("run/celery_%n.pid").resolve())
