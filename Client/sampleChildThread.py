import Queue
import thread
from message import Message

def main_SAMPLE_thread(input_queue, output_queue, logging_queue):

    # logs for debugging purposes
    log(logging_queue,"SAMPLE running")

    ## Setps up child thread queue and Spawn child thread
    SAMPLEsubCHILDQueue = Queue.Queue(100)
    thread.start_new_thread(FUNC1,(SAMPLEsubCHILDQueue,logging_queue,))

    ## loop var
    run = True

    ## Child sub threads manager
    while run:
        if not input_queue.empty():
            currentMessage = input_queue.get()
            ## Terminate functionality (when it recieves the die message terminates child threads and then terminates self)
            if "Terminate" in currentMessage.content and currentMessage.content["Terminate"] is True:
                sendMessage = Message("SAMPLE", "SAMPLEchild", {})
                sendMessage.add_content("Terminate", True)
                output_queue.put(sendMessage)
                run = False
        ## Can add additional logic here/spawn threads as needed

## Functions
def FUNC1(output_queue, logging_queue):
    # Add functionality as needed
    print "Place Holder Text"

## Logging
# Passes a message to the logging thread to log.
def log(queue,mes):
        newLog = Message("SAMPLE", "Logging", {})
        newLog.add_content("1",mes)
        queue.put(newLog)


