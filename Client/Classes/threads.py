from QueueDict import QueueDict

class threads:
	"""docstring for """
	def __init__(self):
		self.Threads = {}

	def addThread(self, name, function, queue):
		queueDict.addQueue(name)
		self.Threads[name] = function
		#self.Threads[thread]["Queue"] = queue
		
