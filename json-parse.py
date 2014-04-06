#!/usr/bin/python
# Need shebang when running from command-line

# MISC. TODO
# - "Better" logging (don't log everything as errors)
# - Document dependencies and other documentation stuff
# - Display timings and continuous execution (display for a bit, move on, repeat)

import json
import urllib2
from subprocess import call

# Logging to syslog
import syslog

# Stupid test JSON (make sure this directory is on the test machine!)
tempurl = "file:////home/frosted/dds-tests/samplejson.txt"

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
    call(["sh","/home/frosted/dds-tests/script.sh", url, name])

# Display the specified image using fbi
def dispImage(name):
    call(["fbi",name])

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

# Testing nonsense
slides = json2Slides(getProperties(tempurl))
slides[0].display()


# xvfb-run --server-args="-screen 0, 1280x1024x24" cutycapt --url=URL --out=FILENAME
# fbi FILENAME
# URL is the URL for the image in single quotes (don't forget to encode!)
# FILENAME is the name of the image cutycapt outputs (which gets displayed by fbi)
# do this with a bash script, i guess

# Make sure clients have the urllib2 library installed!
#!/bin/sh
