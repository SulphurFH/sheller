from .helpers import fix_assets_path

PROXIES_COUNT = 1

# Connection Config for Sheller's own database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@127.0.0.1:3306/sheller?charset=utf8'
SQLALCHEMY_DISABLE_POOL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
DATABASE_QUERY_TIMEOUT = 0.5

# Logger
LOG_LEVEL = 'INFO'
LOG_STDOUT = False
LOG_PREFIX = 'sheller'
LOG_FORMAT = LOG_PREFIX + ':[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s'

# Static
STATIC_ASSETS_PATH = fix_assets_path('../client/app/dist/static/')
TEMPLATE_PATH = fix_assets_path('../client/app/dist/')

# Storage File
UPLOAD_PATH = fix_assets_path('../storage/images/')
DOWNLOAD_PATH = fix_assets_path('../storage/audio/')

# Redis
REDIS_URL = 'redis://127.0.0.1:6379/0'

# Sentry
SENTRY_DSN = ''

try:
    from .local_settings import *   # noqa
    print('\033[1;33;44mlocal_settings imported.!\033[0m')
except ImportError:
    pass

LIMITER_STORAGE = REDIS_URL

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_RESULT_EXPIRES = 3600 * 24
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_WORKER_LOG_FORMAT = LOG_PREFIX + ':[%(asctime)s][PID:%(process)d][%(levelname)s][%(processName)s] %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = LOG_PREFIX + \
    '[%(asctime)s][PID:%(process)d][%(levelname)s][%(processName)s] task_name=%(task_name)s \
    task_id=%(task_id)s %(message)s'
