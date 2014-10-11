from QueueDict import QueueDict

class ThreadDict:
	"""Warpper around thread object, allows us to start all the persistant
	Threads in a consistent simple fashion. See plugins.py for more details."""

	def __init__(self):
		self.Threads = {}

	def addThread(self, name, function, queue):
		queue.addQueue(name)
		self.Threads[name] = function
		#self.Threads[thread]["Queue"] = queue
		
