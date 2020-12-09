# Menu classes

The menu is an important part of the program. 

You provide the Menu class with instances of IFunction in which to build up the menu selection to be shown to the user. 

Internally, the Menu class keeps track of all loaded IFunction instances, default or user provided, and can be used to:

1. Show the menu options to the user
2. When provided with a command line input from the user, attempt to map that input to a valid IFunction instance to execute on the users behalf. 

### Relevant Topics
[IFunction](../interfaces/ReadMe.md)