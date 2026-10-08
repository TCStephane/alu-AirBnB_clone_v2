#!/usr/bin/python3
"""Defines the FileStorage engine (JSON file persistence)."""
import json


class FileStorage:
    """Serializes instances to a JSON file and back."""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return all objects, or only those of the class cls."""
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls = {c.__name__: c for c in self._classes()}.get(cls)
        return {k: v for k, v in FileStorage.__objects.items()
                if type(v) is cls}

    def new(self, obj):
        """Add obj to the objects dictionary."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize the objects dictionary to the JSON file."""
        data = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(data, f)

    def delete(self, obj=None):
        """Delete obj from the objects dictionary if it is inside."""
        if obj is None:
            return
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects.pop(key, None)

    @staticmethod
    def _classes():
        """Return the list of all model classes."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        return [BaseModel, User, State, City, Amenity, Place, Review]

    def reload(self):
        """Deserialize the JSON file into the objects dictionary."""
        classes = {c.__name__: c for c in self._classes()}
        try:
            with open(FileStorage.__file_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        for key, value in data.items():
            FileStorage.__objects[key] = classes[value['__class__']](**value)
