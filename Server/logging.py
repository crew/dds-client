from Classes.message import Message

import syslog


def logging_thread(input_queue, runtimeVars):
    """
    Logs the given Queue to the syslog
    @param input_queue: Queue from which to read
    @type input_queue: QueueDict
    @param runtimeVars: User-Defined Configuration File Contents
    @type runtimeVars: Dictionary
    @return: None
    @rtype: None
    @copyright: Northeastern University Crew 2014
    """
    while True:
        if not input_queue.empty():
            currentMessage = input_queue.get()
            for key in currentMessage.content:
                msg = "PIE: " + currentMessage.src + ": " + currentMessage.content[key]
                syslog.syslog(syslog.LOG_ERR, msg)


def log(queue, mes):
    """
    Logs the given message in the given log
    @param queue: Logging queue to pass message to
    @type queue: Queue.Queue
    @param mes: Message to pass
    @return: None
    @rtype: None
    """
    newLog = Message("Main", "Logging", "Logger", "log", {})
    newLog.add_content("1", mes)
    queue.put(newLog)