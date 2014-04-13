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

# Logging to syslog
import syslog

import ConfigParser
import subprocess
import shlex

settings = ConfigParser.RawConfigParser()
settings.read('PIEConfig.cfg')

def main():
    # initialize graphics
    pygame.init()
    pygame.mouse.set_visible(False)
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)

    # temporary get before loop
    log("Getting initial slides from " + settings.get('SlideRequests', 'server'))
    slides = getSlides()
    # render first slide in the loop before we start
    grabImage(slides[0].location, "slide_0.png", size)
    
    runLoop = True
    while runLoop:
        log("Refreshing slides from " + settings.get('SlideRequests', 'server'))
        print(settings.get('SlideRequests', 'server'))
        slides = getSlides()
        for i in range(0, len(slides)):
            indexNextSlide = (i + 1) % len(slides)
            s = slides[indexNextSlide]
            log("Displaying slide")
            dispImage("slide_" + str(i) + ".png", screen, size, black)
            timeStartedRendering = time.time()
            log("Grabbing slide at " + s.location)
            grabImage(s.location, "slide_" + str(indexNextSlide) + ".png", size)
            
            log("Waiting for next slide")
            timeItTookToRenderSlide = timeStartedRendering - time.time()
            timeToSleep = s.duration - timeItTookToRenderSlide
            if timeToSleep > 0:
                time.sleep(timeToSleep)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                runLoop = False
                pygame.display.quit()
            if event.type == pygame.KEYUP and event.key == pygame.K_c:
                runLoop = False
                pygame.display.quit()

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

# Screencap the site at the specified URL and save it as the specified file name
def grabImage(url, name, size):
    width = size[0]
    height = size[1]
    cmd = ('''sudo xvfb-run -e /dev/stdout --server-args "-screen 0, ''' + 
        str(width) + 
        '''x''' + 
        str(height) + 
        '''x24" /usr/bin/cutycapt --url=''' + 
        url + 
        ''' --out=''' + 
        name + 
        ''' --min-width=''' + 
        str(width) + 
        ''' --min-height=''' + 
        str(height))
    proc = subprocess.Popen(shlex.split(cmd))
    proc.communicate()

# Display the specified image using pygame
def dispImage(name, screen, size, black):
    # global size, black
    img = pygame.image.load(name)
    imgrect = img.get_rect()
    screen.fill(black)
    screen.blit(img, imgrect)
    pygame.display.flip()

# Save messages to syslog
def log(msg):
    msg = "PIE: " + msg
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

if __name__ == "__main__":
    main()
