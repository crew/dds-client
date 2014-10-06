from Classes.threads import threads

from display import main_display_thread
from socketClient import main_socket_thread

def plugin(Threads, Queues):
#	Threads.addThread("Logging", "logging_thread", Queues)
	Threads.addThread("Display", main_display_thread, Queues)
	Threads.addThread("Socket", main_socket_thread, Queues)
