import json

class Message:
    """"A message object to be passed between threads via Queue"""
#src is the name of the src for this message
#dest is the name of the pie || server
#pluginDest is the name of the plugin that this message should be distributed to
#action is the function that the destPlugin should run
#content is the payload of this message, the plugin should know how to interpret the content of this message
    def __init__(self, src, dest, pluginDest, action, content, datetime = None):
        """src is the name of the thread, dest is the goal thread, action is a string that can run a function, content is a dictionary"""
        self.src = src
        self.dest = dest
        self.pluginDest = pluginDest
        self.action = action
        self.content = content
	self.datetime = datetime

    def add_content(self, key, val):
        self.content[key] = val
    
    def toJSON(self):
    	text = json.dumps(self.__dict__)
    	return text

    def __str__(self):
        return "Src = "+self.src+" dest = "+self.dest+" pluginDest = "+self.pluginDest+" action = "+self.action+" content = "+self.content+" datetime = "+self.datetime
    @staticmethod
    def fromJSON(jsonObj):
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
    	raise Exception("Message does not have an attribute \""+item+"\"")
    	
""" Sample Messge Usage:
    Making a new message that will send terminate from main to display.
    
    newMessage = Message("Main", "Display", "Terminate", {})

    Making a slide that will update Display with a new slide.

    newMessage = Message("Main", "Display", "Update", {})
    newMessage.add_content("slide1", "http://google.com")"""
