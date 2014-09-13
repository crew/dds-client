class Message:
    """"A message object to be passed between threads via Queue"""
    def __init__(self, src, dest, content):
        """src is the name of the thread, dest is the goal thread, content is a dictionary"""
        self.src = src
        self.dest = dest
        self.content = content

    def add_content(self, key, val):
        self.content[key] = val
        
