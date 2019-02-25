from sheller import models, limiter
from sheller.handlers.base import BaseResource, paginate
from sheller.utils.decorators import validate_parser
from sheller.utils.generate_code import generate_ts_unique_code
from sheller.config import UPLOAD_PATH
from .parsers import PaginateParser, UploadParser, CreateTaskParser
from .constants import FileType


class TaskListResource(BaseResource):
    decorators = [
        # limiter.limit('10/hour', methods=['GET'], error_message='访问太频繁')
    ]

    @validate_parser(parser_class=PaginateParser())
    def get(self, params):
        tasks = models.Task.all()
        page = params['page']
        page_size = params['page_size']

        context = paginate(
            tasks,
            page,
            page_size
        )
        return context

    @validate_parser(parser_class=CreateTaskParser())
    def post(self, params):
        desc = params['desc']
        image_path = params['image_path']
        models.Task.create(desc=desc, image_path=image_path)
        models.db.session.commit()


class UploadFileResource(BaseResource):

    @validate_parser(parser_class=UploadParser())
    def post(self, params):
        file = params['file']
        code = generate_ts_unique_code(FileType.Image)
        file_name = '%s.%s' % (code, file.filename.split('.')[1])
        file.save(UPLOAD_PATH + file_name)
        context = {
            'file_name': file_name
        }

        self.record_event({
            'action': 'upload',
            'object_id': FileType.Image,
            'object_type': file_name
        })
        return context
