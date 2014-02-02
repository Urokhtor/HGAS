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

from Scheduler import Task

class Startup:
    """
        This class contains functions for initializing on startup all the tasks the system needs to perform.
        It also loads sensors and devices in memory and relays the object information to Arduino(s). 
    """

    def __init__(self, parent):
        self.parent = parent

    def addSensors(self):
        """
            Either sends sensors to clients or syncs them from other API depending on client type.
        """

        sensors = self.parent.sensorManager.getAll()

        for sensor in sensors:
            self.parent.sensorManager.insert(sensor, True)

    def addDevices(self):
        """
            Either sends devices to clients or syncs them from other API depending on client type.
        """

        devices = self.parent.deviceManager.getAll()

        for device in devices:
            self.parent.deviceManager.insert(device, True)

    def addTasks(self):
        """
            Adds user defined write tasks..
        """

        # UPDATE THESE TO USE A MANAGER
        tasks = self.parent.taskManager.getAll()

        for task in tasks:
            self.parent.taskManager.insertToScheduler(task)

    def addSensorLogging(self):
        """
            Task which logs sensor data at given interval.
        """
        
        task = Task("Log sensors", "read", "", 0, 0, self.parent.logging.getSensorReadings)
        
        try:
            interval = self.parent.settingsManager.getByName("logginginterval")

            if interval is None: return # TODO: WE SHOULD WRITE A MESSAGE
            task.scheduleByInterval(interval["value"])
                            
        except:
            self.parent.logging.logEvent("Startup error: Error adding sensor logging intervals, task not added", "red")
            return
                
        self.parent.scheduler.taskManager.addTask(task)
    
    def addDailyPlots(self):
        """
            Task which generates daily plots for the sensors.
        """

        generatePlots = self.parent.settingsManager.getByName("generateplots")

        if generatePlots is None or generatePlots["value"] is False: return # TODO: WE SHOULD WRITE A MESSAGE

        task = Task("dailyplots", "plot", "", 0, 3, self.parent.plot.generateDailyPlots)

        interval = self.parent.settingsManager.getByName("dailyplotinterval")

        if interval is None: return # TODO: WE SHOULD WRITE A MESSAGE
        task.scheduleByInterval(interval["value"])

        self.parent.scheduler.taskManager.addTask(task)
    
    def addWeeklyPlots(self):
        """
            Task which generates weekly plots for the sensors.
        """


        generatePlots = self.parent.settingsManager.getByName("generateplots")

        if generatePlots is None or generatePlots["value"] is False: return # TODO: WE SHOULD WRITE A MESSAGE
        
        task = Task("weeklyplots", "plot", "", 3, self.parent.plot.generateWeeklyPlots)

        interval = self.parent.settingsManager.getByName("weeklyplotinterval")

        if interval is None: return # TODO: WE SHOULD WRITE A MESSAGE
        task.scheduleByInterval(interval["value"])

        self.parent.scheduler.taskManager.addTask(task)

    def addSensorControl(self):
        """
            Task which executes added sensorcontrol tasks.
        """

        # TODO: FIX THE CALLBACK, IT NEEDS TO USE THE SENSORCONTROL ROUTINE!!!
        task = Task("sensorcontrol", "sensorcontrol", self.parent, 2, self.parent.plot.generateWeeklyPlots, True)
        
        try:
            interval = self.parent.settingsManager.getByName("sensorcontrolinterval")

            if interval is None: return # TODO: WE SHOULD WRITE A MESSAGE
            task.scheduleByInterval(interval["value"])
                            
        except:
            self.parent.logging.logEvent("Startup error: Error adding sensorcontrol intervals, task not added", "red")
            return
        
        self.parent.scheduler.taskManager.addTask(task)