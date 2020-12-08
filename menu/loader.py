import os
import importlib
from interfaces.function import IFunction


class FunctionLoader:
    def __init__(self):
        self.functions = []

    def load_functions(self, folder):
        if not os.path.exists(folder):
            raise Exception("Folder does not exist")

        for root, dirs, files in os.walk(folder):
            for name in files:
                # Get the full path
                file_path = os.path.join(root, name)
                # Now trim off the "extension" we expect '.py'
                ext = file_path[len(file_path) - 3:]

                if ext.lower() == '.py':
                    # It is a .py file, so modify it accordingly to make
                    # a module name.
                    module_name = self._get_module_from_path(file_path)

                    # Load the module
                    game_module = importlib.import_module(module_name)
                    for obj in dir(game_module):
                        contained_obj = getattr(game_module, obj)

                        if callable(contained_obj):
                            try:
                                built_obj = contained_obj()
                                if issubclass(built_obj.__class__, IFunction):
                                    self.functions.append(built_obj)
                            except TypeError as ex:
                                # Expected failure on any object that does not have a
                                # parameterless constructor.
                                pass

    def _get_module_from_path(self, file_path=None):
        # Remove leading . / or \
        file_path = file_path.strip("./\\")
        # Convert any remaining \ or / to a .
        file_path = file_path.replace("\\", ".")
        file_path = file_path.replace("/", ".")

        # Now we have the module name
        return file_path[:len(file_path) - 3]
