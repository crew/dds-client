#In the future we should house these in a file of there own
#We can dynamically load plugins from the directory
#we wouldn't need to import and add everything by hand.
from slideShow import SlideShowPlugin
from socketClient import IOPlugin
from gtkDisplay import GTKPlugin


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
