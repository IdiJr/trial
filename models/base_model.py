#!/usr/bin/pyhon3
""" Parent class that defines all attributes/methods
for all other classes
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """ Initialises all common attributes/methods """
    def __init__(self, *args, **kwargs):
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)
        else:
            f = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(kwargs, f)
                if key != '__class__':
                    setattr(self, key, value)

    def __str__(self):
        """Returns string representation of class name, id and
        attribute dictionary
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """ Updates the time for last update"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ Returns dictionary representation of BaseModel instances """
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
