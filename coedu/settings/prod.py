from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # TODO: change to False

ALLOWED_HOSTS = ['3.36.220.93', 'co-edu.co.kr']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CRONJOBS = [
    ('0 * * * *', 'coedu.cron.hour_schedule')
]

CRONTAB_DJANGO_SETTINGS_MODULE = 'coedu.settings.prod'
