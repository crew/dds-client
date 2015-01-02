import Queue
import json
import datetime
import time
import sys

from Classes.message import Message
from Classes.slide import Slide
from logging import Logger
from Plugins.plugin import Plugin
import gtkDisplay


class SlideShowPlugin(Plugin):
    """
    Slide Show Plugin Class
    @see: Plugins/plugin.py for more information
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self):
        self.updateHandle = None
        self.inQ = Queue.Queue(100)
        self.outHandle = None

    def needsThread(self):
        return True

    def run(self, runtimeVars):
        if self.updateHandle is None or self.outHandle is None:
            raise Exception("Something went wrong...")
        runShow(self.inQ, runtimeVars, self.updateHandle, self.outHandle)

    def setup(self, messageDict, runtimeVars):
        self.updateHandle = gtkDisplay.getUpdateHandle(runtimeVars)
        self.outHandle = messageDict["IOPlugin"]

    def getName(self):
        return "slideShow"

    def addMessage(self, message):
        print "Adding : " + str(message)
        self.inQ.put(message, True)


def runShow(inputQueue, runtimeVars, setPage, writeOut):
    """
    Runs the slide show (manages GTK and incoming messages)
    @param inputQueue: The Slide Show Plugin's input queue
    @type inputQueue: Queue.Queue
    @param runtimeVars: User-defined Configuration
    @type runtimeVars: Dictionary
    @param setPage: The function which sets the GTK Display's webpage
    @type setPage: Function
    @param writeOut: The socket outgoing message queue
    @type writeOut: Function
    @return: None
    @rtype: None
    """
    # TODO get DT
    slideRequest = Message(runtimeVars["name"], "Grandma", 'WPHandler', "load-slides", "Maor slidez")
    print "slideReuqest " + slideRequest.toJSON()
    writeOut(slideRequest)

    slides = []
    # Replace with loading slide
    slides.append(
        Slide.makeSlide("file:///home/pi/dds-client/Client/resources/loading_screen/index.html", 5, -1, ""))

    # Temp Weather slide for testing purposes. Uncomment as needed.
    # slides.append(Slide("http://104.131.73.58", 10))

    # Helper to get the slide out of the slide list with the given ID, also insures uniqueness if ID's
    def getSlideById(slideList, id):
        print "getSlideById called. currentMessage(" + str(type(currentMessage)) + "):", currentMessage
        matches = filter(lambda x: x.sameID(id), slideList)
        if len(matches) > 1:
            raise Exception("Why are there two slides with the same ID?")
        return None if len(matches) == 0 else matches[0]

    def deleteSlide(slideList, id):
        print "Deleting slide..."
        temp = getSlideById(slides, id)
        Logger.log("DEBUG", "Removing slide: " + str(temp))
        if temp:
            slideList.remove(temp)

    def editSlide(slideList, id, newSlide):
        print "Editing slide..."
        old = getSlideById(slides, id)
        Logger.log("DEBUG", "Changing slide :" + str(old) + " to " + str(newSlide))
        if old:
            slideList.remove(old)
        slideList.append(newSlide)

    def addSlide(slideList, slide):
        print "Adding slide..."
        Logger.log("DEBUG", "Adding slide :" + str(slide))
        slideList.append(slide)

    x = 0
    Run = True
    while Run:
        print str(slides)
        #
        if len(slides) > 1 and getSlideById(slides, -1) is not None:
            print "Slides have loaded removing loading slide..."
            # Following line needed for situations in which
            # a client only has one slide to show
            x = 0
            slides.remove(getSlideById(slides, -1))
        if len(slides) == 0:
            print "I Have no slides, stopping slide show..."
            Logger.log("ERROR", "Ran out of slides...")
            sys.exit(0)
            # TODO: Handle this situation better.
            # (Currently, the slide show will
            # simply freeze on its last received
            #        slide at this point)
        currentSlide = slides[x]
        target_time = datetime.datetime.now() + datetime.timedelta(seconds=currentSlide.duration)
        setPage(currentSlide.url)
        print "Just set page : " + currentSlide.url
        while datetime.datetime.now() < target_time:
            if not inputQueue.empty():
                currentMessage = inputQueue.get()
                infoForAddition = json.loads(currentMessage["content"])
                if currentMessage["action"] == "load-slides":
                    for slideJSON in infoForAddition["actions"]:
                        # TODO fields in dds-api call need to be changed to standard,
                        #   they also need ID and meta added @Eddie
                        addSlide(slides,
                                 Slide.makeSlide(slideJSON["location"], slideJSON["duration"], slideJSON["ID"],
                                                 ""))
                elif currentMessage["action"] == "add-slide":
                    addSlide(slides, Slide(infoForAddition))
                elif currentMessage["action"] == "delete-slide":
                    deleteSlide(slides, infoForAddition["ID"])
                elif currentMessage["action"] == "edit-slide":
                    editSlide(slides, infoForAddition["ID"], Slide(infoForAddition))
                elif currentMessage["action"] == "Terminate":
                    Run = False
                    break
            time.sleep(1)
        # Move on
        if len(slides):
            x = (x + 1) % len(slides)
