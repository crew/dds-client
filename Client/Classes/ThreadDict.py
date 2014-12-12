class ThreadDict:
    """
    Wrapper around thread object, allows us to
    start all the persistent Threads in a consistent
    and simple fashion. See plugins.py for more details.

    @ivar Threads: The threads contained in the object.
    @type Threads: Dictionary
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self):
        """
        ThreadDict Constructor
        @return: An empty ThreadDict
        @rtype: ThreadDict
        """
        self.Threads = {}

    def addThread(self, name, function, queueDict):
        """
        Adds a thread with the given parameters to the ThreadDict
        @param name: The name of the thread
        @type name: String
        @param function: The function associated with the thread to add
        @type function: Function
        @param queueDict: The QueueDict to add the thread's message queue to
        @type queueDict: QueueDict
        @return: None
        @rtype: NoneType
        """
        queueDict.addQueue(name)
        self.Threads[name] = function