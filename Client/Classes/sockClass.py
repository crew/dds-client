import socket
import time

from message import Message


class sockClass:
    """
    Client Socket class
    @ivar sock: The Socket's I/O socket
    @type sock: Socket
    @ivar hostIP: The Server's IP Address
    @type hostIP: String
    @ivar hostPort: The Server's Port
    @type hostPort: Integer
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self, runtimeVars):
        """
        Client Socket Constructor
        @param runtimeVars: User-defined configuration
        @return: The Constructed Client Socket
        @rtype: sockClass
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostIP = runtimeVars["server"]
        self.hostPort = int(runtimeVars["port"])
        self.connect(runtimeVars)

    def send(self, msg):
        """
        Sends the given message to the server
        @param msg: The message to send
        @type msg: String
        @return: None
        @rtype: NoneType
        """
        self.sock.send(msg)

    def connect(self, runtimeVars):
        """
        Connects the Client to the Server
        (Server configuration inside of Configs/PIE.conf)
        @param runtimeVars: User-defined configuration
        @return: None
        @rtype: NoneType
        """
        print "I'm connected: " + runtimeVars["name"]
        while True:
            try:
                self.sock.connect((self.hostIP, self.hostPort))
                print "Connected"
                break
            except:
                print 'Unable to connect'
                time.sleep(2)

        # Pass along PIE name to Grandma
        # TODO: Abstract to allow config setting of these parameters
        identify = Message(runtimeVars["name"], "Grandma", "socketServer", "connect", {})
        identify.add_content("name", runtimeVars["name"])
        self.sock.send(identify.toJSON())
