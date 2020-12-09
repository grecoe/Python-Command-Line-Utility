class FunctionInput:
    """
    The FunctionInput class is used as a single argument passed into any 
    bound function to be called via a MenuItem.

    The IFunction impementation MUST take a *args parameter along with the self
    parameter. 

    The FunctionInput contains all of hte information that will be required for 
    the bound function to execute.  
    """
    def __init__(self):
        """
        The class has three members

        command:
            The string command that triggered the call
        arguments:
            Dictionary with 
                key = The argument (as defined by the IFunction itself)
                value = The actual argument parameters, for flags this is None
        configuration:
            If the user chose the -c opiton, this dictionary will have settings
            from the application configuration (ConfigFn) in a dictionary where
                key = Configuration key name
                value = Configuration key value
        """
        self.command = None
        self.arguments = {}
        self.configuration = {}