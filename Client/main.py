#!/usr/bin/python
# General Imports
import sys, Queue, thread, os
from time import sleep

# Import Classes
from Classes.message import Message
from Classes.ConfigParser import ConfigParser

# Import functions
from plugin import getPlugins
from logging import Logger



def main():
	runtimeVars = ConfigParser.readConfig()
	
		

	
	
	plugins = getPlugins()
	#reduce == foldl, just mapping each plugin to an entry in a dict, where the name of
	#the plugin is the key, and the value is that plugins addMessage function
	#also preserves safety of each plugin from the others
	#they only have access to the addMessage function, and nothing else
	messageDict = reduce(lambda dict,p : dict[p.getName] = p.addMessage, plugins, {})
	
	
	#Main thread now runs gtk.main() before it was busy waiting
	for plugin in plugins:
		Logger.log("DEBUG","Starting plugin: "+plugin.getName())
		plugin.setup(messageDict, runtimeVars)
		if plugin.needsThread():
			thread.start_new_thread(plugin.startThread, (runtimeVars))
	GTKPlugin().run(runtimeVars) #This is kinda gross, need to clean
	

## Functions called:
# When function is called, passes a terminate message to all the children threads.
def terminate():
	terminateMes = Message("Main", "All", "All", "Terminate",{})
	terminateMes.add_content("Terminate",True)
	for queue in Queues.Queues:
	    queue.put(terminateMes)

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
