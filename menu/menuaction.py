
class MenuAction:
    """
    Used by the Menu class to return information about the currently chosen
    option by the user.
    """
    def __init__(self):
        """
        Class has four members

        execution_command:
            The literal command that the user entered with arguments stripped off
        arguments:
            A dictionary of arguments where key=arg and value is whatever was provided.
        menu_item:
            An instance of MenuItem that will then maintain the bound function to execute.
        """
        self.execution_command = []
        self.arguments = None
        self.menu_item = None