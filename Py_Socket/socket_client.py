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

# def connect(s, host, port): 
#     while True:
#         # connect to remote host
#         #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         #s.settimeout(2)
#         try :
#             s.connect((host, port))
#             print "Connected"
#             break
#         except :
#             print 'Unable to connect'
#             time.sleep(2)
#     # Passes along PIE name to Grandma
#     identify = Message("blueberry", "Grandma", "connect",{})
#     identify.add_content("name","blueberry")
#     identify.add_content("item2","bob")
#     print s
#     print type(s)
#         # print "Its a Socket!"
#     s.send(identify.toJSON())
#     return s  

# def reConnect(s, host, port):
#     print "Disconnected"
#     s.close()
#     s = None
#     s = connect(host, port)

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

    # self.settimeout(2)
    # connection = socketList({}, [], self_socket)
    # connection.addSocket(server_socket)
    # s = connect(s, host, port)
    print s.sock

    run = True
    print("blueberry")
    while run:      
        socket_list = [sys.stdin, s.sock]
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