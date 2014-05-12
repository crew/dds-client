#!/usr/bin/python


# Dependencies:

# cutycapt
# python-pygame
# xvfb

# MUST RUN AS SUDO TO WORK

# Specify server location and PIE name in PIEConfig.cfg

import json
import urllib2
import pygame
import sys
import time
from subprocess import call
import os
import socket # for hostname

# Logging to syslog
import syslog

import ConfigParser
import subprocess
import shlex

configFileName = 'PIEConfig.cfg'

settings = ConfigParser.RawConfigParser()
settings.read(configFileName)

fileLocation = os.path.dirname(os.path.abspath(__file__)) + "/"

# Keeps track of errors that happen
error = None

def main():
    global settings
    global error
    global slides
    global fileLocation
    # initialize graphics
    pygame.init()
    pygame.mouse.set_visible(False)
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    
    displayCentered(getImage(fileLocation + "icons/crew.png"), screen)
    time.sleep(2)
    
    if str(settings.get('SlideRequests', 'name')) == "default":
        hostname = socket.gethostname()
        displayText("DDS: PIE name not set. Using hostname: " + hostname, screen)
        settings.set('SlideRequests', 'name', hostname)
        
        # save configuration with hostname
        configFile = open(configFileName, 'w')
        settings.write(configFile)
        configFile.close()
        
        # set display in error state
        error = "error"
        displayErrorImage(screen)
        time.sleep(2)
        # forget about error and continue
        error = None

    # Make "queued" directory for slides if it does not exist
    displayText("DDS: Checking for queue directory...", screen)
    if not os.path.exists(fileLocation + "queued"):
        displayText("DDS: Creating queue directory...", screen)
        os.makedirs(fileLocation + "queued")
    
    # temporary get before loop
    displayText("DDS: Getting slides from server...", screen)
    log("Getting initial slides from " + settings.get('SlideRequests', 'server'))
    slides = getSlides()
    # render first slide in the loop before we start
    if not (slides is None) and (len(slides) > 0):
        displayText("DDS: Rendering first slide...", screen)
        renderPage(slides[0].location, "slide_0.png", size)
    else:
        slides = waitForSlides(slides, screen)
    
    displayText("DDS: Displaying...", screen)
    runLoop = True
    while runLoop:
        # Refreshes slides
        log("Refreshing slides from " + settings.get('SlideRequests', 'server'))
        
        if testConnection():
            slides = getSlides()
        # Displays slides
        if (slides is None) or (len(slides) == 0):
            print "thing"
            slides = waitForSlides(slides, screen)
            
        for i in range(0, len(slides)):
            
            log("Displaying slide")
            displaySlide("slide_" + str(i) + ".png", screen, size, black)
            
            timeToSleep = renderNext(i, slides, size)
            
            if timeToSleep > 0:
                time.sleep(timeToSleep)
            else:
                log("Missed time budget by " + timeToSleep + " seconds")
        # Allows shutdown
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                runLoop = False
                pygame.display.quit()
            if event.type == pygame.KEYUP and event.key == pygame.K_c:
                runLoop = False
                pygame.display.quit()

# Renders the next slide so it can be displayed
def renderNext(index, slides, size):
    timeStartedRendering = time.time()
    indexNextSlide = (index + 1) % len(slides)
    s = slides[indexNextSlide]
    log("Grabbing slide at " + s.location)
    if testConnection():
        renderPage(s.location, "slide_" + str(indexNextSlide) + ".png", size)
        
    log("Waiting for next slide")
    
    timeItTookToRenderSlide = timeStartedRendering - time.time()
    timeToSleep = s.duration - timeItTookToRenderSlide
    return timeToSleep

# Keep on contacting the server until you get something to display
def waitForSlides(slideList, screen):
    while (slideList is None) or (len(slideList) == 0):
        displayText("DDS: No slides assigned to hostname '" + 
                 str(settings.get('SlideRequests', 'name')) + 
                 "' on " +
                 str(settings.get('SlideRequests', 'server')) , screen)
        time.sleep(5)
        slideList = getSlides() # try every 5 seconds to get the slides
    return slideList

# Display the given text onscreen
def renderText(string):
    font = pygame.font.Font(None, 48)
    text = font.render(string, 1, (250, 250, 250))
    return text

# Load the image at the specified location
def getImage(location):
    return pygame.image.load(location)

# Display the given text in the center of the given screen
def displayText(string, screen):
    displayCentered(renderText(string), screen)

# Display the given image in the center of the given screen
def displayCentered(image, screen):
    bg = pygame.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((0, 0, 0))
    pos = image.get_rect()
    pos.centerx = bg.get_rect().centerx
    pos.centery = bg.get_rect().centery
    screen.blit(bg, (0, 0))
    screen.blit(image, pos)
    pygame.display.flip()
    displayErrorImage(screen)

# Display the icon associated with the current error
def displayErrorImage(screen):
    global error
    if error != None:
        img = getImage(fileLocation + 'icons/' + error + ".png")
        bg = pygame.Surface(screen.get_size())
        pos = img.get_rect()
        pos.left = bg.get_rect().left
        pos.bottom = bg.get_rect().bottom
        screen.blit(img, pos)
        pygame.display.flip()

# Display the specified slide
def displaySlide(name, screen, size, black):
    displayImage(fileLocation + 'queued/' + name, screen, size, black)

# Display the specified image (located in the "queued" folder) using pygame
def displayImage(name, screen, size, black):
    # global size, black
    img = getImage(name)
    imgrect = img.get_rect()
    screen.fill(black)
    screen.blit(img, imgrect)
    pygame.display.flip()
    displayErrorImage(screen) # renders on top of this

# Can this PIE connect to the server?
def testConnection():
    global error
    response = os.system("ping -c 1 " + str(settings.get('SlideRequests', 'server')))
    if response == 0:
        error = None
        return True
    else:
        error = "disconnect"
        return False

# Get the list of Slides that need to be displayed from the server in PIEConfig.cfg
def getSlides():
    global settings
    try:
        url = "http://" + str(settings.get('SlideRequests', 'server')) + "/wp-admin/admin-ajax.php?action=dds_api&pie_name=" + str(settings.get('SlideRequests', 'name'))
        jsonString = str(urllib2.urlopen(url).read().decode("utf-8"))
        print jsonString
        decoder = json.JSONDecoder()
        slides = []
        obj = decoder.decode(jsonString)
        list = obj['actions']
        print list
        for item in list:
            slides.append(Slide(item['location'], item['duration']))
        return slides
    except:
        log("Error: Bad URL/JSON")

# Screencap the site at the specified URL and save it as the specified file name in the "queued" folder
def renderPage(url, name, size):
    width = size[0]
    height = size[1]
    cmd = ('''sudo xvfb-run -e /dev/stdout --server-args "-screen 0, ''' + 
        str(width) + 
        '''x''' + 
        str(height) + 
        '''x24" /usr/bin/cutycapt --url=''' + 
        url + 
        ''' --out=''' + 
        fileLocation + 'queued/' + name + 
        ''' --min-width=''' + 
        str(width) + 
        ''' --min-height=''' + 
        str(height) +
        ''' --zoom-factor=2''')
    proc = subprocess.Popen(shlex.split(cmd))
    proc.communicate()
    
# Save messages to syslog
def log(msg):
    msg = "\t\t\t\tPIE: " + msg
    print msg
    syslog.syslog(syslog.LOG_ERR, msg)

# Represents content grabbed from the server that will be displayed onscreen
class Slide:
    # URL where we can find this Slide's content
    location = None
    # How long to display this Slide (in seconds)
    duration = None

    def __init__(self, l, d):
        self.location = l
        self.duration = d

    def __str__(self):
        return self.location + ", " + str(self.duration)

# Runs everything
if __name__ == "__main__":
    main()
