class Plugin:
    """
    Plugin Base Class
    """

    def needsThread(self):
        """
        Predicate method which asks whether the plugin's
            run() function requires threading
        @return: Whether the plugin needs a thread
        @rtype: Boolean
        """
        return False

    def run(self, runtimeVars):
        """
        The main function of the plugin. This is called
            after setup() by the main client function
        @param runtimeVars: Configuration provided in Configs/PIE.conf
        @return: None
        @rtype: NoneType
        """
        pass

    def setup(self, messageDict, runtimeVars):
        """
        Called during the client's initialization process
        @param messageDict: All of the Client's Plugins' Message Receivers
        @type messageDict: Dictionary
        @param runtimeVars: Configuration provided in Configs/PIE.conf
        @type runtimeVars: Dictionary
        """
        pass

    def getName(self):
        """
        @return: The Plugin's name
        @rtype: String
        """
        raise Exception("Abstract Plugin does not have a name")

    def addMessage(self, message):
        """
        Handler for incoming messages
        @param message: Received message
        @type message: String
        """
        raise Exception("Not implemented for Plugin")

    def __str__(self):
        return self.getName()


