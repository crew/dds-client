#!/usr/bin/python
import select
import sys
import time
import json
import Queue

from Classes.message import Message
from Classes.sockClass import sockClass
from logging import Logger
from Plugins.plugin import Plugin


def socket_out(currentMessage, socket):
    """
    Writes the given Message to the given socket
    @param currentMessage: The Message to write
    @type currentMessage: Message
    @param socket: The socket to write to
    @type socket: Socket
    @return: None
    @rtype: NoneType
    """
    Logger.log("DEBUG", "Outbound Message: " + currentMessage.toJSON())
    if currentMessage.dest == "Grandma":
        try:
            socket.send(currentMessage.toJSON() + '\v')
        except Exception, e:
            print str(e)
            Logger.log("ERROR", "Socket raised exception on send - exception : " + str(e))
            raise Exception("Can't send message. Socket = " + str(socket))
    else:
        Logger.log("WARNING", "Message not addressed to grandma")
    print "Socket Message Sent!"


def socket_in(s, runtimeVars, route):
    """
    Reads and redirects messages received by the client
    @param s: The Client Socket
    @type s: sockClass
    @param runtimeVars: User-defined Configuration
    @type runtimeVars: Dictionary
    @param route: The message handlers for the client plugins
    @type route: Dictionary
    @return: None
    @rtype: NoneType
    """
    run = True
    while run:
        socket_list = [s.sock, ]
        # Get the list of sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            if sock == s.sock:
                data = sock.recv(4096)
                if not data:
                    s.connect(runtimeVars)
                else:
                    messages = filter(lambda s: s != "",
                                      data.split('\v'))
                    for currentMessage in messages:
                        currentMessage = json.loads(currentMessage)
                        if currentMessage["pluginDest"] == "Main":
                            sys.exit(0)
                        print "Got message : " + str(currentMessage)
                        messageDestination = currentMessage["pluginDest"]
                        print "Received message sending it too : " + str(messageDestination)
                        route[messageDestination](Message.fromJSON(currentMessage))
            else:
                print "Something Goofed"
        # We all program updates will be in multiples of 1 sec,
        # as this is the slide time accuracy
        time.sleep(1)


class IOPlugin(Plugin):
    """
    Socket I/O Plugin Class
    @see: Plugins/plugin.py for more information
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self):
        self.queue = Queue.Queue(100)
        self.msgRoute = None
        self.socket = None

    def needsThread(self):
        return True

    def setup(self, messageDict, runtimeVars):
        self.msgRoute = messageDict
        self.socket = sockClass(runtimeVars)

    def run(self, runtimeVars):
        if self.msgRoute is None:
            raise Exception("Can't distribute info; message route is None")
        socket_in(self.socket, runtimeVars, self.msgRoute)

    def getName(self):
        return "IOPlugin"

    def addMessage(self, message):
        print "Attempting to send Message"
        if self.socket is None:
            Logger.log("WARNING", "No socket connection, trying again...")
            time.sleep(.5)
            self.addMessage(message)
        else:
            socket_out(message, self.socket)
