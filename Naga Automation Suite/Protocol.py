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

import json
from Constants import *

class Protocol:
    """
        This class composes messages that are compliant to the communication protocol that
        Arduino code understands.
    """
        
    def readSensor(self, id, index):
        """
            Tell Arduino to get sensor's reading and send it back to the server.
        """
        
        tmp = {}
        
        tmp[KEY_COMMAND] = SEND_READ
        tmp[KEY_ID] = id
        tmp[KEY_INDEX] = index
        
        return json.dumps(tmp)
    
    def write(self, id, index):
        """
            Toggle device state. Not for sensors.
        """
        
        tmp = {}
        
        tmp[KEY_COMMAND] = SEND_WRITE
        tmp[KEY_ID] = id
        tmp[KEY_INDEX] = index
        
        return json.dumps(tmp)
        
    def writeEnable(self, id, index):
        """
            Enable a device at index. Not for sensors. NOT SUPPORTED YET!
        """
        
        tmp = {}
        
        tmp[KEY_COMMAND] = SEND_ENABLE
        tmp[KEY_ID] = id
        tmp[KEY_INDEX] = index
        
        return json.dumps(tmp)
    
    def writeDisable(self, id, index):
        """
            Disable a device at index. Not for sensors. NOT SUPPORTED YET!
        """
        
        tmp = {}
        
        tmp[KEY_COMMAND] = SEND_DISABLE
        tmp[KEY_ID] = id
        tmp[KEY_INDEX] = index
        
        return json.dumps(tmp)
        
    def insert(self, device, type, isStartup = False):
        """
            Tells Arduino to insert a device.
        """

        if not type == TYPE_SENSOR and not type == TYPE_PUMP:
            return json.dumps('{"' + KEY_ERROR + '": ' + str(WRONG_TYPE_ERROR) + '}')
        
        tmp = {}
        
        tmp[KEY_COMMAND] = SEND_INSERT
        tmp[KEY_DEVICE_TYPE] = type
        tmp[KEY_IS_STARTUP] = isStartup
        
        if type == TYPE_SENSOR: self.parseSensor(tmp, device)
        elif type == TYPE_PUMP: self.parseDevice(tmp, device)
        
        return json.dumps(tmp)

    def remove(self, device, type):
        """
            Tells Arduino to remove a device.
        """
        
        if not type == TYPE_SENSOR and not type == TYPE_PUMP:
            return json.dumps('{"' + KEY_ERROR + '": ' + str(WRONG_TYPE_ERROR) + '}')
        
        tmp = {}
        
        tmp[KEY_COMMAND] = SEND_REMOVE
        tmp[KEY_DEVICE_TYPE] = type
        
        if type == TYPE_SENSOR: self.parseSensor(tmp, device)
        elif type == TYPE_PUMP: self.parseDevice(tmp, device)
        
        return json.dumps(tmp)
    
    def freeMemory(self):
        """
        
        """
        
        tmp = {}
        
        tmp[KEY_COMMAND] = SEND_FREEMEMORY
        
        return json.dumps(tmp)

    def parseSensor(self, tmp, sensor):
        tmp[KEY_ID] = sensor["id"]
        tmp[KEY_INDEX] = sensor["index"]
        tmp[KEY_TYPE] = sensor["type"]
        
        if not "lowthreshold" in sensor: tmp[KEY_LOW_THRESHOLD] = -1024
        else: tmp[KEY_LOW_THRESHOLD] = sensor["lowthreshold"]
        
        if not "highthreshold" in sensor: tmp[KEY_HIGH_THRESHOLD] = -1024
        else: tmp[KEY_HIGH_THRESHOLD] = sensor["highthreshold"]
        
        
    def parseDevice(self, tmp, device):
        tmp[KEY_ID] = device["id"]
        tmp[KEY_INDEX] = device["index"]
        tmp[KEY_MAX_ON_TIME] = device["maxontime"]
        tmp[KEY_USES_HYGROMETER] = device["useshygrometer"]
        tmp[KEY_HYGROMETER_INDEX] = device["hygrometerindex"]
    