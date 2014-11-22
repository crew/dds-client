import Queue, thread, json, datetime, time

from Classes.message import Message
from Classes.slide import Slide


from logging import Logger
from plugin import Plugin
import gtkDisplay


		
class SlideShowPlugin(Plugin):
	def __init__(self):
		self.updateHandle = None
		self.inQ = Queue.Queue(100)
		self.outHandle = None
	def needsThread(self):
		return True;
	def run(self, runtimeVars):
		if self.updateHandle == None or self.outHandle == None:
			raise Exception("Something went wrong...")
		runShow(self.inQ, runtimeVars, self.updateHandle, self.outHandle)
	def setup(self, messageDict, runtimeVars):
		self.updateHandle = gtkDisplay.getUpdateHandle(runtimeVars)
		self.outHandle = messageDict["OPlugin"]
	def getName(self):
		return "slideShow"
	def addMessage(self, message):
		print "Adding : "+str(message)
		self.inQ.put(message,True)
	
	

## Functions
def runShow(inputQueue, runtimeVars, setPage, writeOut):
	slideRequest = Message(runtimeVars["name"], "Grandma", 'WPHandler', "querySlides", "placeHolder")
	print "slideReuqest " + slideRequest.toJSON()
	writeOut(slideRequest)

	slides = []
	# Replace with loading slide
	slides.append(Slide("http://mrwgifs.com/wp-content/uploads/2013/08/Success-Kid-Meme-Gif.gif", 5)) 
	
	x = 0
	Run = True
	while Run:
		#todo print slides, why are they not in the list
		print str(slides)
		currentSlide = slides[x]
		target_time = datetime.datetime.now() + datetime.timedelta(seconds = currentSlide.duration * 5)
		setPage(currentSlide.url)
		print "Just set page : "+currentSlide.url
		while(datetime.datetime.now() < target_time):
			if not inputQueue.empty():
				print "The show got a message"
				currentMessage = inputQueue.get()
				if currentMessage["action"] == "loadSlides":
					print "Loading slides: "+currentMessage["content"]
					Logger.log("DEBUG", "Recieved new slide: "+currentMessage["content"])
					tempSlides = json.loads(currentMessage["content"])
					for slide in tempSlides["actions"]:
						if "weather" not in slide["location"]:
							slides.append(Slide(slide["location"], slide["duration"]))
				elif currentMessage["content"] == "removeSlide":
					slides.remove(currentMessage.content)
				elif currentMessage["content"] == "Terminate":
					Run = False
					#this inner loop will still run even if we set Run = false, we need to break
					#in order to terminate immediately
					break
			#Should sleep, we need only support slide durations with precision .1 seconds (we could lesson this to 1 second
			time.sleep(.1)
		# Move on

		x  = (x+1) % len(slides)




