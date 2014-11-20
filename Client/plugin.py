#In the future we should house these in a file of there own
#We can dynamically load plugins from the directory
#we wouldn't need to import and add everything by hand.
from slideShow import SlideShowPlugin
from socketClient import IPlugin, OPlugin
from gtkDisplay import GTKPlugin


def class Plugin:
	def needsThread(self):
		return False;
	def run(self, runtimeVars):
		pass
	def setup(self, messageDict, runtimeVars):
		pass
	def getName(self):
		raise Exception("Abstract Plugin does not have a name")
	def addMessage(self, message):
		raise Exception("Not implemented for Plugin")
	
	
#TODO load dynamically

def getPlugins():
	return [SlideShowPlugin(), IPlugin(), OPlugin()]
