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

class Config:
    """
        A simple class which supports making configurations using JSON objects. Used to store pretty much
        all the data in this project.
    """
    
    def __init__(self, confFile):
        self.confFile = confFile
        self.mutex = RLock() # For thread safe file operations.
        f = open(self.confFile, "r")
        self.data = json.load(f)
        
        # Generate a default conf if one doesn't exist so there won't be any errors.
        if not "devices" in self.data: self.data["devices"] = []
        if not "sensors" in self.data: self.data["sensors"] = []
        if not "tasks" in self.data: self.data["tasks"] = []
        if not "sensorcontrol" in self.data: self.data["sensorcontrol"] = []
        if not "clients" in self.data: self.data["clients"] = []
        if not "localip" in self.data: self.data["localip"] = ""
        if not "listenport" in self.data: self.data["listenport"] = 8080
        if not "arduinoport" in self.data: self.data["arduinoport"] = 48371
        if not "verbose" in self.data: self.data["verbose"] = True
        if not "logginginterval" in self.data: self.data["logginginterval"] = 10
        if not "dailyplotinterval" in self.data: self.data["dailyplotinterval"] = 30
        if not "weeklyplotinterval" in self.data: self.data["weeklyplotinterval"] = 60
        if not "sensorcontrolinterval" in self.data: self.data["sensorcontrolinterval"] = 10
        if not "eventloglength" in self.data: self.data["eventloglength"] = 40
        
        self._write()
        f.close()

    def _write(self):
        """
            Backend which writes the data down to the configuration file.
        """
        
        self.mutex.acquire()
        f = open(self.confFile, "w")
        json.dump(self.data, f, indent = 4)
        f.close()
        self.mutex.release()
    
    def setItem(self, key, value):
        """
            Updates an object and writes it down to the configuration file.
        """
        
        self.data[key] = value
        self._write()
    
    def getItem(self, key, default):
        """
            Returns a JSON object with given name - or the given default parameter if the object wasn't found.
        """
        
        return self.data.get(key, default)
        
    def items(self):
        """
            Returns all the data in the configuration file.
        """
        
        return self.data.items()
