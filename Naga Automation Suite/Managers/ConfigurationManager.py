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

from Conf.Configuration import Configuration

class ConfigurationManager:
    """
        A simple class which supports making configurations using JSON objects. Used to store pretty much
        all the data in this project.
    """
    
    def __init__(self):
        self.confs = {}

    def loadConf(self, conf):
        """
            Takes the conf name as a parameter and searches for it in the conf directory. Returns True
            if the conf was successfully found and loaded, False if it wasn't found or couldn't be loaded.
        """
        
        tmp = Configuration(conf)
        
        if tmp is None:
            return False
        
        self.confs[conf] = tmp
            
        return True
    
    def unloadConf(self, conf):
        """
            Checks if conf file exists, if not returns False. Otherwise removes conf file and returns True.
        """
        
        if not conf in self.confs:
            return False
        
        del self.confs[conf]
        return True
        
    def getConf(self, conf):
        """
            Returns the conf object that is requested. If doesn't find it, returns None.
        """
        
        if not conf in self.confs:
            return None
            
        return self.confs[conf]
        