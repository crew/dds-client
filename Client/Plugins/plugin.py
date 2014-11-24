


class Plugin:
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


