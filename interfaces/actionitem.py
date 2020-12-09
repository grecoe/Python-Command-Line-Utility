class ActionItem:
    """
    Class used by the base IFunction implementation to provide information on 
    functions that it's loaded. 

    Returned from the base IFunction through get_command_mapping as a list of 
    ActionItem instances.
    """
    def __init__(self, command, action):
        """
        Class has two members

        comand - The full text representation of the command to fire it off
        action - The bound method from the loaded IFunction implementation
        """
        self.command = command
        self.action = action