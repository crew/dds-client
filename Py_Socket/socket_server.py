#!/usr/bin/python

## Check out zmq, activemq rabbitmq
# Tcp Chat server


import socket, select, json

from socketlist import socketList
from message import Message
from slide import Slide


#Function to broadcast chat messages to all connected clients


def connect(**kwargs):
    #print "wooho"
    pie = kwargs["currentMessage"]["content"]["name"] 
    kwargs["connection"].mapPie(kwargs["sock"],pie)
    #return kwargs["pieMap"]
    return kwargs

def getSlides(**kwargs):
    print "getSlides"
    identify = Message("Grandma", "blueberry", "loadSlides",{})
    identify.add_content("loadSlides", Slide("http:\/\/m.weather.com\/weather\/tenday\/USMA0046", 5).toJSON())
    kwargs["connection"].sendMessage(kwargs["sock"],identify.toJSON())


def main():
    #Function mapping
    functions = {}
    functions["connect"] = connect 
    functions["getSlides"] = getSlides

    # List to keep track of socket descriptors
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    connection = socketList({}, [], server_socket)
    connection.addSocket(server_socket)

    # Map of the Pies
    pieMap = {}

    print "Chat server started on port " + str(PORT)
 
    while 1:
        print("WHILE")
        # Get the list sockets which are ready to be read through select
        print("PRE ")
        print(connection.pieMap)
        print(connection.sockList)
        read_sockets,write_sockets,error_sockets = select.select(connection.sockList,[],[])
        for sock in read_sockets:
            print(connection.pieMap)
            print(read_sockets)
            if sock == server_socket:
                # Handle the case in which there is a new connections    recieved through server_socket
                sockfd, addr = server_socket.accept()
                connection.addSocket(sockfd)
                print "Client Connected"  
                #connection.broadcast(sockfd, "[%s:%s] entered room\n la-de-da" % addr)
            else:
                data = sock.recv(RECV_BUFFER)
                if data == "":
                    connection.removeSocket(sock)
                else:
                    print "incoming Message"
                    currentMessage = json.loads(data)
                    functions[currentMessage["action"]](connection = connection, currentMessage = currentMessage, pieMap = connection.pieMap, sock = sock)

if __name__ == "__main__":
    main()