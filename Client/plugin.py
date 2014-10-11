# Import thread module
from Classes.ThreadDict import ThreadDict


# Import plugin thread
from slideShow import main_display_thread
from socketClient import main_socket_thread
from gtkDisplay import main_gtk_thread

# Adds plugin thread to our threds object
def plugin(Threads, Queues):
	Threads.addThread("slideShow", main_display_thread, Queues)
	Threads.addThread("Socket", main_socket_thread, Queues)
	Threads.addThread("Gtk", main_gtk_thread, Queues)
