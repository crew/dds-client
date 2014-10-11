#!/usr/bin/python
import socket, select, string, sys, time, json

from Classes.message import Message
from Classes.sockClass import sockClass
import Queue , thread

def main_socket_thread(inputQueue, Queues, runtimeVars):
    log(Queues["Logging"], "Starting Main Socket")
    # Will be replaced with settings from config
    host = "127.0.0.1"
    port = 5000
    s = sockClass(host,port)

    functions = {}
    functions["loadSlides"] = loadSlides

    log(Queues["Logging"], "Starting Socket Listener")
    thread.start_new_thread(socket_thread, (s, Queues, functions))

    Run = True
    while Run:
        if not Queues["Socket"].empty():
            log(Queues["Socket"], "Message in Queue")
            currentMessage = Queues["Socket"].get()
            if currentMessage.dest == "Grandma":
                s.send(currentMessage.toJSON())
#    s.sock.send("{\"dest\": \"Grandma\", \"src\": \"blueberry\", \"content\": {\"name\": \"blueberry\"}, \"action\": \"getSlides\"}")

#main function
def socket_thread(s, Queues, functions):
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
                    functions[currentMessage["action"]](currentMessage = currentMessage, Queues = Queues)
            #user entered a message
            else :
                print "Something Goofed"

def log(queue,mes):
    newLog = Message("Socket", "Logging", "Logger" ,"log", {})
    newLog.add_content("1",mes)
    queue.put(newLog)
