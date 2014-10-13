class ConfigParser:
	@staticmethod
	def readConfig():
		config  = open("Configs/PIE.conf", "r")
		configContents = config.read()
		configDict = {}
		for line in configContents.splitlines():
			if not (line.startswith("[") or line == ""):
				pair = ConfigParser.getPair(line)
				configDict[pair[0]]=pair[1]
		return configDict
	@staticmethod
	def getPair(line):
		split = line.replace(" ","").split("=")
		if len(split) != 2:
			raise Exception("Bad config file...")
		return (split[0], split[1])
