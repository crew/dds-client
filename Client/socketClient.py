#!/usr/bin/python
import socket, select, string, sys, time, json

from Classes.message import Message
from Classes.sockClass import sockClass
import Queue , thread

def socket_out(Queues, socket):
	Run = True
    while Run:
        if not Queues["Socket"].empty():
            log("DEBUG", "Outbound Message: "+currentMessage.toJSON())
            currentMessage = Queues["Socket"].get()
            if currentMessage.dest == "Grandma":
                socket.send(currentMessage.toJSON())
			else:
				log("WARNING", "Message not addressed to grandma")


def socket_in(s, Queues, runtimeVars):
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
                    Queues[currentMessage["pluginDest"]].put(Message.fromJSON(currentMessage))
            else :
                print "Something Goofed"
				
def runSocketIO(inQ, queues, runtimeVars):
	sock = sockClass(runtimeVars)
	
	
	log("DEBUG", "Starting Socket Listener")
    thread.start_new_thread(socket_thread, (sockClass(runtimeVars), Queues, runtimeVars))
	
	
	log("DEBUG", "Starting Socket Writer")
	socket_out(queues, sock)
	
	
#TODO seperate in and out threads, this is non-specific		
class IOPlugin(Plugin):
	def needsThread(self):
		return True;
	def startThread(self, inQ, queues, runtimeVars):
		runSocketIO(inQ, queues, runtimeVars)
	def getName():
		return "IOPlugin"

def log(queue,mes):
	raise Exception("Didn't finish")
