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
from threading import RLock
from os import path
from Constants import CONFIG_ROOT

class Configuration:
    """
        A simple class which supports making configurations using JSON objects. Used to store pretty much
        all the data in this project.
    """
    
    def __init__(self, confFile):
        self.confRoot = CONFIG_ROOT
        self.confFile = confFile
        self.mutex = RLock() # For thread safe file operations.
        self.data = {}
        
        if not path.isfile(self.confRoot + self.confFile + ".json"):
            return None
            
        f = open(self.confRoot + self.confFile + ".json", "r")
            
        try:
            self.data = json.load(f)
            
        except ValueError:
            return None
            
        #self._write()
        f.close()

    def _write(self):
        """
            Backend which writes the data down to the configuration file.
        """
        
        self.mutex.acquire()
        f = open(self.confRoot + self.confFile + ".json", "w")
        json.dump(self.data, f, indent = 4)
        f.close()
        self.mutex.release()
    
    def setItem(self, key, value):
        """
            Updates an object and writes it down to the configuration file.
        """
        
        self.data[key] = value
        self._write()
    
    def getItem(self, key, default = ""):
        """
            Returns a JSON object with given name - or the given default parameter if the object wasn't found.
        """
        
        return self.data.get(key, default)
        
    def items(self):
        """
            Returns all the data in the configuration file.
        """
        
        return self.data.items()
        
    def verify(self):
        noChanges = True
        
        if not "devices" in self.data:
            noChanges = False
            self.data["devices"] = []
            
        if not "sensors" in self.data:
            noChanges = False
            self.data["sensors"] = []
            
        if not "sensorinfo" in self.data:
            noChanges = False
            self.data["sensorinfo"] = []
            
        if not "alerts" in self.data:
            noChanges = False
            self.data["alerts"] = []
        
        if not "tasks" in self.data:
            noChanges = False
            self.data["tasks"] = []
            
        if not "sensorcontrol" in self.data:
            noChanges = False
            self.data["sensorcontrol"] = []
            
        if not "localip" in self.data:
            noChanges = False
            self.data["localip"] = ""
            
        if not "listenport" in self.data:
            noChanges = False
            self.data["listenport"] = 8080
            
        if not "arduinoport" in self.data:
            noChanges = False
            self.data["arduinoport"] = 48371
            
        if not "logginginterval" in self.data:
            noChanges = False
            self.data["logginginterval"] = 15
            
        if not "dailyplotinterval" in self.data:
            noChanges = False
            self.data["dailyplotinterval"] = 30
        
        if not "weeklyplotinterval" in self.data:
            noChanges = False
            self.data["weeklyplotinterval"] = 60
        
        if not "sensorcontrolinterval" in self.data:
            noChanges = False
            self.data["sensorcontrolinterval"] = 1
            
        if not "alertsinterval" in self.data:
            noChanges = False
            self.data["alertsinterval"] = 1
            
        if not "eventloglength" in self.data:
            noChanges = False
            self.data["eventloglength"] = 40
            
        if not "senderemailaddress" in self.data:
            noChanges = False
            self.data["senderemailaddress"] = ""
            
        if not "receiveremailaddress" in self.data:
            noChanges = False
            self.data["receiveremailaddress"] = ""
            
        if not "mailserver" in self.data:
            noChanges = False
            self.data["mailserver"] = ""
        
        if not "mailport" in self.data:
            noChanges = False
            self.data["mailport"] = 25
        
        return noChanges
