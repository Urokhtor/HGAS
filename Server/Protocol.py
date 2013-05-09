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
        self.highThreshold = "h"
        self.lowThreshold = "l"
        self.type = "t"
        self.index = "i"
        self.failed = "f"
        
        # Sensor types
        self.default = 48
        self.temperature = 49
        self.DHT11 = 50
        self.SR04 = 51
        
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
        
        if type == "hygrometer": type = self.default
        elif type == "temp": type = self.temperature
        elif type == "humidity": type = self.DHT11
        elif type == "ultrasound": type = self.SR04
        
        if highThreshold == -1024:
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
    