class MenuItem:
    """
    Class used by the Menu class to track commands and the correlated 
    bound function behind it. 
    """
    def __init__(self):
        """
        Class has four members

        command - String that is the actual command. Each stage of a command is it's own
                  menu item. So for 'get config' three are two MenuItem instances. One 
                  for 'get' and the other for 'config'
        ifunction - Reference to the underlying IFunction implementation
        action - Bound function to something in the IFunction implementation that will 
                 actually execute the command. If not present, it's a parent action like 'get'
        children - Child instances of MenuItem. For the 'get config', 'get' will have one child
                   which is 'config'.                  
        """
        self.command = None
        self.ifunction = None
        self.action = None
        self.children = []
