"""
A function is a class that exposes:

1. Menu choices as a dictionary
{
    "fn" :{
        "fn2" : function_pointer
    }
}
"""
from interfaces.actionitem import ActionItem
from interfaces.argumentdesc import ArgumentDescriptor


class FunctionInput:
    def __init__(self):
        self.arguments = {}
        self.command = None
        self.configuration = {}


class IFunction:
    FN_CONFIGURATION = '-c'
    FN_HELP = '?'

    def __init__(self, name):
        self.name = name
        self.menu_options = {}
        self.arguments = {}
        self.description = None

    def _default_hooks(self):
        self.arguments[IFunction.FN_CONFIGURATION] = ArgumentDescriptor(False, "Comma separated list of configuration names")
        self.arguments[IFunction.FN_HELP] = ArgumentDescriptor(False, "Show help")

    def default_help(self, command):
        print("CMD  > ", " ".join(command))
        if self.description:
            print("INFO > :")
            print(self.description)
        print("ARGS > :")
        print(self.get_pretty_arguments())

    def get_inputs(self, called_args):
        return_value = called_args
        if isinstance(called_args, tuple):
            return_value = called_args[0]
        return return_value

    def get_pretty_arguments(self):
        args = []
        for arg in self.arguments:
            args.append("\t{} : {} : {}".format(
                arg.ljust(5),
                "Required" if self.arguments[arg].required else "Optional",
                self.arguments[arg].description)
            )

        return "\n".join(args)

    def parse_arguments(self, arguments_list):
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
        return self._map_commands()

    def _map_commands(self):
        """
        Maps all of the commands to the functions internally.
        Return is list of ActionItem objects:
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
        commands = []
        for key in sub_dict.keys():
            if isinstance(sub_dict[key], dict):
                found = self._expand_menu(sub_dict[key], " ".join([base, key]))
                commands.extend(found)
            else:
                commands.append(" ".join([base, key]))

        return commands
