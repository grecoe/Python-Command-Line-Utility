from logutils.tracer import LogDecorator


class MenuItem:
    def __init__(self):
        self.command = None
        self.ifunction = None
        self.action = None
        self.children = []


class MenuAction:
    def __init__(self):
        self.execution_command = []
        self.arguments = None
        self.menu_item = None


class Menu:
    def __init__(self, ifunction_list):
        """
        Initialize the menu from a function list
        """
        self.function_list = ifunction_list
        self.menu_options = {}

    def seed_functions(self):
        for ifn in self.function_list:
            self.add_function(ifn)

    def add_function(self, ifunction):

        mapping = ifunction.get_command_mapping()
        for actionmap in mapping:
            command_parts = actionmap.command.split(" ")

            if command_parts[0] not in self.menu_options.keys():
                # This picks up defaults like quit
                menu_item = MenuItem()
                menu_item.ifunction = ifunction
                menu_item.command = command_parts[0]
                if len(command_parts) == 1:
                    menu_item.action = actionmap.action
                self.menu_options[command_parts[0]] = menu_item
            else:
                # This should get the loaded funcitons
                menu_item.action = LogDecorator(menu_item.action)

            active_item = self.menu_options[command_parts[0]]
            part_indexes = range(1, len(command_parts))

            for part in part_indexes:
                menu_item = MenuItem()
                menu_item.ifunction = ifunction
                menu_item.command = command_parts[part]
                if part == len(command_parts) - 1:
                    menu_item.action = actionmap.action

                child = [x for x in active_item.children if x.command == command_parts[part]]
                if not len(child):
                    active_item.children.append(menu_item)
                else:
                    child[0].children.append(menu_item)

                active_item = menu_item

    def print_menu(self):
        for key in self.menu_options.keys():
            self._dump_menuitem(self.menu_options[key], 0)

    def get_action(self, command):
        if not command:
            raise Exception("Must supply a command to execute.")

        return_action = MenuAction()

        commands = command.split(' ')

        if commands[0].lower() not in self.menu_options.keys():
            raise Exception("There is no command staring with > {}".format(command))

        current_menu_item = self.menu_options[commands[0]]
        return_action.execution_command.append(commands[0])
        cmd_indexes = range(1, len(commands))
        last_index = len(commands) - 1

        capture_last = False
        for cmd_index in cmd_indexes:
            last_index = cmd_index
            child = [x for x in current_menu_item.children if x.command == commands[cmd_index]]
            if not len(child):
                if cmd_index == len(commands) - 1:
                    capture_last = True
                break
            return_action.execution_command.append(commands[cmd_index])
            current_menu_item = child[0]

        # Gone as far as we can...
        arguments_list = None
        if last_index < len(commands) - 1:
            arguments_list = commands[last_index:]
        elif capture_last:
            arguments_list = [commands[-1]]

        return_action.menu_item = current_menu_item
        return_action.arguments = arguments_list

        return return_action

    def _dump_menuitem(self, menu_item, depth):
        print("{}{}".format('  ' * depth, menu_item.command))
        for child in menu_item.children:
            self._dump_menuitem(child, depth + 1)
