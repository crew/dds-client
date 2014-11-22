#!/usr/bin/python
# General Imports
import sys, Queue, thread, os
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
from slideShow import SlideShowPlugin
import socketClient
from gtkDisplay import GTKPlugin

#TODO dynamically create
def getPlugins():
	return [SlideShowPlugin(), socketClient.IPlugin(), socketClient.OPlugin()]
	

def main():
	runtimeVars = ConfigParser.readConfig()
	runtimeVars["socket"] = sockClass(runtimeVars)
		

	
	
	plugins = getPlugins()
	#reduce == foldl, just mapping each plugin to an entry in a dict, where the name of
	#the plugin is the key, and the value is that plugins addMessage function
	#also preserves safety of each plugin from the others
	#they only have access to the addMessage function, and nothing else
	def addPluginToDict(dict, p):
		dict[p.getName()] = p.addMessage
		return dict
	messageDict = reduce(addPluginToDict, plugins, {})
	
	
	#Main thread now runs gtk.main() before it was busy waiting
	for plugin in plugins:
		Logger.log("DEBUG","Starting plugin: "+plugin.getName())
		plugin.setup(messageDict, runtimeVars)
		if plugin.needsThread():
			thread.start_new_thread(plugin.run, (runtimeVars,))
	#thread.start_new_thread(GTKPlugin().run, (runtimeVars,))
	#while True:
	#	sleep(10)
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
