import json
# Slide Class Definition
# PARAMETERS
# 	| <String> url: The url to load when displaying the slide
# 	| <Integer> duration: The length of time to display the slide, in seconds
# 	| <Function> action: (optional) Action associated with the slide (NFC? :o)

# (c) Northeastern University Crew 2014
class Slide():
	@staticmethod
	def makeSlide(url, duration, id, meta):
		return Slide({"permalink" : url, "duration" : duration, "ID" : id, "meta" : meta})
		
	def __init__ (self, infoDict):
		self.__type__ = "slide"
		print "Got meta:",infoDict["meta"]
		self.url = infoDict["permalink"]
		if (not(isinstance(infoDict["meta"],str)) and 
			(infoDict["meta"]["dds_external_url"][0] != "")):
			
			self.url = infoDict["meta"]["dds_external_url"][0]

		self.duration = infoDict["duration"]
		self.id = infoDict["ID"]
		self.meta = infoDict["meta"]

	def toJSON(self):
		text = json.dumps(self.__dict__)
		return text
		
	def sameID(self, id):
		return self.id == id
		
	def __str__(self):
		return "Slide[url="+str(self.url)+", duration="+str(self.duration)+", id="+str(self.id)+", meta="+str(self.meta)+"]"
