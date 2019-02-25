import sys
import logging
import urllib

import redis
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_cors import CORS

from sheller import config


__version__ = '0.1.0'


def setup_logging():
    handler = logging.StreamHandler(sys.stdout if config.LOG_STDOUT else sys.stderr)
    formatter = logging.Formatter(config.LOG_FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(config.LOG_LEVEL)

    if config.LOG_LEVEL != "DEBUG":
        logging.getLogger("passlib").setLevel("ERROR")
        logging.getLogger("requests.packages.urllib3").setLevel("ERROR")
        logging.getLogger("snowflake.connector").setLevel("ERROR")
        logging.getLogger('apiclient').setLevel("ERROR")


def create_redis_connection():
    logging.debug("Creating Sheller connection (%s)", config.REDIS_URL)
    redis_url = urllib.parse.urlparse(config.REDIS_URL)

    if redis_url.scheme == 'redis+socket':
        qs = urllib.parse.parse_qs(redis_url.query)
        if 'virtual_host' in qs:
            db = qs['virtual_host'][0]
        else:
            db = 0

        client = redis.StrictRedis(unix_socket_path=redis_url.path, db=db)
    else:
        if redis_url.path:
            redis_db = redis_url.path[1]
        else:
            redis_db = 0
        redis_password = redis_url.password and urllib.unquote(redis_url.password)
        client = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port, db=redis_db, password=redis_password)

    return client


setup_logging()
redis_connection = create_redis_connection()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address, storage_uri=config.LIMITER_STORAGE)
cors = CORS(resources={"/api/*": {"origins": "*"}})


def create_app():
    from sheller import handlers
    from sheller.models import db
    from sheller.utils import sentry

    sentry.init()

    app = Flask(__name__,
                template_folder=config.TEMPLATE_PATH,
                static_folder=config.STATIC_ASSETS_PATH
                )
    app.config.from_object(config)

    # Nginx Proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, config.PROXIES_COUNT)

    env = app.config['ENV']

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    handlers.init_app(app)
    if env == 'development':
        cors.init_app(app)

    return app


def safe_create_app():
    if current_app:
        return current_app

    return create_app()
