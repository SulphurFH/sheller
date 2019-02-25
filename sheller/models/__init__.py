from .base import db, Column
from .mixins import TimestampMixin


class Task(TimestampMixin, db.Model):
    id = Column(db.Integer(), primary_key=True)
    desc = Column(db.String(32))
    image_path = Column(db.String(255))
    content = Column(db.Text, nullable=True)
    audio_path = Column(db.String(255), nullable=True)

    __tablename__ = 'tasks'

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'desc': self.desc,
            'image_path': self.image_path,
            'content': self.content,
            'audio_path': self.audio_path
        }

    @classmethod
    def all(cls):
        tasks = cls.query.filter().order_by(cls.id.asc())
        return tasks

    @classmethod
    def create(cls, *args, **kwargs):
        task = cls(*args, **kwargs)
        db.session.add(task)
        return task


class Event(db.Model):
    id = Column(db.Integer, primary_key=True)
    created_at = Column(db.DateTime(True), default=db.func.now())
    action = Column(db.String(255))
    object_type = Column(db.String(255))
    object_id = Column(db.String(255), nullable=True)

    __tablename__ = 'events'

    @classmethod
    def record(cls, raw_event):
        action = raw_event.pop('action')
        object_type = raw_event.pop('object_type')
        object_id = raw_event.pop('object_id', None)

        event = cls(action=action,
                    object_type=object_type,
                    object_id=object_id)
        db.session.add(event)
