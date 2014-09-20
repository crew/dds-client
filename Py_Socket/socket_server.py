#!/usr/bin/python

## Check out zmq, activemq rabbitmq
# Tcp Chat server


import socket, select, json

from socketlist import socketList
 


#Function to broadcast chat messages to all connected clients


def connect(**kwargs):
    print "wooho"
    #pie = kwargs["currentMessage"]["content"]["name"] 
    #kwargs["pieMap"][pie] = kwargs["sock"]
    #return kwargs["pieMap"]

def getSlides(**kwargs):
    print "hello!"


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
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(connection.sockList,[],[])
        print "sup"
        for sock in read_sockets:
            print sock
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                connection.addSocket(sockfd)
                print "Client (%s, %s) connected" % addr     
                connection.broadcast(sockfd, "[%s:%s] entered room\n" % addr)
            else:
                data = sock.recv(RECV_BUFFER)
                print data
                currentMessage = json.loads(data)
                functions[currentMessage["action"]](currentMessage = currentMessage, pieMap = connection.pieMap, sock = sock)
    server_socket.close()

def checkIncoming(server_socket, connection):
    print "debug"
    # Handle the case in which there is a new connection recieved through server_socket
    sockfd, addr = server_socket.accept()
    connection.addSocket(sockfd)
    print "Client (%s, %s) connected" % addr     
    connection.broadcast(sockfd, "[%s:%s] entered room\n" % addr)


if __name__ == "__main__":
    main()