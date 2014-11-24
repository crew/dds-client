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


import sys, thread, time
import gobject
import gtk
import glib
import webkit
import threading
from Classes.slide import Slide
import Queue
from Plugins.plugin import Plugin

#for testing
import time
#sys.settrace

# Represents fullscreen gtk window displaying
#   the URL provided to it
# Note: URL must begin with prefix (e.g. "http://")
class WebBrowser(gtk.Window):
	def __init__(self, url, width, height):
		gtk.Window.__init__(self)
		self.fullscreen()

		self._browser= webkit.WebView()
		settings = webkit.WebSettings()
		settings.set_property('enable-page-cache', True)
		settings.set_property('enable-accelerated-compositing', True)
		"""pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
		color = gtk.gdk.Color()
		cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)"""

		self._browser.set_settings(settings)
		self.connect('destroy', gtk.main_quit)
		self.add(self._browser)

		self._browser.load_uri(url)
		self._browser.set_size_request(int(width), int(height))
		self.show_all()

		gobject.threads_init()
		
		

	def updatePage(self,url):
		print "Update page running in : "+threading.currentThread().getName()
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


	

#Initializes the browser and returns a function used to update the page
def getUpdateHandle(runtimeVars):
	browser = WebBrowser("", runtimeVars["width"], runtimeVars["height"])
	def updatePage(url):
		gobject.timeout_add(100,browser.updatePage, url)
	return updatePage
	

class GTKPlugin(threading.Thread):
	def needsThread(self):
		return True;
	def run(self, runtimeVars):
		gtk.main()
	def getName(self):
		return "Gtk Plugin"
	def addMessage(self, message):
		raise Exception("GTKPlugin does not take any messages")
