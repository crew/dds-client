#!/usr/bin/env python

# GTK-Based Fullscreen Web Display Client
#    Description: Client accepting pushes
#    from server to load webpages. Intended
#    for use in DDS System

# Extension of python-gtk-webkit presentation program
#                   Copyright (C) 2009 by Akkana Peck.
# (Out of compliance with Peck's copyright, the following
#       is released under GPL v2)

# Copyright (C) 2014 Northeastern University CCIS Crew


import sys
import gobject
import gtk
#import glib
import webkit
import threading
from slide import Slide
import Queue

#for testing
import time
#sys.settrace

# Represents fullscreen gtk window displaying
#   the URL provided to it
# Note: URL must begin with prefix (e.g. "http://")
class WebBrowser(gtk.Window):
    def __init__(self, url):
        gtk.Window.__init__(self)
        self.fullscreen()

        self._browser= webkit.WebView()
        self.add(self._browser)
        settings = webkit.WebSettings()
        settings.set_property('enable-page-cache', True)
        self._browser.set_settings(settings)
        self.connect('destroy', gtk.main_quit)

        self._browser.load_uri(url)
        self.show_all()

        gobject.threads_init()
        
        

    def updatePage(self,url):
        print "updatePage"
        # self.connect("destroy", gtk.main_quit)
        self._browser.load_uri(url)
        #while (self._browser.get_load_status() < 2):
        #   continue
        try:
           self.fullscreen()
        except:
           pass
        print "showing"
        self.show_all()

#test
def openPageTest():
    time.sleep(5)
    openPage("http://dds-wp.ccs.neu.edu/?slide=test-ccis-tutoring&pie_name=chocolate")

# Class Definition of Page-Updating Thread

# TODO: Integrate with existing queues
class PageUpdateThread (threading.Thread):
    def __init__(self, queue=None):
        threading.Thread.__init__(self)
        self.threadID = 1
        self.name = "Page Update"
        self.queue = queue
        self.webBrowser = WebBrowser("")
    def run(self):
        while 1:
            currentSlide = self.queue.get()
            gobject.timeout_add(100,self.webBrowser.updatePage, currentSlide.url)
            time.sleep(currentSlide.duration)
            self.queue.put(currentSlide)

# Allows initial bash invocation to load
#      webpage passed as argument
#if __name__ == "__main__":
    #if len(sys.argv) <= 1 :
    #    print("Usage:", sys.argv[0], "url")
    #    sys.exit(0)

testQueue = Queue.Queue(100)
testQueue.put(Slide("http://facebook.com", 5))
testQueue.put(Slide("http://dds-wp.ccs.neu.edu/?slide=test-ccis-tutoring&pie_name=chocolate", 10))


pageUpdateThread = PageUpdateThread(testQueue)

pageUpdateThread.start()

gtk.main()

# Called on program start and contains
#   gtk.main() (Runs until gtk.main_quit()...
#   i.e. for the program's duration)
#def mainThread(url):
#    gobject.threads_init()
#    webbrowser = WebBrowser(sys.argv[1])
#   gtk.main()



# Refreshing:
# while True:
#   time.sleep(10)
