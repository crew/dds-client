import json

class Message:
    """"A message object to be passed between threads via Queue"""
#src is the name of the src for this message
#dest is the name of the pie || server
#pluginDest is the name of the plugin that this message should be distributed to
#action is the function that the destPlugin should run
#content is the payload of this message, the plugin should know how to interpret the content of this message
    def __init__(self, src, dest, pluginDest, action, content):
        """src is the name of the thread, dest is the goal thread, action is a string that can run a function, content is a dictionary"""
        self.src = src
        self.dest = dest
	self.pluginDest = pluginDest
        self.action = action
        self.content = content

    def add_content(self, key, val):
        self.content[key] = val
    
    def toJSON(self):
    	text = json.dumps(self.__dict__)
    	return text
    	
""" Sample Messge Usage:
    Making a new message that will send terminate from main to display.
    
    newMessage = Message("Main", "Display", "Terminate", {})

    Making a slide that will update Display with a new slide.

    newMessage = Message("Main", "Display", "Update", {})
    newMessage.add_content("slide1", "http://google.com")"""
