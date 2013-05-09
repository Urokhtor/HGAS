from collections import deque
from os import listdir
"""
    Naga Automation Suite - an automation system for home gardens
    Copyright (C) 2013  Jere Teittinen
    
    Author: Jere Teittinen <j.teittinen@luukku.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from time import sleep, strftime
from datetime import datetime
from queue import Queue
from threading import Thread

class Logging:
    """
        This class handles logging all the data from webUI and Arduino(s) and then fetching the logged data
        back to the webUI.
    """
    
    def __init__(self, parent):
        self.parent = parent # Needed to access device manager.
        self.inputQueue = Queue() # Needed to receive messages from Arduino through Connection module.
        
        self.messageThread = Thread(target = self.parseMessage).start()
        
    def getFiles(self):
        """
            Returns a list of files that exist.
        """
    
        return listdir("Logs/")
        
    def getFileData(self, file):
        """
            Returns the data stored in a file.
        """
        tmp = []
        
        for line in reversed(open("Logs/" + file, "r").readlines()):
            try:
                day, time, value = line.split(",")
                tmp.append((day, time, value))
            
            except:
                pass
        
        return tmp
    
    def getSensorReading(self, sensor):
        """
            Sends a request to get the reading for one sensor supplied as the parameter.
        """
        
        self.parent.connection.send((sensor["clientname"], self.parent.protocol.readSensor(sensor["index"])))
    
    def getSensorReadings(self, params):
        """
            Loops through all the sensors and polls their reading separately.
        """
        
        for sensor in self.parent.config.getItem("sensors", ""):
            self.getSensorReading(sensor)
    
    def getEventLogLatestMessages(self):
        """
            Returns the defined number of lines from eventlog.
        """
        
        tmp = []
        linesToRead = self.parent.config.getItem("eventloglength", 40)
        
        for line in reversed(open("Logs/eventlog.csv", "r").readlines()):
            try:
                day, time, text = line.split(",", 2)
                tmp.append("[" + day + " " + time + "] " + text)
                
                if len(tmp) == linesToRead:
                    break
                
            except:
                pass
                
        return tmp
            
    def parseMessage(self):
        """
            Polls for incoming messages and then logs them down accordingly, also handles updating sensor and
            device objects (last reading, last update and isrunning for example).
            
            In future it should be figured out how to make it possible for this thread to return messages to
            functions that sent commands to Arduino(s). This would be important for the webUI so for example
            a command "turn on device" could also inform the user that the action was successful instead of making
            the user check it from eventlog.
        """
        
        while True:
            line = []
            
            if not self.inputQueue.empty():
                line = self.inputQueue.get().split(" ")
            
            if line:
                try:
                    # Handle logging sensor data.
                    if line[0] == self.parent.protocol.read and len(line) > 1:
                        if line[1] == self.parent.protocol.sensor and len(line) > 2:
                            sensors = self.parent.config.getItem("sensors", "")
                            sensor = None
                            
                            for _sensor in sensors:
                                if _sensor["index"] == ord(line[2]):
                                    sensor = _sensor
                                    break
                            
                            if not sensor:
                                self.logEvent("Received message: Couldn't find sensor at index " + str(ord(line[2])), "red")
                                continue
                                
                            file = "Logs/" + sensor["name"] + "-" + str(sensor["index"]) + "-" + sensor["type"] + ".csv"
                            now = datetime.now()
                            
                            if len(line) > 3:
                                sensor["lastreading"] = line[3]
                                sensor["lastupdated"] = str(now.day) + "." + str(now.month) + "." + str(now.year) + " " + strftime("%H:%M:%S")
                                self.parent.config.setItem("sensors", sensors)
                                f = open(file, "a")
                                f.write(str(now.day) + "." + str(now.month) + "." + str(now.year) + "," + strftime("%H:%M:%S") + "," + line[3] + "\n")
                                f.close()
                                
                            else:
                                self.logEvent("Received message: Error logging sensor data with index: " + str(ord(line[2])) + " No reading received", "red")
                        else:
                            self.logEvent("Received message: Couldn't find sensor", "red")
                
                    #else:
                    #    self.logEvent("Received an incomplete response for action READ: No index returned")
                    
                    # Handle write to device events.
                    elif line[0] == self.parent.protocol._write and len(line) > 1:
                        if line[1] == self.parent.protocol.pump and len(line) > 2:
                            devices = self.parent.config.getItem("devices", "")
                            device = None
                            
                            for _device in devices:
                                if _device["index"] == ord(line[2]):
                                    device = _device
                                    break
                            
                            if not device:
                                self.logEvent("Received message: Couldn't find device at index " + str(ord(line[2])), "red")
                                continue
                                
                            if line[3] == self.parent.protocol.failed:
                                self.logEvent("Received message: Failed controlling pump at index: " + str(ord(line[2])), "red")
                                
                            elif line[3] == self.parent.protocol.enable:
                                device["isrunning"] = True
                                self.logEvent("Received message: Started pump at index: " + str(ord(line[2])), "green")
                            
                            elif line[3] == self.parent.protocol.disable:
                                device["isrunning"] = False
                                self.logEvent("Received message: Stopped pump at index: " + str(ord(line[2])), "green")
                            
                            else:
                                self.logEvent("Received message: Couldn't find pump at index: " + str(ord(line[2])), "red")
                                
                            self.parent.config.setItem("devices", devices)
                            
                        elif line[1] == self.parent.protocol.device and len(line) > 2:
                            devices = self.parent.config.getItem("devices", "")
                            device = None
                            
                            for _device in devices:
                                if _device["index"] == ord(line[2]):
                                    device = _device
                                    break
                            
                            if not device:
                                self.logEvent("Received message: Couldn't find device at index " + str(ord(line[2])), "red")
                                continue
                            
                            if len(line) < 4:
                                self.logEvent("Received message: Controlled device at index: " + str(ord(line[2])), "green")
                                
                            elif line[3] == self.parent.protocol.failed:
                                self.logEvent("Received message: Failed controlling device at index: " + str(ord(line[2])), "red")
                                
                            elif line[3] == self.parent.protocol.enable:
                                device["isrunning"] = True
                                self.logEvent("Received message: Started device at index: " + str(ord(line[2])), "green")
                            
                            elif line[3] == self.parent.protocol.disable:
                                device["isrunning"] = False
                                self.logEvent("Received message: Stopped device at index: " + str(ord(line[2])), "green")
                    
                            self.parent.config.setItem("devices", devices)
                            
                        else:
                            self.logEvent("Couldn't find device", "red")
                        
                    #else:
                    #    self.logEvent("Received an incomplete response for action WRITE: No index returned")
                            
                    # Insert device event.
                    elif line[0] == self.parent.protocol.insert and len(line) > 1:
                        if line[1] == self.parent.protocol.sensor and len(line) > 2:
                            sensors = self.parent.config.getItem("sensors", "")
                            sensor = None
                            
                            for _sensor in sensors:
                                if _sensor["index"] == ord(line[2]):
                                    sensor = _sensor
                                    break
                            
                            if not sensor:
                                self.logEvent("Received message: Couldn't find sensor at index " + str(ord(line[2])), "red")
                                continue
                            
                            self.logEvent("Received message: Added sensor at port " + str(ord(line[2])), "green")
                            
                        elif line[1] == self.parent.protocol.pump and len(line) > 2:
                            devices = self.parent.config.getItem("devices", "")
                            device = None
                            
                            for _device in devices:
                                if _device["index"] == ord(line[2]):
                                    device = _device
                                    break
                            
                            if not device:
                                self.logEvent("Received message: Couldn't find device at index " + str(ord(line[2])), "red")
                                continue
                                
                            self.logEvent("Received message: Added pump device at port " + str(ord(line[2])), "green")
                        
                        elif line[1] == self.parent.protocol.device and len(line) > 2:
                            devices = self.parent.config.getItem("devices", "")
                            device = None
                            
                            for _device in devices:
                                if _device["index"] == ord(line[2]):
                                    device = _device
                                    break
                            
                            if not device:
                                self.logEvent("Received message: Couldn't find device at index " + str(ord(line[2])), "red")
                                continue
                            
                            self.logEvent("Received message: Added device at port " + str(ord(line[2])), "green")

                        else:
                            self.logEvent("Received message: Failed to locate device", "red")
                        
                    # Modify device event.
                    elif line[0] == self.parent.protocol.modify and len(line) > 1:
                        if self.parent.deviceManager.hasPumpDeviceByIndex(ord(line[2])) or self.parent.deviceManager.hasDeviceByIndex(ord(line[2])):
                            self.logEvent("Received message: Found device", "green")
                        
                        else:
                            self.logEvent("Received message: Failed to locate device", "red")
                    
                    else:
                        self.logEvent("Received message: Didn't recognise message: " + "".join(line), "red")
                    
                except Exception as e:
                    self.logEvent("Received message: Thread encountered an error: " + str(e), "red")
                    continue
                    
            sleep(0.2)
            
    def logEvent(self, message, colour = "black"):
        """
            The standard logger function which takes the message as an argument and writes it to the
            event log.
        """
        
        text = '<span style="color:' + colour + '">' + message + '</span>'
        
        try:
            file = "Logs/eventlog.csv"
            now = datetime.now()
            
            f = open(file, mode="a")
            
            f.write(str(now.day) + "." + str(now.month) + "." + str(now.year) + "," + strftime("%H:%M:%S") + "," + text + "\n")
            f.close()
            
            if self.parent.config.getItem("verbose", True):
                print("[" + strftime("%H:%M:%S") + "] " + message) # Debug code. Add handling to the Config module so this can be made optional.
        
        except:
            pass
            