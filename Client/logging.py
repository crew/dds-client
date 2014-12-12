import threading


class Logger:
    """
    A Thread-Safe Logging Class
    @todo: Modify to use syslog instead of these log files
    @copyright: Northeastern University Crew 2014
    """

    def __init__(self, threshold):
        """
        Logger Constructor
        @param threshold: The amount of messages to store in a buffer
                            before writing to a logfile
        @type threshold: Integer
        @return: The Constructed Logger
        @rtype: Logger
        """
        self.__debug = []
        self.__debugLock = threading.Lock()
        self.__warning = []
        self.__warningLock = threading.Lock()
        self.__error = []
        self.__errorLock = threading.Lock()
        self.__threshold = threshold

    def __addDebugMsg(self, msg):
        self.__debug.append(msg)
        if len(self.__debug) > self.__threshold:
            self.__writeAllAndClear(self.__debug, open("./debug.txt", "a+"), self.__debugLock)

    def __addWarningMessage(self, msg):
        self.__warning.append(msg)
        if len(self.__warning) > self.__threshold:
            self.__writeAllAndClear(self.__warning, open("./warning.txt", "a+"), self.__warningLock)

    def __addErrorMessage(self, msg):
        self.__error.append(msg)
        if len(self.__error) > self.__threshold:
            self.__writeAllAndClear(self.__error, open("./error.txt", "a+"), self.__errorLock)

    def __writeAllAndClear(self, list, file, lock):
        lock.acquire(True)
        for msg in list:
            file.write(msg + "\n")
        file.close()
        lock.release()
        del list[:]

    @staticmethod
    def log(level, msg):
        """
        Logs the given message with the given Log Level
        @param level: The given Log Level. ( "DEBUG" | "WARNING" | "ERROR" )
        @type level: String
        @param msg: The message to log
        @type msg: String
        @return:
        """
        if instance is None:
            raise Exception("Logging instance was never created")
        if level == "DEBUG":
            instance.__addDebugMsg(msg)
        elif level == "WARNING":
            instance.__addWarningMessage(msg)
        elif level == "ERROR":
            instance.__addErrorMessage(msg)

# Initialize the Logger
instance = Logger(15)