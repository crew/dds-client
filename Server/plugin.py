# Import the threads for the plugins
from socketServer import main_socketServer_thread
from WPHandler import main_WPHandler_thread


# TODO: (See docstring)
def plugin(Threads, Queues):
    """
    Adds plugin threads to the given ThreadDict and
        adds their message Queues to the given QueueDict
    @param Threads: The ThreadDict to contain the plugins' threads
    @type Threads: ThreadDict
    @param Queues: The QueueDict to contain the plugins' message queues
    @type Queues: QueueDict
    @return: None
    @rtype: NoneType
    @todo: Abstract this out so that the plugin names aren't hardcoded
        (At least on the Server end. We'll see what the Pis can handle)
    @copyright: Northeastern University Crew 2014
    """
    Threads.addThread("socketServer", main_socketServer_thread, Queues)
    Threads.addThread("WPHandler", main_WPHandler_thread, Queues)
