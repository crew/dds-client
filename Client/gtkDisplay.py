#!/usr/bin/env python

import threading
import time

import gobject
import gtk
import webkit
from Plugins.plugin import Plugin


class WebBrowser(gtk.Window):
    """
    Web Page Display Window Class
    Represents a full screen GTK Web Browser (no UI)
        displaying a given URL.
    @note: URL must begin with a prefix (e.g. "http://")
    @note: Extension of the python-gtk-webkit presentation program
                    Copyright (C) 2009 by Akkana Peck
    @license: GNU Public License, version 2
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self, url, width, height):
        """
        GTK Window Constructor
        @param url: The initial URL to show
        @type url: String
        @param width: The Screen's Width
        @type width: Integer
        @param height: The Screen's Height
        @type height: Integer
        @return: The Constructed WebBrowser
        @rtype: WebBrowser
        """
        gtk.Window.__init__(self)
        self.fullscreen()

        self._browser = webkit.WebView()
        settings = webkit.WebSettings()
        settings.set_property('enable-page-cache', True)
        settings.set_property('enable-accelerated-compositing', True)

        self._browser.set_settings(settings)
        self.connect('destroy', gtk.main_quit)
        self.add(self._browser)

        self._browser.load_uri(url)
        self._browser.set_size_request(int(width), int(height))
        self.show_all()

        gobject.threads_init()

    def updatePage(self, url):
        """
        Updates the browser to show the given URL
        @param url: The new URL to show
        @type url: String
        @return: None
        @rtype: NoneType
        """
        print "Update page running in : " + threading.currentThread().getName()
        print "updatePage"
        self._browser.load_uri(url)
        try:
            self.fullscreen()
        except:
            pass
        print "showing"
        self.show_all()


def getUpdateHandle(runtimeVars):
    """
    Initializes the browser and returns the
        function used to update its page
    @param runtimeVars: User-defined Configuration
    @type runtimeVars: Dictionary
    @return: Function
    """
    browser = WebBrowser("", runtimeVars["width"], runtimeVars["height"])

    # GTK Thread-Safe Wrapper for updatePage() method
    def updatePage(url):
        gobject.timeout_add(100, browser.updatePage, url)

    return updatePage


class GTKPlugin(Plugin):
    """
    GTK Web Display Plugin Class
    @see: Plugins/plugin.py for more information
    @copyright: Northeastern University Crew 2014
    """

    def needsThread(self):
        return True

    def run(self, runtimeVars):
        gtk.main()
        while True:
            print "Main loop"
            time.sleep(5)

    def getName(self):
        return "Gtk Plugin"

    def addMessage(self, message):
        raise Exception("GTKPlugin does not take any messages")