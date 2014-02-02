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
    
    def __init__(self, confFile, createIfNeeded):
        self.confRoot = CONFIG_ROOT
        self.confFile = confFile
        self.mutex = RLock() # For thread safe file operations.
        self.data = {}
        
        if not path.isfile(self.confRoot + self.confFile + ".json"):
            if not createIfNeeded:
                return None

            f = open(self.confRoot + self.confFile + ".json", "w")
            json.dump(self.data, f, indent = 4)
            f.close()

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

        f = open(self.confRoot + self.confFile + "_backup.json", "w")
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
        
        #return self.data.items()
        return self.data