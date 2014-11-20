import Queue, thread, json, datetime, time

from Classes.message import Message
from Classes.slide import Slide
from logging import log


from logging import Logger


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


		
class SlideShowPlugin(Plugin):
	def __init__(self):
		self.updateHandle = None
	def needsThread(self):
		return True;
	def startThread(self, inQ, queues, runtimeVars):
		if self.updateHandle == None:
			raise Exception("Something got fucked")
		runShow(inQ, queues, runtimeVars, self.updateHandle)
	def setup(self, inQ = None, queues = None, runtimeVars = None):
		if inQ is None or queues is None or runtimeVars is None:
			raise Exception("SlideShowPlugin setup recieved bad arguments")
		self.updateHandle = gtkDisplay.getUpdateHandle(inQ, queues, runtimeVars)
	def getName():
		return "slideShow"

## Functions
def runShow(inputQueue, Queues, runtimeVars, setPage):
    slideRequest = Message(runtimeVars["name"], "Grandma", 'WPHandler', "querySlides", "placeHolder")
    print "slideReuqest " + slideRequest.toJSON()
    Queues["Socket"].put(slideRequest)

    slides = []
    # Replace with loading slide
    slides.append(Slide("http://mrwgifs.com/wp-content/uploads/2013/08/Success-Kid-Meme-Gif.gif", 10)) 

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
        target_time = datetime.datetime.now() + datetime.timedelta(seconds = currentSlide.duration)
        setPage(currentSlide.url)
		#Holy shit this didn't do any waiting, thats A LOT of wasted
		#cpu time, in this loop
        while(datetime.datetime.now() < target_time):
            if not inputQueue.empty():
                currentMessage = inputQueue.get()
                if currentMessage["action"] == "loadSlides":
					Logger.log("DEBUG", "Recieved new slide: "+currentMessage["content"])
                    tempSlides = json.loads(currentMessage["content"])
                    for slide in tempSlides["actions"]:
                        slides.append(Slide(slide["location"], slide["duration"]))
                elif currentMessage["content"] == "removeSlide":
                    slides.remove(currentMessage.content)
                elif currentMessage["content"] == "Terminate":
                    Run = False
					#this inner loop will still run even if we set Run = false, we need to break
					#in order to terminate immediately
					break
			#Should sleep, we need only support slide durations with precision .1 seconds (we could lesson this to 1 second
            sleep(.1)
        # Move on
        x %= len(slides)




