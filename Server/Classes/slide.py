import json


class Slide():
    """
    Class for Slide Show Slide Objects
    @var url: The Slide's URL
    @type url: String
    @var duration: The Duration to show the slide (in seconds)
    @type duration: Integer
    @var id: The Slide's ID
    @type id: Integer
    @var meta: The Slide's meta content
    @type meta: Dictionary
    @copyright: Northeastern University Crew 2014
    """

    @staticmethod
    def makeSlide(url, duration, id, meta):
        """
        Slide Constructor based on the given input (instead of a dictionary)
        @param url: The Slide's URL
        @type url: String
        @param duration: The Duration to show the slide (in seconds)
        @type duration: Integer
        @param id: The Slide's ID
        @type id: Integer
        @param meta: The Slide's meta content
        @type meta: Dictionary
        @return: The constructed Slide
        @rtype: Slide
        """
        return Slide({"permalink": url, "duration": duration, "ID": id, "meta": meta})

    def __init__(self, infoDict):
        """
        Slide Constructor
        @param infoDict: The relevant information for the slide
        @type infoDict: Dictionary
        @return: The constructed Slide
        @rtype: Slide
        """
        self.__type__ = "slide"
        print "Got meta:", infoDict["meta"]
        self.url = infoDict["permalink"]
        if (not (isinstance(infoDict["meta"], str)) and
                (infoDict["meta"]["dds_external_url"][0] != "")):
            self.url = infoDict["meta"]["dds_external_url"][0]

        self.duration = infoDict["duration"]
        self.id = infoDict["ID"]
        self.meta = infoDict["meta"]

    def toJSON(self):
        """
        @return: A JSON Representation of the slide
        @rtype: String
        """
        text = json.dumps(self.__dict__)
        return text

    def sameID(self, id):
        """
        Predicate method which checks if the given id is equal to the slide's
        @param id: The id to check
        @type id: Integer
        @return: Whether the id matches the slide's
        @rtype: Boolean
        @todo: Do we I{really} need a method for this?
        """
        return self.id == id

    def __str__(self):
        return "Slide[url=" + str(self.url) + ", duration=" + str(self.duration) + ", id=" + str(
            self.id) + ", meta=" + str(self.meta) + "]"

    def __repr__(self):
        # Simplified output (Shown when Arrays of Slides are Printed)
        return "Slide(" + str(self.url) + "," + str(self.duration) + ")"
