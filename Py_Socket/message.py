import json

class Message:
    """"A message object to be passed between threads via Queue"""
    def __init__(self, src, dest, action, content):
        """src is the name of the thread, dest is the goal thread, action is a string that can run a function, content is a dictionary"""
        self.src = src
        self.dest = dest
        self.action = action
        self.content = content

    def add_content(self, key, val):
        self.content[key] = val
    
    def toJSON(self):
    	text = json.dumps(self.__dict__)
    	return text
