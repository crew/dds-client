import Queue


class QueueDict:
    """
    A wrapper around the Queue Object, which is
    simply a dictionary of Queues that can be
    passed into a plugin, thereby allowing all
    plugins to communicate with other plugins.
    (i.e. A String to Queue dictionary)
    @ivar Queues: Dictionary of queues
    @type Queues: Dictionary
    @ivar queueSize : Queue size in _Queues
    @type queueSize: Integer
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self, queueSize=100):
        """
        Queue Dictionary Constructor
        @param queueSize: (Optional) Specifies size of contained queues (Default 100)
        @return: The Constructed Queue Dictionary
        @rtype: QueueDict
        """
        self.Queues = {}
        self.queueSize = queueSize

    def __getitem__(self, name):
        """
        Retrieves the desired queue using dictionary syntax
        (e.g. C{queues[name]})
        @param name: The name of the desired queue
        @type name: String
        @return: The queue corresponding to the given name
        @rtype: Queue.Queue
        """
        return self.Queues[name]

    def addQueue(self, name):
        """
        Adds a queue with the given name to the QueueDict object.
        @param name: The name of the queue to add
        @type name: String
        @return: None
        @rtype: NoneType
        """
        self.Queues[name] = Queue.Queue(self.queueSize)