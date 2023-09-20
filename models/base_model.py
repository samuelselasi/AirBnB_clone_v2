#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from models import storage
from sqlalchemy import Column, Integer, String, DateTime

time_frmt = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()


class BaseModel:
    """This is orm base class for all hbnb models"""

    id = Column(String(60), primary_key=true, unique=True, nullable=False)
    created_at = column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """instance intialization function to
        create a new model"""

        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            for key, val in kwargs.items():
                if key == '__class__':
                    continue
                setattr(self, key, val)
                if type(self.created_at) is str:
                    self.created_at = datetime.strptime(self.created_at,
                                                        time_frmt)
                if type(self.updated_at) is str:
                    self.updated_at = datetime.strptime(self.updated_at,
                                                        time_frmt)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()

        # remove _sa_instance_state key only if exist
        new_dict.pop('_sa_instance_state', None)

        return (my_dict)

    def delete(self):
        """ delete current instance from the storage (models.storage)
        by calling the method delete from FileStorage class
        we are using __init__ , So storage = FileStorage()"""
        storage.delete()
