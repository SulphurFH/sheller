import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sheller import config, __version__

# TODO
NON_REPORTED_EXCEPTIONS = []


def before_send(event, hint):
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if any([(e in str(type(exc_value))) for e in NON_REPORTED_EXCEPTIONS]):
            return None

    return event


def init():
    if config.SENTRY_DSN:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            release=__version__,
            before_send=before_send,
            integrations=[FlaskIntegration()]
        )
