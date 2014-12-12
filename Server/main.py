#!/usr/bin/python
# General Imports
import Queue
import thread

# Import Classes
from Classes.message import Message
from Classes.QueueDict import QueueDict
from Classes.ThreadDict import ThreadDict
from Classes.ConfigParser import ConfigParser

# Import functions
from plugin import plugin
from logging import log

# Import children
from logging import logging_thread


def main():
    """
    Main server function (manages threads, queues, etc.)
    @return: None
    @rtype: NoneType
    @copyright: Northeastern University Crew 2014
    """
    # Will be generated from config files
    runtimeVars = ConfigParser.readConfig()

    # Set up individual queues
    Queues = QueueDict()
    Threads = ThreadDict()
    plugin(Threads, Queues)
    Queues.Queues["Logging"] = Queue.Queue(100)
    Queues.Queues["Main"] = Queue.Queue(100)

    # Order of Queues passed to functions:
    # Queue passing data into function,
    #   Queue passing data from function to Main,
    #   Queue for logging function
    thread.start_new_thread(logging_thread, (Queues.Queues["Logging"], runtimeVars))
    for Thread in Threads.Threads:
        log(Queues.Queues["Logging"], "Starting thread" + Thread)
        thread.start_new_thread(Threads.Threads[Thread], (Queues.Queues[Thread], Queues, runtimeVars))

    Run = True
    # Forwards messages to appropriate queues and runs appropriate functions
    while Run:
        log(Queues.Queues["Logging"], "Empty Log")
        while not Queues.Queues["Main"].empty():
            log(Queues.Queues["Logging"], "Entries in Log")
            currentMessage = Queues.Queues["Main"].get()
            if "Terminate" in currentMessage.content:
                log(Queues.Queues["Logging"], "Terminating")
                # Terminate all children threads
                terminate(Queues.Queues)
                Run = False
                break


def terminate(queues):
    """
    Sends a terminate message to the threads
        listening to the given queues
    @param queues: The list of queues to terminate
    @type queues: Dictionary
    @return: None
    @rtype: NoneType
    @note: I added this 'queues' parameter since, as it was written,
             Queues.Queues was out of scope for this function. I *believe*
             the way I added its call above replicates the desired
             behavior. If not, please fix. If so, please remove this
             message. -<Philip (11 Dec 2014)>
    """
    terminateMes = Message("Main", "All", "All", "Terminate", {})
    terminateMes.add_content("Terminate", True)
    for queue in queues:
        queue.put(terminateMes)

# TODO: Replace with argparse library
if __name__ == "__main__":
    main()
