import functools
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
from sheller import config


class ShellerSQLAlchemy(SQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(ShellerSQLAlchemy, self).apply_pool_defaults(app, options)
        if config.SQLALCHEMY_DISABLE_POOL:
            options['poolclass'] = NullPool


db = ShellerSQLAlchemy(session_options={
    'expire_on_commit': False

})
db.configure_mappers()

Column = functools.partial(db.Column, nullable=False)
