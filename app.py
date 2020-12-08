from menu.loader import FunctionLoader
from menu.appmenu import Menu
from interfaces.function import IFunction, FunctionInput
from logutils.tracer import LogDecorator

# This loads up any implementations of IFunction for the app
# from whatever disk path you pass.
loader = FunctionLoader()
loader.load_functions = LogDecorator(loader.load_functions)
loader._get_module_from_path = LogDecorator(loader._get_module_from_path)
loader.load_functions("./functions/user")
loader.load_functions("./functions/default")

# Get the configuration class
configuration_util = None
fns = [x for x in loader.functions if x.name == 'Config Util']
if len(fns):
    configuration_util = fns[0]

# Create the menu, it will parse the functions and enable displaying
# the options based on the IFunctions found.
menu = Menu(loader.functions)
menu.add_function = LogDecorator(menu.add_function)
menu.get_action = LogDecorator(menu.get_action)
menu.seed_functions()

while True:
    try:
        command = input("Enter command: > ")

        if command.lower() == "?" or command.lower() == "help":
            menu.print_menu()
        else:
            menu_action = menu.get_action(command)
            """
                Available fields
                menu_action.menu_item.command - Selected command
                menu_action.menu_item.ifunction - Full IFunction impl
                menu_action.menu_item.action - Pthon Function or None if not found
                menu_action.execution_command - Full command input
                menu_action.arguments - Arguments passed
            """

            if not menu_action.menu_item.action:
                # If we don't have an action, actual function to call, throw
                raise Exception("Unexpected command")
            else:

                # Build up the input object to pass to the function
                fn_input = FunctionInput()
                fn_input.command = menu_action.execution_command

                argument_exception = False
                try:
                    # This will throw if an unrecognized arg is passed or
                    # required args are missing.
                    fn_input.arguments = menu_action.menu_item.ifunction.parse_arguments(menu_action.arguments)
                except Exception as ex:
                    argument_exception = True
                    print(str(ex))
                    menu_action.menu_item.ifunction.default_help(menu_action.execution_command)

                # If you get here, then we have what we need, call the function
                if not argument_exception:
                    if IFunction.FN_CONFIGURATION in fn_input.arguments.keys():
                        if configuration_util:
                            config_names = fn_input.arguments[IFunction.FN_CONFIGURATION]
                            if config_names:
                                config_names.replace(' ', '')
                                config_names = config_names.split(',')
                                for conf in config_names:
                                    fn_input.configuration[conf] = configuration_util.read_configuration_value(conf)

                    value = menu_action.menu_item.action(fn_input)
                    if value:
                        print(value)

    except Exception as ex:
        print(str(ex))
        input("Press enter to see options.....")
        menu.print_menu()

