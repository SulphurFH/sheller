from celery import Celery
from celery.signals import worker_process_init
from flask import current_app
from sheller import config, safe_create_app


celery = Celery(
    'sheller',
    broker=config.CELERY_BROKER_URL,
    include='sheller.tasks'
)

celery_schedule = {

}

celery.conf.update(
    result_backend=config.CELERY_RESULT_BACKEND,
    beat_schedule=celery_schedule,
    timezone=config.CELERY_TIMEZONE,
    result_expires=config.CELERY_RESULT_EXPIRES,
    worker_log_format=config.CELERY_WORKER_LOG_FORMAT,
    worker_task_log_format=config.CELERY_WORKER_TASK_LOG_FORMAT
)

TaskBase = celery.Task


class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)


celery.Task = ContextTask


@worker_process_init.connect
def init_celery_flask_app(**kwargs):
    app = safe_create_app()
    app.app_context().push()
