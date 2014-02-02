__author__ = 'Urokhtor'

# -*- coding: utf-8 -*-

"""
    Naga Automation Suite - an automation system for home and garden that
    interfaces with Telldus Live!
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

import urllib, json
import http.client as httplib
import rauth
from Constants import *

class TelldusInterface:

    def __init__(self):
        self.serverAddress = "api.telldus.com:80"
        self.deviceMethods = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | TELLSTICK_DIM | TELLSTICK_UP | TELLSTICK_DOWN
        self.sensorMethods = TELLSTICK_TEMPERATURE | TELLSTICK_HUMIDITY

    def getConf(self):
        f = open("config.conf", "r")
        tmp = json.load(f)
        f.close()
        return tmp

    def request(self, method, params):
        header = ""

        try:
            conf = self.getConf()

            telldus = rauth.OAuth1Service(
                name = "telldus",
                consumer_key = conf["publicKey"],
                consumer_secret = conf["privateKey"],
                base_url = "http://api.telldus.com/json/" #+ method
            )

            session = telldus.get_auth_session(conf["token"], conf["tokenSecret"], method = "GET") #, data = params)
            response = session.get(method, params = params, verify = True)
            print(response)

            consumer = oauth.OAuthConsumer(conf["publicKey"], conf["privateKey"])
            token = oauth.OAuthToken(conf["token"], conf["tokenSecret"])
            oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_method="GET", http_url="http://api.telldus.com/json/" + method, parameters=params)
            oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
            headers = oauth_request.to_header()
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        except:
            return None

        try:
            conn = httplib.HTTPConnection(self.serverAddress)
            conn.request("GET", "/json/" + method + "?" + urllib.urlencode(params, True).replace("+", "%20"), headers=headers)

        except:
            return None

        try:
            response = conn.getresponse()
            return json.loads(response.read().decode("UTF-8"))

        except:
            return None

    def toggle(self, deviceID):
        device = self.getDevice(deviceID)

        if "error" in device:
            return device["error"]

        if not "state" in device:
            return "Couldn't get device state for given device"

        if int(device["state"]) & TELLSTICK_TURNON or int(device["state"]) & TELLSTICK_DIM:
            self.turnOff(deviceID)
            return "Toggled device off"

        elif int(device["state"]) & TELLSTICK_TURNOFF:
            self.turnOn(deviceID)
            return "Toggled device on"

    def turnOn(self, deviceID):
        return self.request("device/turnOn", {"id": deviceID})

    def turnOff(self, deviceID):
        return self.request("device/turnOff", {"id": deviceID})

    def dim(self, arguments):
        try:
            return self.request("device/dim", {"id": arguments[0], "level": arguments[1]})

        except:
            return None

    def bell(self, deviceID):
        return self.request("device/bell", {"id": deviceID})

    def controlDevice(self, deviceID, methodId, methodValue = 0):
        """
            Takes the ID of a device to be controlled and the method it should be controlled with
            (For example turn it on or off).
        """

        return self.request("device/command", {"id": deviceID, "method": methodId, "value": methodValue})

    def getDevice(self, deviceID, methods = 3):
        # Debug code, uses local database.

        from Config import Config
        config = Config("configuration.json")
        devices = config.getItem("devices", "")
        for device in devices:
            if device["id"] == deviceID:
                return device

        return None

        return self.request("device/info", {"id": deviceID, "supportedMethods": methods})

    def getDevices(self):
        """
            Fetches a list of devices in the system.
        """

        # Debug code, uses local database
        from Config import Config
        config = Config("configuration.json")
        devices = config.getItem("devices", "")

        if len(devices) > 0:
            return devices
        else: return None

        return self.request("devices/list", {"supportedMethods": self.deviceMethods})

    def getSensor(self, sensorID):
        """
            Sends a sensor info request to the Live! API with the wanted sensor"s index.
            Returns the sensor data received.
        """

        from Config import Config
        config = Config("configuration.json")
        sensorinfo = config.getItem("sensorinfo", "")

        for sensor in sensorinfo:
            if sensor["id"] == sensorID:
                return sensor


        # Debug code, uses local database
        if sensorID == "174963":
            response = {u'ignored': 0, u'protocol': u'oregon', u'name': u'Kasvari - l\xe4mmin puoli', u'editable': 1, u'lastUpdated': 1365097299, u'timezoneoffset': 10800, u'sensorId': u'139', u'data': [{u'name': u'temp', u'value': u'2.3'}, {u'name': u'humidity', u'value': u'87'}], u'id': u'174963', u'clientName': u'Koti'}
            return response

        elif sensorID == "895892":
            response = {u'ignored': 0, u'protocol': u'fineoffset', u'name': u'Kellari', u'editable': 1, u'lastUpdated': 1367497808, u'timezoneoffset': 10800, u'sensorId': u'73', u'data': [{u'name': u'temp', u'value': u'13.1'}], u'id': u'895892', u'clientName': u'Kasvari'}
            return response
        else:
            return {"error": "Sensor doesn't exist"}

        return {"error": "Sensor doesn't exist"}

        return self.request("sensor/info", {"id": sensorID})

    def getSensors(self):
        """
            Fetches a list of sensors in the system.
        """

        # Debug code, uses local database
        from Config import Config
        config = Config("configuration.json")
        sensors = config.getItem("sensors", "")
        if len(sensors) > 0:
            return sensors
        else: return None

        return self.request("sensors/list", "")
