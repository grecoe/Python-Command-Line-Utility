# Python Command Line Tool builder

This program is a dynamic command line tool that is quite easy to expand on functionality. 

As an implementor you create new classes and put them in the /functions/user directory. These will derived from a known base class called IFunction, see [here](./interfaces/ReadMe.md) for details on how to proceed. 

The app is menu driven and built off of the IFunction instances that the application finds. Details on the Menu can be found [here](./menu/ReadMe.md). 

As it is, you can run the application as is to see how it works. Simply run from this directory:

```
python app.py 
```

And you will start the application loop. You can find help by using the help or ? command on the command prompt:

```
Enter command: > help 
get
  lower
put
  unlimited
    power
config
  get
  set
  list
quit
```

To execute an action, put all parts in 
```
Enter command: > get lower -t THIS IS NOT LOWER
this is not lower
Enter command: > 
```

To get help, type out the action and use ? as an argument
```
Enter command: > get lower ?
Function Help
CMD  >  get lower
ARGS > :
        -t    : Required : Text to alter
        -c    : Optional : Comma separated list of configuration names
        ?     : Optional : Show help
Enter command: >
```

Give it a try! Not sure exactly how I wanted to use this, but was interested in just making something work. 

Dan