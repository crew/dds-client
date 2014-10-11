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
        self.Queues = {}
        self.queueSize = queueSize
    
    # Allows us to retrvive Queues using queues[name]
    def __getitem__(self, name):
        return self.Queues[name]

    # Adds a Queue to the dict.
    def addQueue(self, name):
        self.Queues[name] = Queue.Queue(self.queueSize)