from queues import queues

class threads:
	"""docstring for """
	def __init__(self):
		self.Threads = {}

	def addThread(self, name, function, queue):
		queue.addQueue(name)
		self.Threads[name] = function
		#self.Threads[thread]["Queue"] = queue
		