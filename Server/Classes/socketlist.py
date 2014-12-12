class socketList:
    """
    Object responsible for keeping track of all socket connections

    @var pieMap: A dictionary mapping each connected Raspberry Pi to its socket
    @type pieMap: Dictionary
    @var sockList: List of live Socket Connections
    @type sockList: Array
    @var serverSocket: Represents the Server's Listening Socket
    @type serverSocket: Socket
    @see: Python C{socket} Documentation for socket info
    @warning: If you're writing a plugin, you I{probably} don't need
                to mess with this.
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self, serverSocket):
        """
        socketList Constructor
        @param serverSocket: The socket to use as the server socket
        @type serverSocket: Socket
        @return: A new empty SocketList with the given server socket
        @rtype: socketList
        """
        self.pieMap = {}
        self.sockList = []
        self.serverSocket = serverSocket

    def addSocket(self, sock):
        """
        Adds the given socket to the socketList
        @param sock: The socket to add
        @type sock: Socket
        @return: None
        @rtype: NoneType
        """
        self.sockList.append(sock)

    def mapPie(self, sock, pieName):
        """
        Maps the given Raspberry Pi to the given socket
        @param sock: The socket to map the Raspberry Pi to
        @type sock: Socket
        @param pieName: The name of the Raspberry Pi
        @type pieName: String
        @return: None
        @rtype: NoneType
        """
        print "mapping" + pieName
        self.pieMap[pieName] = sock

    def removeSocket(self, sock):
        """
        Removes the given socket to the socketList
        @param sock: The socket to remove
        @type sock: Socket
        @return: None
        @rtype: NoneType
        """
        print "\nGood bye, " + str(self.getPie(sock)) + "!\n"
        sock.close()
        self.sockList.remove(sock)
        self.pieMap.pop(self.getPie(sock))

    def broadcast(self, msg, sock=None):
        """
        Broadcasts the given message to every socket
            except the serverSocket and the socket provided
        @param msg: The message to broadcast
        @type msg: String
        @param sock: (Optional) The socket to exclude (e.g.
                        the socket from which the broadcast
                        originated)
        @type sock: Socket
        @return: None
        @rtype: NoneType
        """
        for socket in self.sockList:
            print(self.getPie(socket))
            if socket != self.serverSocket and socket != sock:
                self.sendMessage(socket, msg)

    def sendMessage(self, sock, msg):
        """
        Sends the given message to the given socket
        @param sock: The socket to receive the message
        @type sock: Socket
        @param msg: The message to send
        @type msg: String
        @return: None
        @rtype: NoneType
        """
        print "Sending"
        print "Message " + str(msg)
        try:
            sock.sendall(msg)
            print "Message sent!"
        except Exception as e:
            # Is caught if something goes wrong.
            # Print the exception and do
            # any needed cleanups for the socket
            print str(e)
            if sock:
                self.removeSocket(sock)

    def getSock(self, pie):
        """
        Returns the socket associated with the given
            Raspberry Pi name
        @param pie: The name of the Raspberry Pi whose socket to retrieve
        @type pie: String
        @return: The socket for the given Raspberry Pi
        @rtype: Socket
        """
        try:
            return self.pieMap[pie]
        except:
            print "Missing Pie:", pie

    def getPie(self, sock):
        """
        Returns the Raspberry Pi associated with the given socket
        @param sock: The socket whose Raspberry Pi to retrieve
        @type sock: Socket
        @return: The Raspberry Pi associated with the socket
        @rtype: String
        """
        print(len(self.pieMap))
        for pie, socket in self.pieMap.iteritems():
            if sock == socket:
                return pie