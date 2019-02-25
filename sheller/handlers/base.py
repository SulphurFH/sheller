from flask import Blueprint
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from sheller.tasks import record_event as record_event_task

routes = Blueprint('sheller', __name__)


class BaseResource(Resource):
    decorators = []

    def __init__(self, *args, **kwargs):
        super(BaseResource, self).__init__(*args, **kwargs)

    def record_event(self, options):
        record_event_task.delay(options)


class BaseRequestParser():
    def __init__(self):
        self.parse = RequestParser()

    def validate(self):
        params = self.parse.parse_args()
        return params


def paginate(query_set, page, page_size, **kwargs):
    count = query_set.count()

    if page < 1:
        abort(400, message='页码需为正数')

    if (page - 1) * page_size + 1 > count > 0:
        abort(400, message='页码超过总数限制')

    if page_size > 250 or page_size < 1:
        abort(400, message='页码范围在(1-250)之间')

    results = query_set.paginate(page, page_size)

    items = [result.to_dict() for result in results.items]

    return {
        'count': count,
        'page': page,
        'page_size': page_size,
        'results': items,
    }
