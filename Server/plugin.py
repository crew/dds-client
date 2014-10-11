# Import thread module
from Classes.threads import Threads


# Import plugin thread
from socketServer import main_socket_thread

# Adds plugin thread to our threds object
def plugin(Threads, Queues):
	Threads.addThread("SocketServer", main_socket_thread, Queues)
