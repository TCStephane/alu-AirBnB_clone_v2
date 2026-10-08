#!/usr/bin/python3
"""Module defining FileStorage, which persists objects in a JSON file."""
import json
import os


class FileStorage:
    """Serialize instances to a JSON file and deserialize them back."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return all stored objects, optionally only those of cls."""
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls = {c.__name__: c for c in self._classes()}.get(cls)
        return {key: obj for key, obj in FileStorage.__objects.items()
                if type(obj) is cls}

    def new(self, obj):
        """Add obj to the stored objects using the key <class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def delete(self, obj=None):
        """Delete obj from the stored objects if it is inside."""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects.pop(key, None)

    @staticmethod
    def _classes():
        """Return the list of every model class."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        return [BaseModel, User, State, City, Amenity, Place, Review]

    def save(self):
        """Serialize all stored objects to the JSON file."""
        data = {key: obj.to_dict()
                for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def reload(self):
        """Deserialize the JSON file into objects if the file exists."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = {"BaseModel": BaseModel, "User": User, "State": State,
                   "City": City, "Amenity": Amenity, "Place": Place,
                   "Review": Review}
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            FileStorage.__objects[key] = classes[value["__class__"]](**value)
