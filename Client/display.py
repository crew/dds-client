import Queue, thread, json, datetime

from Classes.message import Message
from Classes.slide import Slide

#from logging import log


# Proably not needed anymore
# def main_display_thread(inputQueue, Queues, runtimeVars):

#     # logs for debugging purposes
#     log(Queues.Queues["Logging"],"display running")

#     ## Setps up child thread queue and Spawn child thread
#     displayQueue = Queue.Queue(100)
#     thread.start_new_thread(imageLoop,(displayQueue,))

#     ## loop var
#     Run = True

#     ## Child sub threads manager
#     while Run:
#         if not input_queue.empty():
#             currentMessage = input_queue.get()
#             ## Terminate functionality (when it recieves the die message terminates child threads and then terminates self)
#             if "Terminate" in currentMessage.content and currentMessage.content["Terminate"] is True:
#                 sendMessage = Message("display", "displaychild", {})
#                 sendMessage.add_content("Terminate", True)
#                 output_queue.put(sendMessage)
#                 run = False
#         ## Can add additional logic here/spawn threads as needed

## Functions
def main_display_thread(inputQueue, Queues, runtimeVars):
    slides = []
    # Replace with loading slide
    slides.append(Slide("http://facebook.com", 10)) 

    # all of the information to be sent to be displayed
    #Loops through the Json and outputs the data
    #Once it reaches the end of the data it resets
    #If "a" key is pressed, then it adds the next slide in the queue to the JSON
    #if "r" key is pressed, puts fram back into queue, then it removes the last slide in the JSON
    #prints "at last frame!" if you press r to the last frame
    x = 0
    Run = True
    while Run:
        currentSlide = slides[x]
        print currentSlide.duration
        target_time = datetime.datetime.now() + datetime.timedelta(seconds = currentSlide.duration)
        Queues["Gtk"].put(currentSlide)
        while(datetime.datetime.now() < target_time):
            pass
            if not inputQueue.empty():
                currentMessage = inputQueue.get()
                if currentMessage.action == "addSlide":
                    print "New Slide!!!!"
                    print currentMessage.content
                    tempSlide = json.loads(currentMessage.content)
                    if  '__type__' in tempSlide and tempSlide["__type__"] == "slide":
                        slides.append(Slide(tempSlide["url"], tempSlide["duration"], tempSlide["action"]))
                elif currentMessage.action == "removeSlide":
                    slides.remove(currentMessage.content)
                elif currentMessage.action == "Terminate":
                    Run = False
            else:
                pass
        # Load Slide
        if x < (len(slides) - 1):
            x+=1
        else:            
            x=0

def updateBrowser(slide):
    # Insert Websocket code here
    print "Place holder"

## Logging
# Passes a message to the logging thread to log.
def log(queue,mes):
        newLog = Message("Display", "Logging", "Logger", "log", {})
        newLog.add_content("1",mes)
        queue.put(newLog)


