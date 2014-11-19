# Import thread module
from Classes.ThreadDict import ThreadDict
import os

# Import plugin thread
from slideShow import main_display_thread
from socketClient import main_socket_thread
from gtkDisplay import main_gtk_thread


def class Plugin:
	def needsThread(self):
		return False;
	def startThread(self, inQ, queues, runtimeVars):
		pass
	def setup(self, inQ = None, queues = None, runtimeVars = None):
		pass
		
	def getName():
		raise Exception("Abstract Plugin does not have a name")
	

def getPlugins():
	return [SlideShowPlugin(queues), IOPlugin(queues), GTKPlugin(queues)]
