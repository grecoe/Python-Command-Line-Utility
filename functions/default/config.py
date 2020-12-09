import os
import json
from interfaces import IFunction, ArgumentDescriptor


class ConfigFn(IFunction):
    CONFIGURATION_FILE = "user_settings.json"

    def __init__(self):
        super().__init__("Config Util")

        self.argkeys = ['-n', '-v']
        self.arguments = {
            '-n': ArgumentDescriptor(False, "Configuration name"),
            '-v': ArgumentDescriptor(False, "Configuration value")
        }

        self.menu_options = {
            "config": {
                "get": self.get_config_value,
                "set": self.set_config_value,
                "list": self.list_config_values
            }
        }

        # Default hook the help command, don't need to do this yourself
        self.set_default_hooks()

    def get_config_value(self, *args):
        """
        Get a configuration value (print)
        """
        # Instance of FunctionInput - interfaces\function.py
        function_input = self.get_inputs(args)
        arg = '-n'

        if arg not in function_input.arguments.keys():
            err = "Argument {} required ({})".format(arg, self.arguments[arg].description)
            raise Exception(err)

        value = self.read_configuration_value(function_input.arguments[arg])

        print("{} = ({}) {}".format(function_input.arguments[arg], type(value), value))

    def read_configuration_value(self, val_key):
        """
            Read from the configuration file the value at
            val_key.

            This is used internally and by the app itself.
        """
        settings = self._load_configuration()
        value = None
        if val_key in settings.keys():
            value = settings[val_key]
        return value

    def set_config_value(self, *args):
        """
            Set a configuraiton value
        """
        # Instance of FunctionInput - interfaces\function.py
        function_input = self.get_inputs(args)
        settings = self._load_configuration()

        # Set requires both -n and -v to be present
        for arg in self.argkeys:
            if arg not in function_input.arguments.keys():
                err = "Argument {} required ({})".format(arg, self.arguments[arg].description)
                raise Exception(err)

        output_value = function_input.arguments['-v']
        if '[' in output_value or '{' in output_value:
            output_value = json.loads(output_value)

        settings[function_input.arguments['-n']] = output_value

        self._save_configuration(settings)

    def list_config_values(self, *args):
        """
            List names of all configuration values. This
            function does not require input, but it's getting
            it anyway.
        """
        # Instance of FunctionInput - interfaces\function.py
        settings = self._load_configuration()

        if len(settings):
            print("Configuration Settings:")
            for setting in settings.keys():
                print("\t{}".format(setting))

    def _save_configuration(self, settings):
        directory = os.path.split(__file__)[0]
        file_path = os.path.join(directory, ConfigFn.CONFIGURATION_FILE)

        with open(file_path, "w") as settings_file:
            file_data = json.dumps(settings, indent=4)
            settings_file.write(file_data)

    def _load_configuration(self):
        directory = os.path.split(__file__)[0]
        file_path = os.path.join(directory, ConfigFn.CONFIGURATION_FILE)

        settings = {}

        if os.path.exists(file_path):
            with open(file_path, "r") as settings_file:
                file_data = settings_file.readlines()
                file_data = "\n".join(file_data)
                settings = json.loads(file_data)

        return settings
