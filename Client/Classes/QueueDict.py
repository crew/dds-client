import Queue
from message import Message

class QueueDict:
    """
    A String to Queue dictionary
    
    :var _queues : Dictionary. Dictionary of queues
    :var _queueSize : Integer. Queue size in _queues

    """

    def __init__(self, queueSize = 100):
        self._queues = {}
        self._queueSize = queueSize
    

    """
    :param <name> : String. Markup name of a queue.
    """
    def getQueue(self, name):
        return self._queues[name]

    def __getitem__(self, name):
        return self.getQueue(name)

    def addQueue(self, name):
		self._queues[name] = Queue.Queue(queueSize)
