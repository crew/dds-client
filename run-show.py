#!/usr/bin/python


# Dependencies:

# cutycapt
# python-pygame
# xvfb


# MISC. TODO
# - "Better" logging (more detailed?)
# - Document dependencies and other stuff
# - Pull properties such as resolution and URL from a PIE config file

# NOTE: PIE = Personal Information Endpoint
# Use this from now on when referring to clients instead of "Pi".

import json
import urllib2
import pygame
import sys
import time
from subprocess import call

# Logging to syslog
import syslog

import subprocess
import shlex
pygame.init()

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
black = 0, 0, 0

screen = pygame.display.set_mode(size)


# Used to pull info from JSONs
decoder = json.JSONDecoder()

# Load PIE-specific properties from some sort of local config
# (maybe get display resolution from that config)
pID = 0
pygame.mouse.set_visible(False)
# Grabs the contents of the given URL in plain text
def getProperties(url):
    try:
        return str(urllib2.urlopen(url).read().decode("utf-8"))
    except:
        log("Error: Bad URL")

# Produce a list of Slides from a JSON string
def json2Slides(json):
    try:
        print(json)
    	slides = []
    	obj = decoder.decode(json)
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

# Set jsonUrl to the location of the JSON data source
jsonUrl = "http://10.0.0.61/wp-admin/admin-ajax.php?action=dds_api"

runLoop = True
while runLoop:
    log("Refreshing slides from jsonUrl")
    slides = json2Slides(getProperties(jsonUrl))
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
#!/bin/sh
