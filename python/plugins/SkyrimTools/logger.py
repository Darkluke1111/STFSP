


from mimetypes import init


modes = {"ERROR": 0, "WARN":  1, "INFO": 2, "DEBUG": 3}
instance = None


def INSTANCE():
    global instance
    if not instance:
        instance = Logger()
    return instance

class Logger():

    def __init__(self, prefix: str = "", mode: str = "DEBUG") -> None:
        self.prefix = prefix
        self.mode = mode
    
    def log(self, level, msg):
        if not msg:
            msg = "NULL VALUE"
        if modes[level] <= modes[self.mode]:
            print(self.prefix + "[" + level + "] " + msg)

    def logDebug(self, msg):
        self.log("DEBUG",msg)

    def logInfo(self, msg):
        self.log("INFO",msg)

    def logWarning(self, msg):
        self.log("WARN",msg)

    def logError(self, msg):
        self.log("ERROR",msg)

    def setMode(self, mode):
        self.mode =  mode

    def setPrefix(self, prefix):
        self.prefix =  prefix