from QueueDict import QueueDict

class ThreadDict:
    """
    String to Thread dictionary.
    
    :var _threads: Dictionary.

    """
    def __init__(self):
        self._threads = {}

    def addThread(self, name, function, queueDict):
        queueDict.addQueue(name)
        self._threads[name] = function
        #self.Threads[thread]["Queue"] = queueDict
