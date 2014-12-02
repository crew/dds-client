import json
# Slide Class Definition
# PARAMETERS
# 	| <String> url: The url to load when displaying the slide
# 	| <Integer> duration: The length of time to display the slide, in seconds
# 	| <Function> action: (optional) Action associated with the slide (NFC? :o)

# (c) Northeastern University Crew 2014
class Slide():
	def __init__(self, url, duration, id, meta = None):
		self.__type__ = "slide"
		self.url = url
		self.duration = duration
		self.id = id
		self.meta = meta
		
	def __init__(self, infoDict):
		self.__type__ = "slide"
		self.url = infoDict["Permalink"]
		self.duration = infoDict["Duration"]
		self.id = infoDict["ID"]
		self.meta = infoDict["meta"]

	def toJSON(self):
		text = json.dumps(self.__dict__)
		return text
		
	def sameID(self, id):
		return self.id == id
		
	def __str__(self):
		return "Slide[url="+str(self.url)+", duration="+str(self.duration)+", id="+str(self.id)+", meta="+self.meta+"]"
