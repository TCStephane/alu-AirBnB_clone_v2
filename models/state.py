#!/usr/bin/python3
"""Defines the State class."""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """Represents a state."""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """Return the City instances linked to this state."""
            from models import storage
            from models.city import City
            return [c for c in storage.all(City).values()
                    if c.state_id == self.id]
