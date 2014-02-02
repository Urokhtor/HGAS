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
from Managers.SensorManager import SensorManager
from Managers.DeviceManager import DeviceManager
from Managers.TaskManager import TaskManager
from Managers.SettingsManager import SettingsManager
from Managers.MessageManager import MessageManager
from Managers.ClientManager import ClientManager
from HTTPServer import WebServer
from Startup import Startup
from Constants import *

from time import sleep
import sys, json

class Core:
    """
        Initializes all the submodules and serves as a connection point between different modules.
    """
    
    def __init__(self, justPlots = False):
        self.__name__ = "Core"
        
        self.configManager = ConfigurationManager()
        
        # These return True of False depending on whether loading the conf was a success.
        # It should be checked if the conf was loaded successfully and failures should be logged.
        self.configManager.loadConf(CONFIG_CORE, True)
        self.configManager.loadConf(CONFIG_SETTINGS, True)
        self.configManager.loadConf(CONFIG_FORMS, True)
        self.configManager.loadConf(CONFIG_URLMAP, True)
        self.configManager.loadConf(CONFIG_MESSAGES, True)
        
        self.moduleManager = ModuleManager(self)
        self.settingsManager = SettingsManager(self)
        self.clientManager = ClientManager(self)
        self.sensorManager = SensorManager(self)
        self.deviceManager = DeviceManager(self)
        self.taskManager = TaskManager(self)
        self.messageManager = MessageManager(self)
        self.logging = Logging(self)

        if self.settingsManager.equals("plottype", "matplotlib"):
            from Plot import Plot
            self.plot = Plot(self)

        self.protocol = Protocol(self)
        if not justPlots: self.connection = Connection(self)
        if not justPlots: self.scheduler = Scheduler()
        if not justPlots: self.webServer = WebServer(self.connection.getLocalIP(), self.settingsManager.getValueByName("listenport")) # Currently binds to localhost. But this needs to be fixed so other connections can be listened to too.

    def initialize(self):
        self.logging.logDebug(self.__name__ + "." + "initialize")
        self.scheduler.initialize()
        
        startup = Startup(self)
        startup.addSensors()
        startup.addDevices()
        #startup.addTasks()
        #startup.addSensorLogging()
        #startup.addDailyPlots()
        #startup.addWeeklyPlots()
        #startup.addSensorControl()

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
        # Check if auth exists, if not, add a new one.
        f = open(".passwd.json", "r")
        tmp = f.readlines()

        if len(tmp) is 0 or "auth" not in json.loads("".join(tmp)):
            addUser()

        try:
            server = Core()
            server.initialize()

            # We actually don't even go here because of the HTTP server.
            while 1:
                sleep(0.1)

        except KeyboardInterrupt as e:
            from os import _exit
            _exit(0)

        #except Exception as e:

    # Adds an encrypted user and password pair.
    elif sys.argv[1] == "set" and sys.argv[2] == "user":
        addUser()

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

def addUser():
    user = input("Enter user name: ")
    password = input("Enter password: ")

    from base64 import b64encode
    b64encoded = b64encode((user + ":" + password).encode("UTF-8", "replace"))

    from hashlib import sha512
    m = sha512()
    m.update(b64encoded)
    hashedString = m.digest()

    tmp = {}
    tmp["auth"] = hashedString.decode("UTF-8", "replace")

    f = open(".passwd.json", "w")
    json.dump(tmp, f, indent = 4)
    f.close()
    print("Added auth")

if __name__ == "__main__":
    main()