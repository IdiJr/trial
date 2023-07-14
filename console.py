#!/usr/bin/python3
""" Entry point of the command interpreter """
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
import json
import shlex


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB_clone program"""

    prompt = "(hbnb) "
    intro = "Welcome to the AirBnB console. Type help or ? to list commands.\n"

    CALLS = [
        'BaseModel', 'User', 'Amenity', 'Place', 'City', 'State', 'Review'
    ]

    list_classes = ['BaseModel', 'User', 'Amenity',
                    'Place', 'City', 'State', 'Review']

    list_commands = ['create', 'show', 'update', 'all', 'destroy', 'count']

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it
        (to the JSON file) and prints the id.
        """
        if not arg:
            print("""** class name missing **""")
        elif arg not in HBNBCommand.list_classes:
            print("*** class doesn't exist ***")
        else:
            mdl = {
                'BaseModel': BaseModel,
                'User': User,
                'Place': Place,
                'City': City,
                'Amenity': Amenity,
                'State': State,
                'Review': Review
            }
            my_model = mdl[arg]()
            print(my_model.id)
            my_model.save()

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id.
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.list_classes:
            print("*** class doesn't exist ***")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for key, value in all_objs.items():
                ob_name = value.__class__.__name__
                ob_id = value.id
                if ob_name == args[0] and ob_id == args[1].strip('"'):
                    print(value)
                    return
                print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name
        and id (save the change into the JSON file)
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.list_classes:
            print("*** class doesn't exist ***")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for key, value in all_objs.items():
                ob_name = value.__class__.__name__
                ob_id = value.id
                if ob_name == args[0] and ob_id == args[1].strip('"'):
                    del value
                    del storage._FileStorage__objects[key]
                    storage.save()
                    return
                print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances
        based or not on the class name.
        """
        if not arg:
            print("** class name missing **")
            return

        args = arg.split(' ')

        if args[0] not in HBNBCommand.list_classes:
            print("*** class doesn't exist ***")
        else:
            all_objs = storage.all()
            list_instances = []
            for key, value in all_objs.items():
                ob_name = value.__class__.__name__
                if ob_name == args[0]:
                    list_instances += [value.__str__()]
                    print(list_instances)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by
        adding or updating attribute (save the change into the JSON file).
        """
        if not arg:
            if not arg:
                print("** class name missing **")
                return

            a = ""
            for argv in arg.split(','):
                a = a + argv

            args = shlex.split(a)

            if args[0] not in HBNBCommand.l_classes:
                print("** class doesn't exist **")
            elif len(args) == 1:
                print("** instance id missing **")
            else:
                all_objs = storage.all()
                for key, objc in all_objs.items():
                    ob_name = objc.__class__.__name__
                    ob_id = objc.id
                    if ob_name == args[0] and ob_id == args[1].strip('"'):
                        if len(args) == 2:
                            print("** attribute name missing **")
                        elif len(args) == 3:
                            print("** value missing **")
                        else:
                            setattr(objc, args[2], args[3])
                            storage.save()
                        return
                    print("** no instance found **")

    def do_count(self, class_name):
        """ Counts number of instances of a class """
        count = 0
        all_objs = storage.all()
        for k, v in all_objs.items():
            class_ = k.split('.')
            if class_[0] == class_name:
                count = count + 1
        print(count)

    def emptyline(self):
        """Does nothing when empty line + Enter is input"""
        pass

    def help_create(self):
        """Creates a new instance of BaseModel, saves, and prints the id."""
        print('\n'.join(['create <object>',
                        'create the named object/instance', ]))

    def help_show(self):
        """Prints an instance based on the class name and id."""
        print('\n'.join(['show <object>',
                        'shows the named object/instant', ]))

    def help_destroy(self):
        """Deletes an instance based on the class name and id."""
        print('\n'.join(['destroy <object>',
                        'Deletes the named object/instant', ]))

    def help_all(self):
        """Prints all instances based or not on the class name."""
        print('\n'.join(['all <object>',
                        'Print all intances based on or not on class name', ]))

    def help_update(self):
        """Updates an instance based on the class name and id"""
        print('\n'.join(['update <class name> <id> <attribute name>',
                        'update attributes of instance, one at a time', ]))

    def complete_create(self, text, line, begidx, endidx):
        if not text:
            completions = self.CALLS[:]
        else:
            completions = [
                f for f in self.CALLS if f.startswith(text)
            ]
            return completions

    def complete_show(self, text, line, begidx, endidx):
        if not text:
            completions = self.CALLS[:]
        else:
            completions = [
                f for f in self.CALLS if f.startswith(text)
            ]
            return completions

    def complete_destroy(self, text, line, begidx, endidx):
        if not text:
            completions = self.CALLS[:]
        else:
            completions = [
                f for f in self.CALLS if f.startswith(text)
            ]
            return completions

    def complete_all(self, text, line, begidx, endidx):
        if not text:
            completions = self.CALLS[:]
        else:
            completions = [
                f for f in self.CALLS if f.startswith(text)
            ]
            return completions

    def complete_update(self, text, line, begidx, endidx):
        if not text:
            completions = self.CALLS[:]
        else:
            completions = [
                f for f in self.CALLS if f.startswith(text)
            ]
            return completions

    def do_quit(self, line):
        """Close the cmd window, and exit: when quit is input"""
        print("Thank you for using hbnb :)")
        return True

    def do_EOF(self, line):
        """Close the cmd window, and exit: when EOF or Ctrl-D is input"""
        print("Thank you for using hbnb :)")
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
