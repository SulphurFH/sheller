from celery.utils.log import get_task_logger

from sheller import models
from sheller.worker import celery

logger = get_task_logger(__name__)


@celery.task(name='sheller.tasks.record_event')
def record_event(raw_event):
    models.Event.record(raw_event)
    models.db.session.commit()
