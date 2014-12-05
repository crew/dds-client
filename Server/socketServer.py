#!/usr/bin/python

## Check out zmq, activemq rabbitmq
# Tcp Chat server


import socket, select, json, thread, string, time

from Classes.socketlist import socketList
from Classes.message import Message
from Classes.slide import Slide
from WPHandler import wpListenerStart

#Function to broadcast chat messages to all connected clients


def connect(**kwargs):
    print "wooho"
    pie = kwargs["currentMessage"]["src"] 
    kwargs["connection"].mapPie(kwargs["sock"],pie)
    print "Done mapping pie"
    #time.sleep(.5)
    return kwargs

def main_socketServer_thread(inputQueue, Queues, runtimeVars):
    # List to keep track of socket descriptors
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = int(runtimeVars["port"])
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    connection = socketList({}, [], server_socket)
    connection.addSocket(server_socket)
    wpListenerStart(Queues["socketServer"])
    # Map of the Pies
    pieMap = {}

    print "Chat server started on port " + str(PORT)
    thread.start_new_thread(socketServer, (connection, Queues, server_socket, RECV_BUFFER))

    Run = True
    while Run:
        if not Queues["socketServer"].empty():
            log(Queues["Logging"], "Message in Queue")
            currentMessage = Queues["socketServer"].get()
            connection.sendMessage(connection.getSock(currentMessage.dest), currentMessage.toJSON())
            

def socketServer(connection, Queues, server_socket, RECV_BUFFER):
    while 1:
        print("WHILE")
        # Get the list sockets which are ready to be read through select
        print("PRE ")
        print "PIEMAP:"
        print(connection.pieMap)
        print "sockList:"
        print(connection.sockList)
        read_sockets,write_sockets,error_sockets = select.select(connection.sockList,[],[])
        for sock in read_sockets:
            print(connection.pieMap)
            print(read_sockets)
            if sock == server_socket:
                # Handle the case in which there is a new connections    recieved through server_socket
                sockfd, addr = server_socket.accept()
                connection.addSocket(sockfd)
                print "Client Connected " + str(addr)  
            else:
                data = sock.recv(RECV_BUFFER)
                print data
                if data == "":
                    print data
                    print sock
                    connection.removeSocket(sock)
                else:
                    currentMessage = json.loads(data)
                    if not currentMessage["pluginDest"] == "socketServer":
                        print "Placing message in destination: "+currentMessage["pluginDest"]
                        Queues[currentMessage["pluginDest"]].put(Message.fromJSON(currentMessage))
                    else:
                        print "Connecting"
                        connect(connection = connection, currentMessage = currentMessage, pieMap = connection.pieMap, sock = sock)
                        print "Finished connection..."

def log(queue,mes):
    newLog = Message("Socket", "Logging", "Logger" ,"log", {})
    newLog.add_content("1",mes)
    queue.put(newLog)
