from interfaces.function import IFunction
from interfaces.argumentdesc import ArgumentDescriptor


class FirstFunction(IFunction):

    def __init__(self):
        super().__init__("FirstFunction")

        # Define your arguments here. Anything tagged as required
        # will ensure that your functions do not get triggered
        # unless the argument is present.
        self.arguments = {
            '-t': ArgumentDescriptor(True, "Text to alter")
        }

        # Define your menu options
        self.menu_options = {
            "get": {
                "lower": self._alter_text
            }
        }

        # Default hook the help command, don't need to do this yourself
        self._default_hooks()

    def _alter_text(self, *args):
        # Instance of FunctionInput - interfaces\function.py
        function_input = self.get_inputs(args)

        print("CONF", function_input.configuration)
        # If here, required arguments are present and help would
        # have already been dealt with. You simply have to verify
        # that the arguments, if any, have a value that is appropriate
        # then perform whatever it is you want.
        text_to_alter = function_input.arguments['-t']

        if not text_to_alter:
            raise Exception("Must provide text to alter")

        return_val = None
        if 'lower' in function_input.command:
            return_val = text_to_alter.lower()
        else:
            return_val = text_to_alter.upper()

        return return_val
