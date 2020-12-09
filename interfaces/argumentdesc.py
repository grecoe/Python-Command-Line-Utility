class ArgumentDescriptor:
    """
    Used by the IFunction instance to declare it's arguments.

    IFunction arguments are a dictionary of
    key = text argument, i.e. -s
    value = ArgumentDescriptor
    """
    def __init__(self, required, description):
        """
        Two fields on this object are
        required - Is the argument required
        description - Text to show user to explain what the argument means
        """
        self.required = required
        self.description = description