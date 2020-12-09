"""
A function is a class that exposes:

1. Menu choices as a dictionary
{
    "fn" :{
        "fn2" : function_pointer
    }
}
"""
from interfaces import ActionItem, ArgumentDescriptor, FunctionInput


class IFunction:
    """
    IFunction is a base class to be used by any class that wishes to be part of the 
    application. 

    This base class provides useful functionality so that each function implementation 
    does not need to provide it. 
    """

    """
    Static class memebers for default provided menu options, should the implementor want them
    in their own IFunction instance.

    ?  - Help, if set implementor does not need to do any work for help. Options and information
         will be shown to the user if they trigger the function with a ? argument.
    -c - If set, the user can provide a list of names for configuration settings they want 
         passed along from the application configuration (functions/default/config)
    """
    FN_CONFIGURATION = '-c'
    FN_HELP = '?'

    def __init__(self, name):
        """
        Class has four members

        name:
            Provided by the implmentor in the IFunction instance constructor.
            The name of the function, which has nothing to do with how it 
            appears in any menu.
        description:
            Provided by the implmentor in the IFunction instance constructor.

            A textual description of the function. 
            If provided, it will be displayed if the user asks for help. 
        menu_options:
            Provided by the implmentor in the IFunction instance constructor.

            A dictionary that breaks down what menu options the IFunciton instance
            is going to provide to the user along with bound functions to call if the 
            menu option is selected. 

            This is used by the Menu class.

            Ex: Binding to "get status" the menu would be 
            {
                "get" : {
                    "status" : <class funciton to support>
                }
            }    
        arguments:
            Provided by the implmentor in the IFunction instance constructor.

            A list of arguments that the function will accept. This too is a dictionary
            that defines which arguments are accepted. 

            The dictionary is:
            key = actual argument to accept, i.e. '-t'
            value = Instance of ArgumentDescriptor
        """
        self.name = name
        self.menu_options = {}
        self.arguments = {}
        self.description = None

    def set_default_hooks(self, help=True, config=True):
        """
        In the implementors IFunction derived constructor, this call can be used to 
        add in additional arguments to the IFunction implementation.

        Because help (?) or configuration (-c) are common to all implementations, they
        are provided through the base class.

        help:
            If true, the ? argument is added
        config:
            If true, the -c argument is added
        """
        if config:
            self.arguments[IFunction.FN_CONFIGURATION] = ArgumentDescriptor(False, "Comma separated list of configuration names")
        if help:
            self.arguments[IFunction.FN_HELP] = ArgumentDescriptor(False, "Show help")

    def default_help(self, command):
        """
        If the ? argument is present, this is called on behalf of the implememtor assuming
        that the ? argument was added to the list of acceptable arguments. 

        This shows information about the IFunction implmementation to the user.
        """
        print("CMD  > ", " ".join(command))
        if self.description:
            print("INFO > :")
            print(self.description)
        print("ARGS > :")
        print(self.get_pretty_arguments())

    def get_inputs(self, called_args):
        """
        Can be used in all bound functions on the IFunction instance.

        All bound functions are passed a single parameter through *args which 
        is translated by Python to a tuple. 

        That single parameter in tuple[0], if present, will be a FunctionInput instance.
        """
        return_value = called_args
        if isinstance(called_args, tuple):
            return_value = called_args[0]
        return return_value

    def get_pretty_arguments(self):
        """
        Function used by default_help to display the accepted arguments
        to the IFunction implementation.
        """
        args = []
        for arg in self.arguments:
            args.append("\t{} : {} : {}".format(
                arg.ljust(5),
                "Required" if self.arguments[arg].required else "Optional",
                self.arguments[arg].description)
            )

        return "\n".join(args)

    def parse_arguments(self, arguments_list):
        """
        Parses the arguments that the user has entered. This call is utilized in the 
        main application loop (app.py) to parse out arguments. 

        arguments_list:
            A list of strings of the remaining input from the user that did not trigger
            a find on the menu options. Considered remainder of that command line must 
            be arguments to the IFunction instance.

        Returns:
            A dictionary of arguments key=arg and value=what user entered.

            Values in this case may be None if the argument is used simply as a flag.

        Exceptions:
            - ? was found as an argument
            - An unexpected argument was found 
            - A required argument is not present (though does NOT enforce if present
              that it has any value associated with it. )
        """
        args = {}

        current_arg = None
        current_arg_input = []
        unexpected_arguments = []
        if arguments_list:
            # If we get an unexpected argument we need to throw here
            if arguments_list[0].lower() not in self.arguments.keys():
                unexpected_arguments.append(arguments_list[0].lower())

            for arg in arguments_list:
                if arg.lower() in self.arguments.keys():
                    if current_arg:
                        args[current_arg] = " ".join(current_arg_input) if current_arg_input else None
                        current_arg_input = []
                    current_arg = arg.lower()
                else:
                    current_arg_input.append(arg)

            if current_arg not in args.keys():
                args[current_arg] = " ".join(current_arg_input) if current_arg_input else None

        # See if we got help anywhere, if not, make sure nothing unexpected
        if IFunction.FN_HELP in args.keys():
            raise Exception("Function Help")
        elif len(unexpected_arguments):
            unexpected = ",".join(unexpected_arguments)
            raise Exception("Unexpected argument > {}".format(unexpected))

        # Now that we have them all, ensure any required args are present.
        for arg in self.arguments.keys():
            if self.arguments[arg].required:
                if arg not in args.keys():
                    raise Exception("Required argument {} is not present".format(arg))

        return args

    def get_command_mapping(self):
        """
        Used by the Menu.add_function call to break down this instance of
        an IFunction into consumable parts to be added the the main application
        menu. 
        """
        return self._map_commands()

    def _map_commands(self):
        """
        Maps all of the commands to the functions internally.
        Return is list of ActionItem objects that will be used
        by the Menu class to present this IFunction instance as
        options in the menu.
        """
        commands = []
        for key in self.menu_options.keys():
            if isinstance(self.menu_options[key], dict):
                commands.extend(self._expand_menu(self.menu_options[key], key))
            else:
                commands.append(key)

        action_map = []
        for cmd in commands:
            split_commands = cmd.split(' ')
            current_action = self.menu_options[split_commands[0]]
            for idx in range(1, len(split_commands)):
                current_action = current_action[split_commands[idx]]

            action_map.append(ActionItem(cmd, current_action))
        return action_map

    def _expand_menu(self, sub_dict, base):
        """
        Used by _map_commands to recursively build up options to be passed
        back out for the Menu class to represent this instance.

        sub_dict:
            A child of the menu option to parse next
        base:
            String of the base functionality (so that the full command can be built)
        """
        commands = []
        for key in sub_dict.keys():
            if isinstance(sub_dict[key], dict):
                found = self._expand_menu(sub_dict[key], " ".join([base, key]))
                commands.extend(found)
            else:
                commands.append(" ".join([base, key]))

        return commands
