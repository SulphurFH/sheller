from flask_restful import Api

from sheller.handlers.task_info import TaskListResource, UploadFileResource
from sheller.handlers.monitor import MonitorResource


api = Api()


api.add_resource(TaskListResource, '/api/tasks', endpoint='tasks')
api.add_resource(UploadFileResource, '/api/upload', endpoint='upload')

api.add_resource(MonitorResource, '/api/monitor', endpoint='monitor')
