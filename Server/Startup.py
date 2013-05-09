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
from Utils import executeSensorControl

class Startup:
    """
        This class contains functions for initializing on startup all the tasks the system needs to perform.
        It also loads sensors and devices in memory and relays the object information to Arduino(s). 
    """

    def __init__(self, parent):
        self.parent = parent
    
    def addDevices(self):
        """
            Loads sensors and devices to memory and sends the Arduino(s) signal to add them in its memory.
        """
        
        sensors = self.parent.config.getItem("sensors", "")
        devices = self.parent.config.getItem("devices", "")
        
        for sensor in sensors:
            self.parent.connection.send((sensor["clientname"], self.parent.protocol.insertSensor(sensor["index"], sensor["type"], sensor["lowthreshold"], sensor["highthreshold"])))
            
        for device in devices:
            if device["type"] == "pump":
                usesHygrometer = False
                hygrometerIndex = -1
                if "hygrometerindex" in device:
                    usesHygrometer = True
                    hygrometerIndex = device["hygrometerindex"]
                    
                self.parent.connection.send((device["clientname"], self.parent.protocol.insertPump(device["index"], device["maxontime"], usesHygrometer, hygrometerIndex)))

    
    def addTasks(self):
        """
            Adds user defined write tasks..
        """
        
        tasks = self.parent.config.getItem("tasks", "")
        devices = self.parent.config.getItem("devices", "")
        sensors = self.parent.config.getItem("sensors", "")
        
        for task in tasks:
            if task["type"] == "write":
                deviceName = task["device"]
                device = None
                
                for _device in devices:
                    if _device["name"] == deviceName:
                        device = _device
                        break
                
                if device:
                    newTask = Task(task["name"], "write", (device["clientname"], self.parent.protocol.write(device["index"])), device["index"], 1, self.parent.connection.send)
                
                else:
                    self.parent.logging.logEvent("Startup error: Can't add task " + task["name"] + ", device " + deviceName + " doesn't exist", "red")
                    pass
                
                if not "schedules" in task:
                    self.parent.logging.logEvent("Startup error: Schedules not specified for task " + task["name"], "red")
                    continue
                
                for time in task["schedules"]:
                    try:
                        hour, minute = time.split(":")
                        if int(hour) > 23 or int(hour) < 0 or int(minute) > 60 or int(minute) < 0:
                            self.parent.logging.logEvent("Startup error: Scheduled time " + time + " is not valid in task " + task["name"], "red")
                            continue
                            
                        else:
                            taskTime = int(hour)*60*60 + int(minute)*60
                            newTask.addScheduledEvent(taskTime)
                            
                    except:
                        self.parent.logging.logEvent("Startup error: Scheduled time " + time + " is not valid in task " + task["name"], "red")
                        continue
                        
                self.parent.scheduler.taskManager.addTask(newTask)
    
    def addSensorLogging(self):
        """
            Task which logs sensor data at given interval.
        """
        
        task = Task("Log sensors", "read", "", 0, 0, self.parent.logging.getSensorReadings)
        
        try:
            time = 0
            timeInterval = self.parent.config.getItem("logginginterval", 10)*60
                        
            while time < 86400:
                task.addScheduledEvent(time)
                time += timeInterval
                            
        except:
            self.parent.logging.logEvent("Startup error: Error adding sensor logging intervals, task not added", "red")
            return
                
        self.parent.scheduler.taskManager.addTask(task)
    
    def addDailyPlots(self):
        """
            Task which generates daily plots for the sensors.
        """
        
        task = Task("dailyplots", "plot", "", 0, 3, self.parent.plot.generateDailyPlots)

        time = 0
        timeInterval = self.parent.config.getItem("dailyplotinterval", 30)*60
                    
        while time < 86400:
            task.addScheduledEvent(time)
            time += timeInterval
                
        self.parent.scheduler.taskManager.addTask(task)
    
    def addWeeklyPlots(self):
        """
            Task which generates weekly plots for the sensors.
        """
        
        task = Task("weeklyplots", "plot", "", 0, 3, self.parent.plot.generateWeeklyPlots)

        time = 0
        timeInterval = self.parent.config.getItem("weeklyplotinterval", 60)*60
                    
        while time < 86400:
            task.addScheduledEvent(time)
            time += timeInterval
                
        self.parent.scheduler.taskManager.addTask(task)
        
    def addSensorControl(self):
        """
            Task which executes added sensorcontrol tasks.
        """
        
        task = Task("sensorcontrol", "sensorcontrol", self.parent, 0, 2, executeSensorControl, True)
        
        try:
            time = 0
            timeInterval = self.parent.config.getItem("sensorcontrolinterval", 1)*60
                        
            while time < 86400:
                task.addScheduledEvent(time)
                time += timeInterval
                            
        except:
            self.parent.logging.logEvent("Startup error: Error adding sensorcontrol intervals, task not added", "red")
            return
        
        self.parent.scheduler.taskManager.addTask(task)
        