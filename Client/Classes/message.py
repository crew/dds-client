import json


# TODO: See doctring below
class Message:
    """"
    A message object to be passed between threads via Queue
    I{Sample Usage}:
    Making a new message that will send terminate from main to display:
    C{newMessage = Message("Main", "Display", "Terminate", \{\})}
    Making a slide that will update Display with a new slide:
    C{newMessage = Message("Main", "Display", "Update", \{\})}
    C{newMessage.add_content("slide1", "http://google.com")}

    @attention: It is good practice to use dict accessors as opposed to object attributes
    @todo: Un-expose attributes
    @ivar src: Name of the thread who sent the message
    @type src: String
    @ivar dest: Intended message destination
    @type dest: String
    @ivar pluginDest: Client-side plugin to receive the message
    @type pluginDest: String
    @ivar action: Action for the client-side plugin to perform
    @type action: String
    @ivar content: Message payload (destination plugin should be able to interpret content)
    @type content: Dictionary
    @ivar datetime: Message timestamp
    @type datetime: String
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self, src, dest, pluginDest, action, content, datetime=None):
        """
        Message Constructor
        @param src: Name of the thread who sent the message
        @type src: String
        @param dest: Intended message destination
        @type dest: String
        @param pluginDest: Client-side plugin to receive the message
        @type pluginDest: String
        @param action: Action for the client-side plugin to perform
        @type action: String
        @param content: Message payload (destination plugin should be able to interpret content)
        @type content: Dictionary
        @param datetime: Message timestamp
        @type datetime: String
        @return: Message with the given parameters
        @rtype: Message
        """
        self.src = src
        self.dest = dest
        self.pluginDest = pluginDest
        self.action = action
        self.content = content
        self.datetime = datetime

    def add_content(self, key, val):
        """
        Sets the given key-value pair to the message's content
        @param key: Key to write to in message content
        @param val: Value to write in message content
        @return: None
        """
        self.content[key] = val

    def toJSON(self):
        """
        Returns the message in JSON format
        @return: JSON representation of Message
        @rtype: String
        """
        text = json.dumps(self.__dict__)
        return text

    # TODO: (See docstring)
    def __str__(self):
        """
        @return: String Representation of Message
        @rtype: String
        @todo: This looks horrendous. We should pretty it up.
        """
        return "Src = " + self.src + " dest = " + self.dest + " pluginDest = " + self.pluginDest + \
               " action = " + self.action + " content = " + self.content + " datetime = " + self.datetime

    @staticmethod
    def fromJSON(jsonObj):
        """
        Creates a message from JSON input
        @param jsonObj: A Parsed JSON Input
        @type jsonObj: Dictionary
        @return: Message represented by the given JSON
        @rtype: Message
        """
        src = jsonObj['src']
        dest = jsonObj['dest']
        pluginDest = jsonObj['pluginDest']
        action = jsonObj['action']
        content = jsonObj['content']
        datetime = None
        if "datetime" in jsonObj:
            datetime = jsonObj["datetime"]
        return Message(src, dest, pluginDest, action, content, datetime)

    def __getitem__(self, item):
        """
        Implements dict-like behavior for Messages
        @param item: Message value to fetch
        @return: The attribute associated with the given key
        """
        if item == "src":
            return self.src
        elif item == "dest":
            return self.dest
        elif item == "pluginDest":
            return self.pluginDest
        elif item == "action":
            return self.action
        elif item == "content":
            return self.content
        elif item == "datetime":
            return self.datetime
        raise Exception("Message does not have an attribute \"" + item + "\"")