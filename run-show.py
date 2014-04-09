#!/usr/bin/python


# Dependencies:

# cutycapt
# python-pygame
# xvfb


# MISC. TODO
# - "Better" logging (more detailed?)
# - Document dependencies and other stuff

# NOTE: PIE = Public Information Endpoint
# Use this from now on when referring to clients instead of "Pi".

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
pygame.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
black = 0, 0, 0

screen = pygame.display.set_mode(size)


# Enables reading of configuration settings in PIEConfig.cfg
settings = ConfigParser.RawConfigParser()
settings.read('PIEConfig.cfg')

# Eventually find a way to use this in server requests
pID = settings.get('SlideRequests', 'name')

# Hide mouse
pygame.mouse.set_visible(False)

# Grabs the slide properties JSON from the server in PIEConfig.cfg using dds_api
def getProperties():
    try:
        url = str(settings.get('SlideRequests', 'server')) + "/wp-admin/admin-ajax.php?action=dds_api"
        return str(urllib2.urlopen(url).read().decode("utf-8"))
    except:
        log("Error: Bad URL")

# Produce a list of Slides from a JSON string
def json2Slides(jsonString):
    try:
        decoder = json.JSONDecoder()
    	slides = []
    	obj = decoder.decode(jsonString)
    	list = obj['actions']
    	for item in list:
            slides.append(Slide(item['location'], item['duration']))
    	return slides
    except:
	log("Error: Bad JSON")

# Screencap the site at the specified URL and save it as the specified file name
def grabImage(url,name):
    global size
    urlScreengrab(url, size[0], size[1], name)

# grabImage helper with extra parameters (combine these two methods later)
def urlScreengrab(url, width, height, imageName, **kwargs):
    cmd = '''sudo xvfb-run -e /dev/stdout --server-args "-screen 0, '''+str(width)+'''x'''+str(height)+'''x24" /usr/bin/cutycapt --url='''+url+''' --out='''+imageName+''' --min-width='''+str(width)+''' --min-height='''+str(height)
    print cmd
    proc = subprocess.Popen(shlex.split(cmd))
    proc.communicate()

# Display the specified image using pygame
def dispImage(name):
    global size, black
    imagey = pygame.image.load(name)
    #imagey = pygame.transform.scale(imagey,(size[0],size[1]))
    imageyrect = imagey.get_rect()
    screen.fill(black)
    screen.blit(imagey, imageyrect)
    pygame.display.flip()
    #call(["fbi",name])

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

    # Displays this slide on the PIE
    def display(self):
        global pID
        log("grabing image")
	grabImage(self.location, "test.jpg")
	log("image retrieved")
	dispImage("test.jpg")

# MUST RUN AS SUDO TO WORK
# Specify server location in PIEConfig.cfg

runLoop = True
while runLoop:
    log("Refreshing slides from " + settings.get('SlideRequests', 'server'))
    slides = json2Slides(getProperties())
    for s in slides:
        log("Grabbing slide at " + s.location)
        grabImage(s.location, "currentSlide.png")
        log("Displaying slide")
        dispImage("currentSlide.png")
        log("Waiting for next slide")
        time.sleep(s.duration)
	for event in pygame.event.get():
        	if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
			runLoop = False
			pygame.display.quit()
		if event.type == pygame.KEYUP and event.key == pygame.K_c:
			runLoop = False
			pygame.display.quit()
