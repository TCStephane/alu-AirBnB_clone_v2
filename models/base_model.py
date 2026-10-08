#!/usr/bin/python3
"""Defines the BaseModel class shared by every model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()
TIME_FMT = "%Y-%m-%dT%H:%M:%S.%f"


def _parse_time(value):
    """Convert an ISO string into a datetime object."""
    try:
        return datetime.strptime(value, TIME_FMT)
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


class BaseModel:
    """Base class providing id, created_at and updated_at."""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new instance from optional keyword arguments."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            if key in ('created_at', 'updated_at') and isinstance(value, str):
                value = _parse_time(value)
            setattr(self, key, value)

    def __str__(self):
        """Return the string representation of the instance."""
        data = dict(self.__dict__)
        data.pop('_sa_instance_state', None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, data)

    def save(self):
        """Update updated_at, add the instance to storage and save it."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        data = dict(self.__dict__)
        data['__class__'] = type(self).__name__
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data.pop('_sa_instance_state', None)
        return data

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
