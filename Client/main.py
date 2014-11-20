#!/usr/bin/python
# General Imports
import sys, Queue, thread, os
from time import sleep

# Import Classes
from Classes.message import Message
from Classes.QueueDict import QueueDict
from Classes.ThreadDict import ThreadDict
from Classes.ConfigParser import ConfigParser

# Import functions
from plugin import getPlugins
from logging import Logger



def main():

	# Will be generated from config files
	runtimeVars = ConfigParser.readConfig()
	#runtimeVars["PIEname"] = "blueberry"
	#runtimeVars["Server"] = "dds-wp.ccs.neu.edu"
	#runtimeVars["serverPort"] = "5000"
		

	#Setup individual Queues
	Queues = QueueDict()
	#Threads = ThreadDict()
	
	plguins = getPlugins()
	Queues.Queues["Logging"] = Queue.Queue(100)
	Queues.Queues["Main"] = Queue.Queue(100)

	#Why does this need its own thread #overengineering
	#thread.start_new_thread(logging_thread,(Queues.Queues["Logging"], Queues, runtimeVars))
	for plugin in plugins:
		Logger.log("DEBUG","Starting plugin: "+plugin.getName())
		plugin.setup()
		if plugin.needsThread():
			thread.start_new_thread(plugin.startThread, (Queues.Queues[Thread], Queues, runtimeVars))

	Run = True
	## Keeps the program running until recieves a terminate command.
	#This is pointless we should run something in the main thread, instead of spawning new ones for everything.
	#in addition this is a busy wait loop, meaning that it still takes cpu time, which is something we don't want
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
