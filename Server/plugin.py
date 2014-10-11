# Import thread module
from Classes.ThreadDict import ThreadDict


# Import plugin thread
from socketServer import main_socketServer_thread
from WPHandler import main_WPHandler_thread

# Adds plugin thread to our threds object
def plugin(Threads, Queues):
	Threads.addThread("socketServer", main_socketServer_thread, Queues)
	Threads.addThread("WPHandler", main_WPHandler_thread, Queues)
