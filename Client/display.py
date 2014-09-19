import Queue
import thread
from message import Message

def main_display_thread(input_queue, output_queue, logging_queue):

    # logs for debugging purposes
    log(logging_queue,"display running")

    ## Setps up child thread queue and Spawn child thread
    displayQueue = Queue.Queue(100)
    thread.start_new_thread(imageLoop,(displayQueue,logging_queue,))

    ## loop var
    run = True

    ## Child sub threads manager
    while run:
        if not input_queue.empty():
            currentMessage = input_queue.get()
            ## Terminate functionality (when it recieves the die message terminates child threads and then terminates self)
            if "Terminate" in currentMessage.content and currentMessage.content["Terminate"] is True:
                sendMessage = Message("display", "displaychild", {})
                sendMessage.add_content("Terminate", True)
                output_queue.put(sendMessage)
                run = False
        ## Can add additional logic here/spawn threads as needed

## Functions
def imageLoop(output_queue, logging_queue):
    # Insert image timer/displayer here
    print "Place holder"

def updateBrowser(slide):
    # Insert Websocket code here
    print "Place holder"

## Logging
# Passes a message to the logging thread to log.
def log(queue,mes):
        newLog = Message("display", "Logging", {})
        newLog.add_content("1",mes)
        queue.put(newLog)


