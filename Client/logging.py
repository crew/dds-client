from message import Message
import Queue
import syslog
# Takes a dict input and logs its contents to the syslog
def logging_thread(input_queue):
    while True:
        if not input_queue.empty():
            currentMessage = input_queue.get()
            for key in currentMessage.content:
	        msg = "PIE: " + currentMessage.src + ": " + currentMessage.content[key]
		syslog.syslog(syslog.LOG_ERR, msg)
