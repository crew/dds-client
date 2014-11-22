#!/usr/bin/python
import socket, select, string, sys, time, json, Queue

from Classes.message import Message
from Classes.sockClass import sockClass
from logging import Logger

from plugin import Plugin

def socket_out(outMessageQueue, socket):
	Run = True
	while Run:
		if not outMessageQueue.empty():
			currentMessage = outMessageQueue.get()
			Logger.log("DEBUG", "Outbound Message: "+currentMessage.toJSON())
			if currentMessage.dest == "Grandma":
				socket.send(currentMessage.toJSON())
			else:
				Logger.log("WARNING", "Message not addressed to grandma")
	time.sleep(.25)


def socket_in(s, runtimeVars, route):
	run = True
	while run:      
		socket_list = [s.sock,]
		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock in read_sockets:
			if sock == s.sock:
				data = sock.recv(4096)
				if not data:
					s.connect(runtimeVars)
				else :
					currentMessage = json.loads(data)
					if currentMessage["pluginDest"] == "Main":
						#TODO terminate program
						continue
					print "Got message : "+str(currentMessage)
					messageDestination = currentMessage["pluginDest"]
					print "Recieved message sending it too : "+str(messageDestination)
					route[messageDestination](Message.fromJSON(currentMessage))
					#Queues[currentMessage["pluginDest"]].put(Message.fromJSON(currentMessage))
			else :
				print "Something Goofed"


class IPlugin(Plugin):
	def __init__(self):
		self.queue = Queue.Queue(100)
		self.msgRoute = None
	def needsThread(self):
		return True;
	def setup(self, messageDict, runtimeVars):
		self.msgRoute = messageDict
		
	def run(self, runtimeVars):
		if self.msgRoute == None:
			raise Exception("Can't distribute info, message route is None")
		socket_in(runtimeVars["socket"], runtimeVars, self.msgRoute)
	def getName(self):
		return "IPlugin"
	def addMessage(self, message):
		raise Exception("WTF? what are you trying to do?")
		
class OPlugin(Plugin):
	def __init__(self):
		self.queue = Queue.Queue(100)
	def needsThread(self):
		return True
	def run(self, runtimeVars):
		socket_out(self.queue, runtimeVars["socket"])
	def getName(self):
		return "OPlugin"
	def addMessage(self, message):
		self.queue.put(message)



