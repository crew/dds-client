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

error = None

def main():
    global settings
    global error
    # initialize graphics
    pygame.init()
    pygame.mouse.set_visible(False)
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    
    displayImage("icons/crew.png", screen, size, black)

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
        time.sleep(5)
        # forget about error and continue
        error = None

    # Make "queued" directory for slides if it does not exist
    displayText("DDS: Checking for queue directory...", screen)
    if not os.path.exists("queued"):
        displayText("DDS: Creating queue directory...", screen)
        os.makedirs("queued")
    
    # temporary get before loop
    displayText("DDS: Getting slides from server...", screen)
    log("Getting initial slides from " + settings.get('SlideRequests', 'server'))
    slides = getSlides()
    # render first slide in the loop before we start
    if not (slides is None):
        displayText("DDS: Rendering first slide...", screen)
        renderPage(slides[0].location, "slide_0.png", size)
    else:
        while (slides is None):
            displayText("DDS: No slides assigned to hostname '" + 
                     str(settings.get('SlideRequests', 'name')) + 
                     "' on " +
                     str(settings.get('SlideRequests', 'server')) , screen)
            time.sleep(5)
            slides = getSlides() # try every 5 seconds to get the slides
    
    displayText("DDS: Displaying...", screen)
    runLoop = True
    while runLoop:
        # Refreshes slides
        log("Refreshing slides from " + settings.get('SlideRequests', 'server'))
        
        if testConnection():
            slides = getSlides()            
        # Displays slides
        for i in range(0, len(slides)):
            indexNextSlide = (i + 1) % len(slides)
            s = slides[indexNextSlide]
            log("Displaying slide")
            displaySlide("slide_" + str(i) + ".png", screen, size, black)
            timeStartedRendering = time.time()
            log("Grabbing slide at " + s.location)
            if testConnection():
                renderPage(s.location, "slide_" + str(indexNextSlide) + ".png", size)
                log("Waiting for next slide")
            timeItTookToRenderSlide = timeStartedRendering - time.time()
            timeToSleep = s.duration - timeItTookToRenderSlide
            if timeToSleep > 0:
                time.sleep(timeToSleep)
        # Allows shutdown
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                runLoop = False
                pygame.display.quit()
            if event.type == pygame.KEYUP and event.key == pygame.K_c:
                runLoop = False
                pygame.display.quit()

# Display the given text in the center of the given screen
def displayText(string, screen):
    font = pygame.font.Font(None, 48)
    text = font.render(string, 1, (250, 250, 250))
    displayCentered(text, screen)
    
def displayErrorText(string, screen):
    font = pygame.font.Font(None, 48)
    text = font.render(string, 1, (250, 250, 250))
    bg = pygame.Surface(screen.get_size())
    pos = text.get_rect()
    pos.left = bg.get_rect().left
    pos.bottom = bg.get_rect().bottom
    screen.blit(text, pos)
    pygame.display.flip()
    
def displayCentered(text, screen):
    bg = pygame.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((0, 0, 0))
    pos = text.get_rect()
    pos.centerx = bg.get_rect().centerx
    pos.centery = bg.get_rect().centery
    screen.blit(bg, (0, 0))
    screen.blit(text, pos)
    pygame.display.flip()
    displayErrorImage(screen)

def displayErrorImage(screen):
    global error
    if error != None:
        img = pygame.image.load('icons/' + error + ".png")
        bg = pygame.Surface(screen.get_size())
        pos = img.get_rect()
        pos.left = bg.get_rect().left
        pos.bottom = bg.get_rect().bottom
        screen.blit(img, pos)
        pygame.display.flip()
        
def displaySlide(name, screen, size, black):
    displayImage('queued/' + name, screen, size, black)

# Display the specified image (located in the "queued" folder)  using pygame
def displayImage(name, screen, size, black):
    # global size, black
    img = pygame.image.load(name)
    imgrect = img.get_rect()
    screen.fill(black)
    screen.blit(img, imgrect)
    pygame.display.flip()
    displayErrorImage(screen)

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
        'queued/' + name + 
        ''' --min-width=''' + 
        str(width) + 
        ''' --min-height=''' + 
        str(height) +
        ''' --zoom-factor=2''')
    proc = subprocess.Popen(shlex.split(cmd))
    proc.communicate()
    
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
