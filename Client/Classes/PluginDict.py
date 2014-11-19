class PluginDict:

	def __init__(self):
		self.plugins = {};

	def addPlugin(self, title,  p):
		self.plugins[title] = p
