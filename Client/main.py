#!/usr/bin/python
# General Imports
import thread

from Classes.ConfigParser import ConfigParser

# Import functions

# In the future we should house these in a file of there own
# We can dynamically load plugins from the directory
# we wouldn't need to import and add everything by hand.
from Plugins.plugin import Plugin
from slideShow import SlideShowPlugin
from socketClient import IOPlugin
from gtkDisplay import GTKPlugin


def getAdditionalPlugins(runtimeVars):
    """
    Gets any User-Defined Plugins specified in the Configuration
        from ./Plugins
    @param runtimeVars: User-Defined Configuration
    @type runtimeVars: Dictionary
    @return: User-Define Plugins
    @rtype: Array
    """
    plugins = []
    for plugin in runtimeVars["plugins"]:
        try:
            exec "from Plugins." + plugin + " import " + plugin
            instance = eval(plugin + "()")
            if isinstance(instance, Plugin):
                print instance
                plugins.append(instance)
            else:
                print "Huh? what did i get? : " + str(instance)
        except Exception, e:
            print "Couldn't create an instance of a plugin in the config"
            print str(e)
    return plugins


def main():
    """
    The main function of the client
    @return: None
    @rtype: None
    """
    runtimeVars = ConfigParser.readConfig()
    plugins = [SlideShowPlugin(), IOPlugin()] + getAdditionalPlugins(runtimeVars)
    runtimeVars["plugins"] += ["SlideShowPlugin", "IOPlugin"]

    def addPluginToDict(dict, p):
        dict[p.getName()] = p.addMessage
        return dict

    # messageDict = Message-handling functions for each plugin
    messageDict = reduce(addPluginToDict, plugins, {})

    for plugin in plugins:
        plugin.setup(messageDict, runtimeVars)
    for plugin in plugins:
        print "Starting " + plugin.getName()
        if plugin.needsThread():
            thread.start_new_thread(plugin.run, (runtimeVars,))
    # Instead of having main() be in a busy wait doing nothing,
    # we denote GTKPlugin() to be the "main" plugin, so its
    # behavior drives any looping done on the main thread
    GTKPlugin().run(runtimeVars)


# TODO: Replace with argparse library
if __name__ == "__main__":
    main()

