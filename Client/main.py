#!/usr/bin/python
import sys
import Queue
import thread
import curses

from message import Message
from logging import logging_thread
#
def main(debug=False):
	#Setup general vars
	Run = True
	x = 0
	y = 0 
	
	#Setup individual Queues
	mainQueue = Queue.Queue(100)

	childrenQueues = {}
#	childrenQueues["Keyboard"] =  Queue.Queue(100)
#	childrenQueues["Display"] =  Queue.Queue(100)
	childrenQueues["Logging"] =  Queue.Queue(100)
#	childrenQueues["NFC"] =  Queue.Queue(100)

	#Function mapping
	functions = {}
	functions["Terminate"] = terminate


	#Order of Queues passed to functions: Queue passing data into function, Queue passing data from function to Main, Queue for logging function
	#thread.start_new_thread(keyboard_thread,(childrenQueues["Keyboard"],  mainQueue, childrenQueues["Logging"]))
	thread.start_new_thread(logging_thread,(childrenQueues["Logging"],))

	## Forwards messages to apropriate Queues/ runs appropriate functions
	while Run:
		log(childrenQueues["Logging"], "Empty Log")
		while not mainQueue.empty():
			log(childrenQueues["Logging"], "Entries in Log")
			currentMessage = mainQueue.get()
			if "Terminate" in currentMessage.content:
				log(childrenQueues["Logging"], "Terminating")
				Run = False
				break;
			else:
				functions[currentMessage.message]


## Logging Queue
def log(queue,mes):
	newLog = Message("Main", "Logging", {})
	newLog.add_content("1",mes)
	queue.put(newLog)

##Functions called:
def terminate():
	print "Terminating"
	## Add Terminate Handleing


##Allow for command line args: At the moment only can handle one (DEBUG). Order specific
if __name__ == "__main__":
	if len(sys.argv)>1:
		main(sys.argv[1])
	else:
		main()
