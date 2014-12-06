import Queue, thread, json, datetime, time

from Classes.message import Message
from Classes.slide import Slide


from logging import Logger
from Plugins.plugin import Plugin
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
		self.outHandle = messageDict["IOPlugin"]
	def getName(self):
		return "slideShow"
	def addMessage(self, message):
		print "Adding : "+str(message)
		self.inQ.put(message,True)
	
	

## Functions
def runShow(inputQueue, runtimeVars, setPage, writeOut):
	#TODO get DT 
	slideRequest = Message(runtimeVars["name"], "Grandma", 'WPHandler', "querySlides", "Maor slidez")
	print "slideReuqest " + slideRequest.toJSON()
	writeOut(slideRequest)

	slides = []
	# Replace with loading slide
	slides.append(Slide.makeSlide("http://mrwgifs.com/wp-content/uploads/2013/08/Success-Kid-Meme-Gif.gif", 5, -1, "")) 
	# Temp Weather slide for testing purposes. Uncomment as needed.
	#slides.append(Slide("http://104.131.73.58", 10))
	
	
	#Helper to get the slide out of the slide list with the given ID, also insures uniqueness if ID's
	def getSlideById(slideList, id):
		matches = filter(lambda x : x.sameID(currentMessage["ID"]), slides)
		if len(matches) > 1:
			raise Exception("Why are there 2 slides with the same ID?")
		return None if len(matches) == 0 else matches[0]
		
	def deleteSlide(slideList, id):
		print "Deleting slide..."
		temp = getSlideById(slides, id)
		Logger.log("DEBUG", "Removing slide: "+str(temp))
		if temp:
			slides.remove(temp)
		
	def editSlide(slideList, id, newSlide):
		print "Editing slide..."
		old = getSlideById(slides, id)
		Logger.log("DEBUG", "Changing slide :"+str(old)+" to "+ str(newSlide))
		if old:
			slideList.remove(old)
		slideList.add(new)
		
	def addSlide(slideList, slide):
		print "Adding slide..."
		Logger.log("DEBUG", "Adding slide :"+str(slide))
		slideList.append(slide)
	x = 0
	Run = True
	while Run:
		#todo print slides, why are they not in the list
		print str(slides)
		currentSlide = slides[x]
		target_time = datetime.datetime.now() + datetime.timedelta(seconds = currentSlide.duration)
		setPage(currentSlide.url)
		print "Just set page : "+currentSlide.url
		while(datetime.datetime.now() < target_time):
			if not inputQueue.empty():
				currentMessage = inputQueue.get()
				infoForAddition = json.loads(currentMessage["content"])
				if currentMessage["action"] == "load-slides":
					for slideJSON in infoForAddition["actions"]:
						#TODO fields in dds-api call need to be changed to standard, they also need ID and meta added @Eddie
						addSlide(slides, Slide.makeSlide(slideJSON["location"], slideJSON["duration"], slideJSON["ID"],""))
				elif currentMessage["action"] == "add-slide":
					addSlide(slides, Slide(infoForAddition))
				elif currentMessage["action"] == "delete-slide":
					deleteSlide(slides, infoForAddition["ID"])
				elif currentMessage["action"] == "edit-slide":
					editSlide(slides, infoForAddition["ID"], Slide(infoForAddition))
				elif currentMessage["action"] == "Terminate":
					Run = False
					break
			#Are time accuracies will all be within 1 sec
			time.sleep(1)
		# Move on

		x  = (x+1) % len(slides)




