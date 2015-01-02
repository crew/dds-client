#!/usr/bin/python

import socket
import select
import json
import thread

from Classes.socketlist import socketList
from Classes.message import Message
from WPHandler import wpListenerStart


def connect(**kwargs):
    """
    Handles any new connections
    @param kwargs: Needed information for the connection
    @type kwargs: Dictionary
    @return: The updated parameters of the parameters used to call it
    @rtype: Dictionary
    """
    pie = kwargs["currentMessage"]["src"]
    kwargs["connection"].mapPie(kwargs["sock"], pie)
    return kwargs


def main_socketServer_thread(inputQueue, Queues, runtimeVars):
    """
    Socket Server Primary Thread Function
    @param inputQueue: Socket server's message queue (Unused, included to conform to plugin thread API)
    @type inputQueue: Queue.Queue
    @param Queues: Global queue list
    @type Queues: QueueDict
    @param runtimeVars: User-defined configurations
    @type runtimeVars: Dictionary
    @return: None
    @rtype: NoneType
    @copyright: Northeastern University Crew 2014
    """
    # List to keep track of socket descriptors
    RECV_BUFFER = 4096  # Advisable to keep it as a power of 2
    PORT = int(runtimeVars["port"])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    connection = socketList(server_socket)
    connection.addSocket(server_socket)
    wpListenerStart(Queues["socketServer"])

    log(Queues["Logging"], "Socket server started on port " + str(PORT))
    thread.start_new_thread(socketServer, (connection, Queues, server_socket, RECV_BUFFER))

    while True:
        if not Queues["socketServer"].empty():
            log(Queues["Logging"], "Message in Queue")
            currentMessage = Queues["socketServer"].get()
            connection.sendMessage(connection.getSock(currentMessage.dest), currentMessage.toJSON() + "\v")


def socketServer(connection, Queues, server_socket, RECV_BUFFER):
    """
    The socket server implementation
    @param connection: The socketServer's socket connection
    @type connection: socketList
    @param Queues: The global list of queues
    @type Queues: QueueDict
    @param server_socket: The server's local socket
    @type server_socket: Socket
    @param RECV_BUFFER: The socket read buffer size
    @type RECV_BUFFER: Integer
    @return: None
    @rtype: NoneType
    """
    # Wrapper to log to Logging Queue
    write_log = lambda s: log(Queues["Logging"], str(s) + '\n')

    while True:
        write_log("pieMap: " + str(connection.pieMap))
        write_log("sockList: " + str(connection.sockList))
        read_sockets, write_sockets, error_sockets = select.select(connection.sockList, [], [])
        for sock in read_sockets:
            write_log(read_sockets)
            if sock == server_socket:
                # Handle the case in which there is a new connections
                # received through server_socket
                sockfd, addr = server_socket.accept()
                connection.addSocket(sockfd)
                write_log("Client Connected " + str(addr))
            else:
                data = sock.recv(RECV_BUFFER)
                write_log(data)
                if data == "":
                    write_log("No Data Received on Socket %s. Removing." % str(sock))
                    connection.removeSocket(sock)
                else:
                    messages = filter(lambda s: s != "",
                                      data.split('\v'))
                    for rawMessage in messages:
                        print rawMessage
                        currentMessage = json.loads(rawMessage)
                        if not currentMessage["pluginDest"] == "socketServer":
                            write_log("Placing message in destination: " + currentMessage["pluginDest"])
                            Queues[currentMessage["pluginDest"]].put(Message.fromJSON(currentMessage))
                        else:
                            write_log("Connecting")
                            connect(connection=connection, currentMessage=currentMessage, pieMap=connection.pieMap,
                                    sock=sock)
                            write_log("Finished connection...")


# TODO: Deal with the fact that we have multiple log() definitions across our codebase...
def log(queue, mes):
    """
    Logs the given message
    @param queue: The Logger's message queue
    @type queue: Queue.Queue
    @param mes: The message to log
    @return: None
    @rtype: None
    """
    newLog = Message("Socket", "Logging", "Logger", "log", {})
    newLog.add_content("1", mes)
    queue.put(newLog)
