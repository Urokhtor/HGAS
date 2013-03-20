from collections import deque
from os import listdir
from time import strftime
from datetime import datetime
from queue import Queue

class Logging:
    """
        
    """
    
    def __init__(self, parent):
        self.parent = parent # Needed to access device manager.
        self.inputQueue = Queue() # Needed to receive messages from Arduino through Connection module.
    
    def parseMessage(self):
        """
            Polls for incoming messages and then logs them down accordingly.
        """
        
        line = []
        
        if not self.inputQueue.empty():
            line = self.inputQueue.get().split(" ")
        
        if line:
            
            # Handle logging sensor data.
            if line[0] == self.parent.protocol.read:
                if line[1] == self.parent.protocol.sensor and len(line) > 2:
                    if self.parent.deviceManager.hasSensorDeviceByIndex(ord(line[2])):
                        device = self.parent.deviceManager.getSensorDeviceByIndex(ord(line[2]))
                        file = "Logs/" + self.parent.deviceManager.getSensorDeviceNameByIndex(device.getIndex()) + "-" + str(device.getIndex()) + "-" + str(device.getType()) + ".csv"
                        now = datetime.now()

                        f = open(file, "a")
                        f.write(str(now.day) + "." + str(now.month) + "." + str(now.year) + "," + strftime("%H:%M:%S") + "," + line[3] + "\n")
                        f.close()
            
                    else:
                        self.logEvent("Couldn't find sensor with index: " + str(ord(line[2])))
            
                else:
                    self.logEvent("Received an incomplete response for action READ: No index returned")
            
            # Handle write to device events.
            elif line[0] == self.parent.protocol._write:
                if line[1] == self.parent.protocol.pump and len(line) > 2:
                    if self.parent.deviceManager.hasPumpDeviceByIndex(ord(line[2])):
                        if line[3] == self.parent.protocol.failed:
                            self.logEvent("Failed controlling pump at index: " + str(ord(line[2])))
                            
                        elif line[3] == self.parent.protocol.enable:
                            self.logEvent("Started pump at index: " + str(ord(line[2])))
                        
                        elif line[3] == self.parent.protocol.disable:
                            self.logEvent("Stopped pump at index: " + str(ord(line[2])))
                    
                    else:
                        self.logEvent("Couldn't find pump at index: " + str(ord(line[2])))
                        
                elif line[1] == self.parent.protocol.device and len(line) > 2:
                    if self.parent.deviceManager.hasDeviceByIndex(ord(line[2])):
                        if line[3] == self.parent.protocol.failed:
                            self.logEvent("Failed controlling device at index: " + str(ord(line[2])))
                            
                        elif line[3] == self.parent.protocol.enable:
                            self.logEvent("Started device at index: " + str(ord(line[2])))
                        
                        elif line[3] == self.parent.protocol.disable:
                            self.logEvent("Stopped device at index: " + str(ord(line[2])))
                
                    else:
                        self.logEvent("Couldn't find device at index: " + str(ord(line[2])))
                
                else:
                    self.logEvent("Received an incomplete response for action WRITE: No index returned")
                    
            # Insert device event.
            elif line[0] == self.parent.protocol.insert:
                if self.parent.deviceManager.hasPumpDeviceByIndex(ord(line[2])) or self.parent.deviceManager.hasDeviceByIndex(ord(line[2])):
                    self.logEvent("Found device")
                
                else:
                    self.logEvent("Failed to locate device")
            
            # Modify device event.
            elif line[0] == self.parent.protocol.modify:
                if self.parent.deviceManager.hasPumpDeviceByIndex(ord(line[2])) or self.parent.deviceManager.hasDeviceByIndex(ord(line[2])):
                    self.logEvent("Found device")
                
                else:
                    self.logEvent("Failed to locate device")
            
            else:
                self.logEvent("Didn't recognise message: " + "".join(line))
            
    def logEvent(self, message):
        """
            The standard logger function which takes the message as an argument and writes it to the
            event log.
        """
        
        file = "Logs/eventlog.csv"
        now = datetime.now()
        
        f = open(file, mode="a")
        
        f.write(str(now.day) + "." + str(now.month) + "." + str(now.year) + "," + strftime("%H:%M:%S") + "," + message + "\n")
        f.close()
        print("[" + strftime("%H:%M:%S") + "] " + message) # Debug code. Add handling to the Config module so this can be made optional.