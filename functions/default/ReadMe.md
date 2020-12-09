# Default Functions

This folder contains two default funcitons that are added to the main program menu.

1. QuitFn
    - Quits the program
2. ConfigFn
    - Enables the user to create configuration settings and acces them via
        - get, set, list
    - Through a default parameter that is added to each user funciton (-c) end user functions can have access to those configuration settings through the FunctionInput object that is passed as a parameter to every function.      