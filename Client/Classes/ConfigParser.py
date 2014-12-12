class ConfigParser:
    """
    Configuration Parser Class
    @copyright: Northeastern University Crew 2014
    """

    @staticmethod
    def readConfig():
        """
        Reads the contents of PIE.conf
        @return: User-specified Configuration
        @rtype: Dict
        """
        config = open("Configs/PIE.conf", "r")
        configContents = config.read()
        configDict = {}
        for line in configContents.splitlines():
            if not (line.startswith("[") or line == ""):
                pair = ConfigParser.getPair(line)
                configDict[pair[0]] = pair[1]
        return configDict

    @staticmethod
    def getPair(line):
        """
        Parses the given configuration file
        line into a tuple.
        @param line: The line to parse
        @type line: String
        @return: Tuple of the form (key, value)
        @rtype: Tuple
        """
        split = line.replace(" ", "").split("=")
        if len(split) != 2:
            raise Exception("Bad config file...")
        return split[0], split[1]

