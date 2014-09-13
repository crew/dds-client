#!/usr/bin/python
# Tcp Chat server
 
import socket, select, json
 


#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message , CONNECTION_LIST, server_socket):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
    return CONNECTION_LIST

def connect(currentMessage, pieMap, sock):
    pie = currentMessage["content"]["name"] 
    pieMap[pie] = sock
    return pieMap


def main():
    #Function mapping
    functions = {}
    functions["connect"] = connect 

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    # Map of the Pies
    pieMap = {}

    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                print sockfd
                print addr
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                 
                CONNECTION_LIST = broadcast_data(sockfd, "[%s:%s] entered room\n" % addr, CONNECTION_LIST, server_socket)
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                #try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    print data
                    currentMessage = json.loads(data)
                    pieMap = functions[currentMessage["action"]](currentMessage, pieMap, sock)
#                    CONNECTION_LIST = broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data, CONNECTION_LIST, server_socket)                
                 
               #except:
                #    CONNECTION_LIST = broadcast_data(sock, "Client (%s, %s) is offline" % addr, CONNECTION_LIST, server_socket)
                #    print "Client (%s, %s) is offline" % addr
                #    sock.close()
                #    CONNECTION_LIST.remove(sock)
                #    continue
     
    server_socket.close()

if __name__ == "__main__":
    main()