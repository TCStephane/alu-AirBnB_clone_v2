#!/usr/bin/python3
"""Entry point of the AirBnB clone command interpreter."""
import cmd
import re
import shlex
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter to manage AirBnB objects."""

    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel, "User": User, "State": State,
               "City": City, "Amenity": Amenity, "Place": Place,
               "Review": Review}

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program
        """
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def _split(self, arg):
        """Split arg into words, keeping double-quoted strings together."""
        try:
            return shlex.split(arg)
        except ValueError:
            return arg.split()

    def _get_key(self, arg):
        """Validate class name and id from arg and return the storage key."""
        args = self._split(arg)
        if not args:
            print("** class name missing **")
            return None
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return None
        if len(args) < 2:
            print("** instance id missing **")
            return None
        key = "{}.{}".format(args[0], args[1])
        if key not in models.storage.all():
            print("** no instance found **")
            return None
        return key

    def do_create(self, arg):
        """Create an instance: create <Class> <key>=<value> ...
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        kwargs = {}
        for param in args[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)
            if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                inner = value[1:-1]
                if re.search(r'(?<!\\)"', inner):
                    continue
                value = inner.replace('\\"', '"').replace("_", " ")
            else:
                try:
                    value = float(value) if "." in value else int(value)
                except ValueError:
                    continue
            kwargs[key] = value
        obj = self.classes[args[0]](**kwargs)
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Print the string representation of an instance
        """
        key = self._get_key(arg)
        if key:
            print(models.storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id
        """
        key = self._get_key(arg)
        if key:
            models.storage.delete(models.storage.all()[key])
            models.storage.save()

    def do_all(self, arg):
        """Print all instances, optionally filtered by class name
        """
        args = self._split(arg)
        if args and args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        objs = models.storage.all(self.classes[args[0]] if args else None)
        print([str(obj) for obj in objs.values()])

    def do_update(self, arg):
        """Update an instance by adding or updating one attribute
        """
        key = self._get_key(arg)
        if not key:
            return
        args = self._split(arg)
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = models.storage.all()[key]
        name, value = args[2], args[3]
        if hasattr(obj, name):
            try:
                value = type(getattr(obj, name))(value)
            except (ValueError, TypeError):
                pass
        else:
            for cast in (int, float):
                try:
                    value = cast(value)
                    break
                except ValueError:
                    pass
        setattr(obj, name, value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
