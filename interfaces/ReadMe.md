# IFunction base class

To add functionality to the application an implementor has to create additional classes that dervive from the [IFunction](./funciton.py) class and place it in the directory functions/user.

By doing so, the application will detect the new IFunction implementation and it will be picked up and added to the running program. 

## Key Points
This design makes it as easy as possible for you to create additional command line options for the program with a minimal amount of work. 

Your real work should focus on what you are trying to implement instead of worrying about the plumbing of presenting and parsing user input.

1. Derive your class from IFunction
```python
from interfaces import IFunction, ArgumentDescriptor
class FirstFunction(IFunction):
    ....
```
2. In the class constructor (__init__(self)) you must provide the following:
    1. Seed the base class with a name
    ```python
    # Base class expectes name in constructor
    super().__init__("FirstFunction")
    ```
    2. Build your programs menu. This is what will available to the user to run. The menu options are defined as a dictionary.<br><br>For example, if you want to expose the action 'get balance' to your program and tie it to your IFunction class implentations call get_balance, the menu would look like this:
    ```python
    # Define your function menu options
    self.menu_options = {
        "get": {
            "balance": self.get_balance
        }
    }
    ```
    3. Define the arguments that your operation uses or requires. For our example the account (-a) is required and the address (-add) is optional.
    ```python
    # Define your funciton arguments here
    self.arguments = {
        '-a': ArgumentDescriptor(True, "Account ID"),
        '-add': ArgumentDescripto(False, "Associated Address)
    }
    ```
    4. Opitonally give your functionality default optional arguments for help (?) and configuration (-c)
    ```python
        # Default hook the help command, don't need to do this yourself
        self.set_default_hooks()
    ```

## Bound Functions
Bound functions are those that are pointed to in your menu definition. 

These functions MUST support a single argument (aside from self) -> *args:
```python
def my_bound_func(self, *args):
```

The way the code is called from the main application loop is to bundle up an instance of [FunctionInput](./functioninput.py) and pass it to the bound function. 

This will appear as a tuple to the function and the base class can unpack that for you:
```python
def _alter_text(self, *args):
    # Instance of FunctionInput - interfaces\function.py
    function_input = self.get_inputs(args)
```

The input will have all of the information you need, or have requested, from the user. 

## Configuration
By default a configuration function is added into your program for you. This allows your app to write to and read from a configuration (JSON) file. You can save values or full on JSON objects through the 'config' commands. 

A default argument (-c) can be used for configuraiton on your application by hooking that default argument. 

If the -c is present, the input for that argument is a comma separated list of names of configuration settings to pass into your function. 

These appear in the [FunctionInput](./functioninput.py) object under configuration as a dictionary. 