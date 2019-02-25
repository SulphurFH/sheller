import click
import logging
from flask import current_app
from flask.cli import FlaskGroup
from flask_sqlalchemy import get_debug_queries

from sheller import create_app, __version__
from sheller.cli import database


def create(group):
    app = current_app or create_app()
    group.app = app

    @app.shell_context_processor
    def shell_context():
        from sheller import models
        return dict(models=models)

    @app.after_request
    def after_request(response):
        from sheller import config
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        for query in get_debug_queries():
            if query.duration >= config.DATABASE_QUERY_TIMEOUT:
                logging.warning(('SLOW QUERY: %s\nParameters: %s\nDuration: %fs'
                                 '\nContext: %s\n'
                                 ).format(query.statement, query.parameters, query.duration, query.context))
        return response

    return app


@click.group(cls=FlaskGroup, create_app=create)
def manager():
    """Management script for Sheller"""


manager.add_command(database.manager, "database")


@manager.command()
def version():
    """Displays Sheller version."""
    print(__version__)


@manager.command()
def ipython():
    """Starts IPython shell instead of the default Python shell."""
    import sys
    import IPython
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app

    banner = 'Python %s on %s\nIPython: %s\nSheller version: %s\n' % (
        sys.version,
        sys.platform,
        IPython.__version__,
        __version__
    )

    ctx = {}
    ctx.update(app.make_shell_context())

    IPython.embed(banner1=banner, user_ns=ctx)
