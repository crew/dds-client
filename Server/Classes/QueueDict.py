import Queue
from message import Message

class QueueDict:
    """
    A wrapper around the Queue Object. 
    Simply a dict of Queues that can be passed into a plugin 
    allowing all plugins to compunicate with other plugins

    A String to Queue dictionary
    
    :var _queues : Dictionary. Dictionary of queues
    :var _queueSize : Integer. Queue size in _queues

    """

    def __init__(self, queueSize = 100):
        self._queues = {}
        self._queueSize = queueSize
    
    # Allows us to retrvive Queues using queues[name]
    def __getitem__(self, name):
        return self.getQueue(name)

    """
    :param <name> : String. Markup name of a queue.
    """
    def getQueue(self, name):
        return self._queues[name]

    # Adds a Queue to the dict.
    def addQueue(self, name):
        self._queues[name] = Queue.Queue(queueSize)
