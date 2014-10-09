import json

# Slide Class Definition
# PARAMETERS
# 	| <String> url: The url to load when displaying the slide
# 	| <Integer> duration: The length of time to display the slide, in seconds
# 	| <Function> action: (optional) Action associated with the slide (NFC? :o)

# (c) Northeastern University Crew 2014
class Slide():
	def __init__(self, url, duration, action="None"):
		"""

		:param url: String
		:param duration: Integer
		:param action: Function
		"""
		self.__type__ = "slide"
		self.url = url
		self.duration = duration
		self.action = action

	def toJSON(self):
		text = json.dumps(self.__dict__)
		return text
