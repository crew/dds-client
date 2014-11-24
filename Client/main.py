#!/usr/bin/python
# General Imports
import sys, Queue, thread, os, types
from time import sleep

# Import Classes
from Classes.message import Message
from Classes.ConfigParser import ConfigParser


from Classes.sockClass import sockClass



# Import functions
from logging import Logger

#In the future we should house these in a file of there own
#We can dynamically load plugins from the directory
#we wouldn't need to import and add everything by hand.
from Plugins.plugin import Plugin
from slideShow import SlideShowPlugin
from socketClient import IOPlugin
from gtkDisplay import GTKPlugin
#Loads all the plugins in ./Plugins (that were placed in the config)
def getAdditionalPlugins(runtimeVars):
	plugins = []
	for plugin in runtimeVars["plugins"]:
		try:
			exec "from Plugins."+plugin+" import "+plugin
			instance = eval(plugin+"()")
			if isinstance(instance, Plugin):
				print instance
				plugins.append(instance)
			else:
				print "Huh? what did i get? : "+str(instance)
		except Exception, e:
			print "Couldn't create an instance of a plugin in the config"
			print str(e)
	return plugins

def main():
	runtimeVars = ConfigParser.readConfig()
	plugins = [IOPlugin(), SlideShowPlugin()] + getAdditionalPlugins(runtimeVars)
	
	def addPluginToDict(dict, p):
		dict[p.getName()] = p.addMessage
		return dict
	messageDict = reduce(addPluginToDict, plugins, {})
	print "All Plugins : "+str(plugins)
	#Main thread now runs gtk.main() before it was busy waiting
	for plugin in plugins:
		print "Starting "+plugin.getName()
		Logger.log("DEBUG","Starting plugin: "+plugin.getName())
		plugin.setup(messageDict, runtimeVars)
		if plugin.needsThread():
			thread.start_new_thread(plugin.run, (runtimeVars,))
	GTKPlugin().run(runtimeVars) #This is kinda gross, need to clean

	

## Functions called:
# When function is called, passes a terminate message to all the children threads.
def terminate():
	terminateMes = Message("Main", "All", "All", "Terminate",{})
	terminateMes.add_content("Terminate",True)
	for queue in Queues.Queues:
		queue.put(terminateMes, True)

# Allow for command line args: At the moment only can handle one (DEBUG). Order specific
# To be replaced with argparse library
if __name__ == "__main__":
		main()
		
		
		
#Old main thread
'''
	while Run:
		Logger.log("DEBUG", "Empty Log")
		while not Queues.Queues["Main"].empty():
			Logger.log("DEBUG", "Entries in Log")
			currentMessage = Queues.Queues["Main"].get()
			if "Terminate" in currentMessage.content:
				Logger.log("DEBUG", "Terminating")
				terminate()
				Run = False
				break;
			else:
				Logger.log("ERROR", "Runaway Message: " + message)
		sleep(10)
'''
