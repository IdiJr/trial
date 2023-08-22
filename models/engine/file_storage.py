#!/usr/bin/python3
""" Class that serializes instances to JSON file
and deserializes JSON file to intances
"""
import json
import os


class FileStorage:
    """ Serializes objects/instances to JSON file and
    deserializes JSON files to objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects """
        if cls is None:
            return self.__objects
        else:
            obj_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    obj_dict[key] = value
            return obj_dict

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file  """
        dictionary = {}

        for key, value in self.__objects.items():
            dictionary[key] = value.to_dict()

        with open(self.__file_path, "w") as f:
            json.dump(dictionary, f)

    def reload(self):
        """ Deserializes the JSON file to __objects """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.city import City
        from models.amenity import Amenity
        from models.state import State
        from models.review import Review        
        mdl = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'City': City,
            'Amenity': Amenity,
            'State': State,
            'Review': Review
        }

        if os.path.exists(self.__file_path) is True:
            with open(self.__file_path, "r") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    self.new(mdl[value['__class__']](**value))
