# Replace do_create in YOUR console.py with this (needs `import re` at top).
# Adapt `HBNBCommand.classes` to however your v1 console stores classes.
    def do_create(self, arg):
        """Create a new instance: create <Class> <key>=<value> ..."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        kwargs = {}
        for param in args[1:]:
            if '=' not in param:
                continue
            key, value = param.split('=', 1)
            if value.startswith('"') and value.endswith('"') \
                    and len(value) >= 2:
                inner = value[1:-1]
                if re.search(r'(?<!\\)"', inner):
                    continue
                value = inner.replace('\\"', '"').replace('_', ' ')
            else:
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    continue
            kwargs[key] = value
        obj = HBNBCommand.classes[args[0]](**kwargs)
        obj.save()
        print(obj.id)
