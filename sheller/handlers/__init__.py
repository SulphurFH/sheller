from flask import render_template
from sheller.handlers.api import api
from sheller.handlers.base import routes


@routes.route('/', methods=['GET'], defaults={'path': ''})
@routes.route('/<path:path>')
def index(path):
    return render_template('index.html')


def init_app(app):
    app.register_blueprint(routes)
    api.init_app(app)
