#!/usr/bin/python
# General Imports
import sys, Queue, thread

# Import Classes
from Classes.message import Message
from Classes.queues import queues
from Classes.threads import threads

# Import functions
from plugin import plugin
from logging import log

# Import childern
from logging import logging_thread
# from display import main_display_thread
# from socketClient import main_socket_thread


def main():

	# Will be generated from config files
	runtimeVars = {}
	runtimeVars["PIEname"] = "blueberry"
	runtimeVars["Server"] = "dds-wp.ccs.neu.edu"
	runtimeVars["serverPort"] = "5000"


	#Setup individual Queues
	Queues = queues()
	Threads = threads()
	plugin(Threads, Queues)
	Queues.Queues["Logging"] = Queue.Queue(100)
	Queues.Queues["Main"] = Queue.Queue(100)

	#Function mapping
	functions = {}
#	functions["Terminate"] = terminate

	#Order of Queues passed to functions: Queue passing data into function, Queue passing data from function to Main, Queue for logging function
	thread.start_new_thread(logging_thread,(Queues.Queues["Logging"], Queues, runtimeVars))
	#thread.start_new_thread(display_thread,(Queues, runtimeVars))
	#thread.start_new_thread(socket_thread, (Queues, runtimeVars))
	for Thread in Threads.Threads:
		log(Queues.Queues["Logging"],"Starting thread" + Thread)
		thread.start_new_thread(Threads.Threads[Thread], (Queues.Queues[Thread], Queues, runtimeVars))

	Run = True
	## Forwards messages to apropriate Queues/ runs appropriate functions
	while Run:
		log(Queues.Queues["Logging"], "Empty Log")
		while not Queues.Queues["Main"].empty():
			log(Queues.Queues["Logging"], "Entries in Log")
			currentMessage = Queues.Queues["Main"].get()
			if "Terminate" in currentMessage.content:
				log(Queues.Queues["Logging"], "Terminating")
				terminate()
				Run = False
				break;
			# else:
			# 	functions[currentMessage.action]()

## Functions called:
# When function is called, passes a terminate message to all the children threads.
def terminate():
	terminateMes = Message("Main", "All", "Terminate",{})
	terminateMes.add_content("Terminate",True)
	for queue in Queues.Queues:
	    queue.put(terminateMes)

# Allow for command line args: At the moment only can handle one (DEBUG). Order specific
# To be replaced with argparse library
if __name__ == "__main__":
		main()
