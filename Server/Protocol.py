class Protocol:
    """
        This class composes messages that are compliant to the communication protocol that
        Arduino code understands.
    """
    
    def __init__(self):
        """
            Definitions for the commands the protocol uses.
        """
        
        # First byte
        self._write = "w"
        self.read = "r"
        self.insert = "i"
        self.modify = "m"
        self._forceSetup = "f"
        self._setupStart = "{"
        self._setupEnd = "}"
        
        # Third byte, write only
        self.enable = "e"
        self.disable = "d"
        self.sensor = "s"
        self.pump = "p"
        self.device = "r"
        
        # Fourth byte, additional parameters
        self.remove = "r"
        self.highTreshold = "h"
        self.lowTreshold = "l"
        self.type = "t"
        self.index = "i"
        self.failed = "f"
        
        # Sensor types
        self.default = 0
        self.temperature = 1
        self.DHT11 = 2
        
    def readSensor(self, index):
        """
            Tell Arduino to get sensor's reading and send it back to the server.
        """
        
        return self.read + chr(index)
    
    def write(self, index):
        """
            Toggle device state. Not for sensors.
        """
        
        return self._write + chr(index)
        
    def writeEnable(self, index):
        """
            Enable a device at index. Not for sensors. NOT SUPPORTED YET!
        """
        return self._write + chr(index) + self.enable
    
    def writeDisable(self, index):
        """
            Disable a device at index. Not for sensors. NOT SUPPORTED YET!
        """
        
        return self._write + chr(index) + self.disable
        
    def insertSensor(self, index, type = 0, lowThreshold = -1024, highThreshold = -1024):
        """
            Tells Arduino to insert a sensor device.
        """
        
        if highTreshold == -1024:
            return self.insert + chr(index) + self.sensor + chr(type)
        
        elif lowThreshold != -1024 and highThreshold == -1024:
            return self.insert + chr(index) + self.sensor + chr(type) + str(len(str(lowThreshold))) + str(lowThreshold)
        
        else:
            return self.insert + chr(index) + self.sensor + chr(type) + str(len(str(lowThreshold))) + str(lowThreshold) + str(len(str(highThreshold))) + str(highThreshold)

    def insertPump(self, index, maxOnTime = 140, usesHygrometer = False, hygrometerIndex = -1):
        """
            Tells Arduino to insert a pump device.
        """
        
        if not usesHygrometer or (usesHygrometer and hygrometerIndex == -1):
            return self.insert + chr(index) + self.pump + str(len(str(maxOnTime))) + str(maxOnTime)
            
        else:
            return self.insert + chr(index) + self.pump + str(len(str(maxOnTime))) + str(maxOnTime) + chr(1) + chr(hygrometerIndex)
     
    def forceSetup(self):
        """
            DEPRECATED (I guess). Forces Arduino to take in setup instructions because normally starting
            setup wouldn't work if it has been already run.
        """
        
        return self._forceSetup
        
    def setupStart(self):
        """
            Tell Arduino to start expecting setup instructions.
        """
        
        return self._setupStart
        
    def setupEnd(self):
        """
            Tell Arduino not to expect any further setup instructions.
        """
        
        return self._setupEnd
    