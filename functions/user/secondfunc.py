from interfaces import IFunction, ArgumentDescriptor


class SecondFunction(IFunction):

    def __init__(self):
        # Base class expectes name in constructor
        super().__init__("SecondFunction")

        # Define your funciton arguments here
        self.arguments = {
            '-b': ArgumentDescriptor(True, "Some description"),
            '-c': ArgumentDescriptor(True, "Another description")
        }

        # Define your function menu options
        self.menu_options = {
            "put": {
                "unlimited": {
                    "power": self._get_lower_name
                }
            }
        }

        # Default hook the help command, don't need to do this yourself
        self.set_default_hooks()

    def _get_lower_name(self, *args):
        # Instance of FunctionInput - interfaces\function.py
        function_input = self.get_inputs(args)

        # If here, required arguments are present and help would
        # have already been dealt with. You simply have to verify
        # that the arguments, if any, have a value that is appropriate
        # then perform whatever it is you want.
        print("Action :", self.name)
        print("Command :", function_input.command)
        print("Arguments :", function_input.arguments)