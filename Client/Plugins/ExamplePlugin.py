"""
This is an example of a plugin that the user could add themselves.
There are several rules to create a plugin and have it run, in order to ensure
programmatic safety as well as usability. they are as follows:
    1. The file for the plugin must be placed in the Plugins directory
    2. The file must only define one class, nothing more, nothing less
    3. The class must have the EXACT same name as the file its in
    4. the class must extend Plugin
    5. add the class to the config file in the plugins field. The syntax for this field
    is identical to the python list syntax
    6. The plugin must implement the method getName which returns a string. No other implementations are necessary.
@note: your plugin will raise an exception if another plugin tries to pass it a message and the C{addMessage} method is
not implemented
"""
from plugin import Plugin


class ExamplePlugin(Plugin):
    def getName(self):
        return "ExamplePlugin"