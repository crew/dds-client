import threading

# Takes a dict input and logs its contents to the syslog
'''def logging_thread(input_queue, Queues, runtimeVars):
    while True:
        if not input_queue.empty():
            currentMessage = input_queue.get()
            for key in currentMessage.content:
	        msg = "PIE: " + currentMessage.src + ": " + currentMessage.content[key]
		syslog.syslog(syslog.LOG_ERR, msg)

'''	
#a thread-safe logging class
#use Logger.log to log a message with the given priority
class Logger:
	instance = Logger(5)
	
	def __init__(self, threshold):
		self.debug = []
		self.debugLock = threading.Lock()
		self.warning = []
		self.warningLock = threading.Lock()
		self.error = []
		self.errorLock = threading.Lock()
		self.threshold = threshhold
	#In the future these can be modified to use syslog.syslog(PRIORITY, MESSAGE)
	#If we want to use syslog instead of our own logs (theirs might be faster)
	
	#All of the add*Message methods append the message to the required list and if the number
	#of messages if above threshhold they write all of them to file, in a threadsafe way.
	#and clear the message list.
	
	#Tried to make file I/O more effiecient through batch writes it may not matter
	#I don't know how python does the file writing (if it doesn't buffer the writes then it shouldn't matter)
	
	def addDebugMsg(self, msg):
		self.debug.append(msg)
		if len(self.debug) > self.threshold:
			writeAllAndClear(self.debug, open("debug.txt", "a"), self.debugLock)
		
	def addWarningMessage(self, msg):
		self.warning.append(msg)
		if len(self.warning) > self.threshhold:
			writeAllAndClear(self.warning, open("warning.txt", "a"), self.warningLock)
	
	def addErrorMessage(self, msg):
		self.error.append(msg)
		if len(self.error) > self.threshhold:
			writeAllAndClear(self.warning, open("error.txt", "a"), self.errorLock)
	
	def writeAllAndClear(list, file, lock):
		lock.aquire(true)
		for msg in list:
			file.write(msg+"\n")
		file.close()
		lock.release()
		del list[:]
			
		
	## Logging
	# Level is:
	# -DEBUG
	# -WARNING
	# -ERROR
	@staticmethod
	def log(level, msg):
		if instance == None:
			raise Exception("Logging instance was never created")
		if level == "DEBUG":
			instance.addDebugMsg(msg)
		elif level == "WARNING":
			instance.addWarningMessage(msg)
		elif level == "ERROR":
			instance.addErrorMessage(msg)
		
		
	
	

#	newLog = Message("Main", "Logging", "Logger" , "log", {})
#	newLog.add_content("1",mes)
#	queue.put(newLog)
