from werkzeug import datastructures
from sheller.handlers.base import BaseRequestParser


def str_max_length(length):
    def validate(s):
        if len(s) <= length:
            return s
        raise ValueError("String must not greater than %i characters long" % length)
    return validate


class PaginateParser(BaseRequestParser):
    def __init__(self):
        super(PaginateParser, self).__init__()
        self.parse.add_argument('page', type=int, required=True)
        self.parse.add_argument('page_size', type=int, required=False, default=10)


class UploadParser(BaseRequestParser):
    def __init__(self):
        super(UploadParser, self).__init__()
        self.parse.add_argument('file', type=datastructures.FileStorage, location='files')


class CreateTaskParser(BaseRequestParser):
    def __init__(self):
        super(CreateTaskParser, self).__init__()
        self.parse.add_argument('desc', type=str_max_length(32), required=True)
        self.parse.add_argument('image_path', type=str_max_length(100), required=True)
