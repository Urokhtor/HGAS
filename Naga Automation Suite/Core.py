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

from Connection import Connection
from Protocol import Protocol
from Scheduler import Scheduler
from Logging import Logging
from Managers.ConfigurationManager import ConfigurationManager
from Managers.ModuleManager import ModuleManager
from Managers.DeviceManager import DeviceManager
from Managers.TaskManager import TaskManager
from Managers.SettingsManager import SettingsManager
from Managers.ClientManager import ClientManager
from HTTPServer import WebServer
from Startup import Startup
#from Plot import Plot
from Constants import *

from time import sleep
import sys

class Core:
    """
        Initializes all the submodules and serves as a connection point between different modules.
    """
    
    def __init__(self, justPlots = False):
        self.__name__ = "Core"
        
        self.configManager = ConfigurationManager()
        
        # These return True of False depending on whether loading the conf was a success.
        # It should be checked if the conf was loaded successfully and failures should be logged.
        self.configManager.loadConf(CONFIG_CORE)
        self.configManager.loadConf(CONFIG_SETTINGS)
        self.configManager.loadConf(CONFIG_FORMS)
        self.configManager.loadConf(CONFIG_URLMAP)
        
        self.moduleManager = ModuleManager(self)
        self.clientManager = ClientManager(self)
        self.deviceManager = DeviceManager(self)
        self.taskManager = TaskManager(self)
        self.settingsManager = SettingsManager(self)
        self.logging = Logging(self)
        #self.plot = Plot(self)
        self.protocol = Protocol()
        if not justPlots: self.connection = Connection(self)
        if not justPlots: self.scheduler = Scheduler()
        if not justPlots: self.webServer = WebServer(self.configManager.getConf(CONFIG_SETTINGS).getItem("localip", ""), self.configManager.getConf(CONFIG_SETTINGS).getItem("listenport", 8080))

    def initialize(self):
        self.logging.logDebug(self.__name__ + "." + "initialize")
        self.scheduler.initialize()
        
        startup = Startup(self)
        startup.addDevices()
        startup.addTasks()
        startup.addSensorLogging()
        #startup.addDailyPlots()
        #startup.addWeeklyPlots()
        startup.addSensorControl()

        #modules = []

        #for moduleList in self.configManager.getConf(CONFIG_FORMS).getItem("modules", ""):
        #    modules.append(moduleList["module"])

        self.moduleManager.loadModules(self.configManager.getConf(CONFIG_FORMS).getItem("modules", ""))

        self.webServer.setUp()
    
    def quit(self):
        """
            Gives threads a signal to shut down, gives them some time to do so and then exits the program
            gracefully.
        """
        
        self.logging.logEvent("Core: Shutting down", "orange")
        self.connection.running = False
        sleep(1)
        from os import _exit
        _exit(0)
        
def main():
    # License disclaimer.
    print("Naga Automation Suite  Copyright (C) 2013  Jere Teittinen")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions; for more details visit the GPL")
    print("terms and conditions at <http://www.gnu.org/licenses/gpl.html>")
    print("")
    
    if len(sys.argv) == 1:
        server = Core()
        server.initialize()
        
        while 1:
            tmp = input("")
            print("You gave: " + tmp)
            sleep(0.1)
    
    # Adds an encrypted user and password pair.
    elif sys.argv[1] == "user":
        if len(sys.argv) != 4:
            print("An invalid number of arguments was passed. Syntax = python Core.py user [username] [password]")
            from os import _exit
            _exit(0)

        from base64 import b64encode
        b64encoded = b64encode((sys.argv[2] + ":" + sys.argv[3]).encode("UTF-8", "replace"))
        
        from hashlib import sha512
        m = sha512()
        m.update(b64encoded)
        hashedString = m.digest()
        
        import json
        f = open(".passwd.json", "r")
        tmp = json.load(f)
        f.close()
        
        tmp["auth"] = hashedString.decode("UTF-8", "replace")
            
        f = open(".passwd.json", "w")
        json.dump(tmp, f, indent = 4)
        f.close()
        print("Added auth")
    
    # Start the server for plot generation, generate them and exit.
    elif sys.argv[1] == "plot":
        server = Core(True)
        
        if len(sys.argv) == 2 or sys.argv[2] == "day":
            print("Generating daily plots...")
            server.plot.generateDailyPlots("")
        
        if len(sys.argv) == 2 or sys.argv[2] == "week":
            print("Generating weekly plots...")
            server.plot.generateWeeklyPlots("")
        
        print("\nDone generating, exiting...")
        
        from os import _exit
        _exit(0)
    

if __name__ == "__main__":
    main()