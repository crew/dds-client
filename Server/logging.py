from Classes.message import Message

import Queue, syslog

# Takes a dict input and logs its contents to the syslog
def logging_thread(input_queue, Queues, runtimeVars):
    while True:
        if not input_queue.empty():
            currentMessage = input_queue.get()
            for key in currentMessage.content:
	        msg = "PIE: " + currentMessage.src + ": " + currentMessage.content[key]
		syslog.syslog(syslog.LOG_ERR, msg)

## Logging
# Passes a message to the logging thread to log.
def log(queue,mes):
	newLog = Message("Main", "Logging", "log", {})
	newLog.add_content("1",mes)
	queue.put(newLog)