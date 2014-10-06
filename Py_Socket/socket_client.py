#!/usr/bin/python
import socket, select, string, sys, time, json

from message import Message
from socketlist import socketList
from sockClass import sockClass
import Queue
import thread
from types import *
from time import sleep
import multiprocessing

def Input():
    sleep(5)
    return getSlides()

def getSlides():
    print "getSlides"
    jsonRequest = Message("blueberry", "Grandma", "getSlides", {})
    jsonRequest.add_content("name", "blueberry")
    return jsonRequest

def heartbeat():
    jsonaAnswer = {}
    return jsonRequest

def getHardware():
    jsonRequest = {}
    return jsonRequest

def main():
    host = "127.0.0.1"
    port = 5000

    s = sockClass(host,port)
    thread.start_new_thread(socket_thread, (s,))
    sleep(20)
    s.sock.send("{\"dest\": \"Grandma\", \"src\": \"blueberry\", \"content\": {\"name\": \"blueberry\"}, \"action\": \"getSlides\"}")
    sleep(20)


#main function
def socket_thread(s):
    run = True
    print("blueberry")
    while run:      
        socket_list = [s.sock,]
        # Get the list sockets which are readable
        print "Hang"
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        print "Incoming Socket"
        for sock in read_sockets:
            print sock
            if sock == s.sock:
                data = sock.recv(4096)
                print data
                if not data:
                    s.connect()
                else :
                    currentMessage = json.loads(data)
                    functions[currentMessage["action"]](connection = connection, currentMessage = currentMessage, pieMap = connection.pieMap, sock = sock)

            #user entered a message
            else :
                print "input"
                msg = Input()
                print s.sock
                print "Sending"
                print msg.toJSON()
                s.sock.send("{\"dest\": \"Grandma\", \"src\": \"blueberry\", \"content\": {\"name\": \"blueberry\"}, \"action\": \"getSlides\"}")

if __name__ == "__main__":
    main()