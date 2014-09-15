#!/usr/bin/python
# General Imports
import sys
import Queue
import thread

# Import Classes
from message import Message

# Import childern
from logging import logging_thread
from display import display_thread
from socketListener import socket_thread

def main(debug=False):
	#Setup individual Queues
	mainQueue = Queue.Queue(100)

	childrenQueues = {}
	childrenQueues["Logging"] = Queue.Queue(100)
	childrenQueues["Display"] = Queue.Queue(100)
	childrenQueues["Socket"]  = Queue.Queue(100)

	#Function mapping
	functions = {}
	functions["Terminate"] = terminate


	#Order of Queues passed to functions: Queue passing data into function, Queue passing data from function to Main, Queue for logging function
	thread.start_new_thread(logging_thread,(childrenQueues["Logging"]))
	thread.start_new_thread(display_thread,(childrenQueues["Display"], mainQueue, childrenQueues["Logging"]))
	thread.start_new_thread(socket_thread, (childrenQueues["Socket"], mainQueue, childrenQueues["Logging"]))

	Run = True
	## Forwards messages to apropriate Queues/ runs appropriate functions
	while Run:
		log(childrenQueues["Logging"], "Empty Log")
		while not mainQueue.empty():
			log(childrenQueues["Logging"], "Entries in Log")
			currentMessage = mainQueue.get()
			if "Terminate" in currentMessage.content:
				log(childrenQueues["Logging"], "Terminating")
				terminate()
				Run = False
				break;
			else:
				functions[currentMessage.action]()


## Logging
# Passes a message to the logging thread to log.
def log(queue,mes):
	newLog = Message("Main", "Logging", "log", {})
	newLog.add_content("1",mes)
	queue.put(newLog)

## Functions called:
# When function is called, passes a terminate message to all the children threads.
def terminate():
	terminateMes = Message("Main", "All", "Terminate",{})
	terminateMes.add_content("Terminate",True)
	for queue in childernQueues:
	    queue.put(terminateMes)


# Allow for command line args: At the moment only can handle one (DEBUG). Order specific
# To be replaced with argparse library
if __name__ == "__main__":
	if len(sys.argv)>1:
		main(sys.argv[1])
	else:
		main()
