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

    def __init__(self, parent):
        self.parent = parent

    def createHeader(self, object, message):
        # get clientid and client type
        document = {}
        document["message"] = message

        if object is not None:
            client = self.parent.clientManager.getById(object["clientid"])
            document["protocol"] = client["type"]
            document["clientid"] = client["id"]

        return document

    def readSensor(self, sensor):
        """
            Tell Arduino to get sensor's reading and send it back to the server.
        """
        
        message = {}
        client = self.parent.clientManager.getById(sensor["clientid"])

        if client is None: return None # Return some error

        if client["type"] == CLIENT_TYPE_ARDUINO:
            message[KEY_COMMAND] = SEND_READ
            message[KEY_ID] = sensor["id"]
            message[KEY_INDEX] = sensor["index"]

        elif client["type"] == CLIENT_TYPE_TELLDUS:
            message["method"] = "sensor/info"
            message["params"] = {"id": sensor["telldusid"]}
        
        return self.createHeader(sensor, message)
    
    def write(self, device):
        """
            Toggle device state. Not for sensors.
        """
        
        message = {}
        client = self.parent.clientManager.getById(device["clientid"])

        if client is None: return None # Return some error

        if client["type"] == CLIENT_TYPE_ARDUINO:
            message[KEY_COMMAND] = SEND_WRITE
            message[KEY_ID] = device["id"]
            message[KEY_INDEX] = device["index"]

        elif client["type"] == CLIENT_TYPE_TELLDUS:
            if device["state"] == DEVICE_STATE_OFF: message["method"] = "device/turnOn"
            else: message["method"] = "device/turnOff"
            message["params"] = {"id": device["telldusid"]}
        
        return self.createHeader(device, message)
        
    def writeEnable(self, device):
        """
            Enable a device at index. Not for sensors. NOT SUPPORTED YET!
        """
        
        message = {}
        client = self.parent.clientManager.getById(device["clientid"])

        if client is None: return None # Return some error

        if client["type"] == CLIENT_TYPE_ARDUINO:
            message[KEY_COMMAND] = SEND_ENABLE
            message[KEY_ID] = device["id"]
            message[KEY_INDEX] = device["index"]

        elif client["type"] == CLIENT_TYPE_TELLDUS:
            message["method"] = "device/turnOn"
            message["params"] = {"id": device["telldusid"]}
        
        return self.createHeader(device, message)
    
    def writeDisable(self, device):
        """
            Disable a device at index. Not for sensors. NOT SUPPORTED YET!
        """
        
        message = {}
        client = self.parent.clientManager.getById(device["clientid"])

        if client is None: return None # Return some error

        if client["type"] == CLIENT_TYPE_ARDUINO:
            message[KEY_COMMAND] = SEND_DISABLE
            message[KEY_ID] = device["id"]
            message[KEY_INDEX] = device["index"]

        elif client["type"] == CLIENT_TYPE_TELLDUS:
            message["method"] = "device/turnOff"
            message["params"] = {"id": device["telldusid"]}
        
        return self.createHeader(device, message)

    def writeDim(self, device, value):

        message = {}
        client = self.parent.clientManager.getById(device["clientid"])

        if client is None: return None # Return some error
        message["method"] = "device/dim"
        message["params"] = {"id": device["telldusid"], "level": value}

        return self.createHeader(device, message)

        
    def insert(self, device, type, isStartup = False):
        """
            Tells Arduino to insert a device.
        """

        if not type == TYPE_SENSOR and not type == TYPE_PUMP:
            return json.dumps('{"' + KEY_ERROR + '": ' + str(WRONG_TYPE_ERROR) + '}')
        
        message = {}
        
        message[KEY_COMMAND] = SEND_INSERT
        message[KEY_DEVICE_TYPE] = type
        message[KEY_IS_STARTUP] = isStartup
        
        if type == TYPE_SENSOR: self.parseSensor(message, device)
        elif type == TYPE_PUMP: self.parseDevice(message, device)
        
        return self.createHeader(device, message)

    def remove(self, device, type):
        """
            Tells Arduino to remove a device.
        """
        
        if not type == TYPE_SENSOR and not type == TYPE_PUMP:
            return json.dumps('{"' + KEY_ERROR + '": ' + str(WRONG_TYPE_ERROR) + '}')
        
        message = {}
        
        message[KEY_COMMAND] = SEND_REMOVE
        message[KEY_DEVICE_TYPE] = type
        
        if type == TYPE_SENSOR: self.parseSensor(message, device)
        elif type == TYPE_PUMP: self.parseDevice(message, device)
        
        return self.createHeader(device, message)

    def parseSensor(self, message, sensor):
        message[KEY_ID] = sensor["id"]
        message[KEY_INDEX] = sensor["index"]
        message[KEY_TYPE] = sensor["type"]
        
        if not "lowthreshold" in sensor: message[KEY_LOW_THRESHOLD] = -1024
        else: message[KEY_LOW_THRESHOLD] = sensor["lowthreshold"]
        
        if not "highthreshold" in sensor: message[KEY_HIGH_THRESHOLD] = -1024
        else: message[KEY_HIGH_THRESHOLD] = sensor["highthreshold"]
        
        
    def parseDevice(self, message, device):
        message[KEY_ID] = device["id"]
        message[KEY_INDEX] = device["index"]
        message[KEY_MAX_ON_TIME] = device["maxontime"]
        message[KEY_USES_HYGROMETER] = device["useshygrometer"]
        message[KEY_HYGROMETER_INDEX] = device["hygrometerindex"]

    def getSensor(self, sensor):
        """
            This method creates message for getting latest device information for the Telldus device with given ID.
        """

        message = {}
        client = self.parent.clientManager.getById(sensor["clientid"])

        if client is None: return None # Return some error

        message["method"] = "sensor/info"
        message["params"] = {"id": sensor["telldusid"]}

        return self.createHeader(sensor, message)

    def getSensors(self, sensor):
        """
            This method creates message for getting latest device information for the Telldus device with given ID.
        """

        message = {}
        client = self.parent.clientManager.getById(sensor["clientid"])

        if client is None: return None # Return some error

        message["method"] = "sensors/list"
        message["params"] = ""

        return self.createHeader(sensor, message)

    def getDevice(self, device, methods = 3):
        """
            This method creates message for getting latest device information for the Telldus device with given ID.
        """

        message = {}
        client = self.parent.clientManager.getById(device["clientid"])

        if client is None: return None # Return some error

        message["method"] = "device/info"
        message["params"] = {"id": device["telldusid"], "supportedMethods": methods} # TODO: Is methods needed?

        return self.createHeader(device, message)

    def getDevices(self, device):
        """
            This method creates message for getting latest device information for the Telldus device with given ID.
        """

        message = {}
        client = self.parent.clientManager.getById(device["clientid"])

        if client is None: return None # Return some error

        message["method"] = "devices/list"
        message["params"] = {"supportedMethods": 16} # TODO: Make this better.

        return self.createHeader(device, message)

