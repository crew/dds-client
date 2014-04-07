#!/usr/bin/python
# Need shebang when running from command-line

# Dependencies:

# cutycapt
# python-pygame
# xvfb 


# MISC. TODO
# - "Better" logging (don't log everything as errors)
# - Document dependencies and other documentation stuff
# - Display timings and continuous execution (display for a bit, move on, repeat)

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



# Stupid test JSON (make sure this directory is on the test machine!)
tempurl = "http://crewbie-01.crew.ccs.neu.edu/samplejson.txt"

# Used to pull info from JSONs
decoder = json.JSONDecoder()

# Load Pi-specific properties from some sort of local config
# (maybe get display resolution from that config)
pID = 0

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
#call(["sh","script.sh", url, name])


def urlScreengrab(url, width, height, imageName, **kwargs):
    cmd = '''xvfb-run --server-args "-screen 0, '''+str(width)+'''x'''+str(height)+'''x24" /usr/bin/cutycapt --url='''+url+''' --out='''+imageName+''' --min-width='''+str(width)+''' --min-height='''+str(height)
    print cmd
    proc = subprocess.Popen(shlex.split(cmd))
    proc.communicate()

# Display the specified image using fbi
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
    # How long to display this Slide (in milliseconds)
    duration = None
       
    def __init__(self, l, d):
        self.location = l
        self.duration = d

    def __str__(self):
        return self.location + ", " + str(self.duration)

    # Displays this slide on the Pi
    def display(self):
        global pID
        log("grabing image")
	grabImage(self.location, "test.jpg")
	log("image retrieved")
	dispImage("test.jpg")

# Look, I don't know how you guys are doing this, but this code is how I got it to work nicely

grabImage("http://pitcam.ccs.neu.edu", "test123.jpg")
# Testing nonsense
while True:
    print "grabbing"
    print "displaying"
    dispImage("test123.jpg")
    grabImage("http://pitcam.ccs.neu.edu", "test123.jpg")
    time.sleep(5)
    print "finished"
#slides = json2Slides(getProperties(tempurl))
#slides[0].display()


# xvfb-run --server-args="-screen 0, 1280x1024x24" cutycapt --url=URL --out=FILENAME
# fbi FILENAME
# URL is the URL for the image in single quotes (don't forget to encode!)
# FILENAME is the name of the image cutycapt outputs (which gets displayed by fbi)
# do this with a bash script, i guess

# Make sure clients have the urllib2 library installed!
#!/bin/sh
