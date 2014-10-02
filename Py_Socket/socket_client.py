#!/usr/bin/python
import socket, select, string, sys, time, json

from message import Message
from socketlist import socketList
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

def connect(host, port): 
    while True:
        # connect to remote host
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.settimeout(2)
        try :
            s.connect((host, port))
            print "Connected"
            break
        except :
            print 'Unable to connect'
            time.sleep(2)
    # Passes along PIE name to Grandma
    identify = Message("blueberry", "Grandma", "connect",{})
    identify.add_content("name","blueberry")
    identify.add_content("item2","bob")
    print s
    print type(s)
        # print "Its a Socket!"
    s.send(identify.toJSON())
    return s  

def reConnect(s, host, port):
    print "Disconnected"
    s.close()
    s = None
    s = connect(host, port)

def main():
    socketQueue = multiprocessing.Queue(100)
    thread.start_new_thread(socket_thread, (socketQueue,))
    sleep(20)
    socketQueue.put("{\"dest\": \"Grandma\", \"src\": \"blueberry\", \"content\": {\"name\": \"blueberry\"}, \"action\": \"getSlides\"}")


#main function
def socket_thread(socketQueue):
    host = "127.0.0.1"
    port = 5000

    # self_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # self.settimeout(2)
    # connection = socketList({}, [], self_socket)
    # connection.addSocket(server_socket)
    s = connect(host, port)
    print s

    run = True
    print("blueberry")
    while run:      
        socket_list = [sys.stdin, s, socketQueue._reader]
        # Get the list sockets which are readable
        print "Hang"
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        print read_sockets
        for sock in read_sockets:
            print sock
            if type(sock) == type(s):
                if sock == s:
                    data = sock.recv(4096)
                    print data
                    if not data:
                        s = reConnect(s, host , port)
                    else :
                        currentMessage = json.loads(data)
                        functions[currentMessage["action"]](connection = connection, currentMessage = currentMessage, pieMap = connection.pieMap, sock = sock)

                #user entered a message
                else :
                    print "input"
                    msg = Input()
                    print s
                    print "Sending"
                    print msg.toJSON()
                    s.send("{\"dest\": \"Grandma\", \"src\": \"blueberry\", \"content\": {\"name\": \"blueberry\"}, \"action\": \"getSlides\"}")
            else:
                if not sock.empty():
                    s.send(mainQueue.get())

if __name__ == "__main__":
    main()