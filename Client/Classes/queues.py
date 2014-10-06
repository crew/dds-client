import Queue
from message import Message

class queues:
	"""docstring for Queues"""
	def __init__(self):
		self.Queues = {}

	def __getitem__(self, name):
		return self.Queues[name]

	def addQueue(self,name):
		self.Queues[name] = Queue.Queue(100)