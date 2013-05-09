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
from Scheduler import Task
from time import sleep

def getSensors(parent):
    """
        Returns sensor objects.
    """
    
    return json.dumps(parent.config.getItem("sensors", ""))
    
def getDevices(parent):
    """
        Returns device objects.
    """
    
    return json.dumps(parent.config.getItem("devices", ""))

def getSensorControl(parent):
    """
        Returns sensorcontrol objects.
    """
    
    return json.dumps(parent.config.getItem("sensorcontrol", ""))
    
def controlDevice(parent, request):
    """
        Controls one device in the given index. Support turning on, turning off and toggling.
    """
    
    command, index, action = request.split(";")
    device = None
    
    try:
        index = int(index)
    except:
        parent.logging.logEvent("ControlDevice: Supplied device index isn't correct, only integers are allowed", "red")
        return "ControlDevice: Supplied device index isn't correct, only integers are allowed"
    
    if action != parent.protocol.enable and action != parent.protocol.disable and action != parent.protocol._write:
        parent.logging.logEvent("ControlDevice: Supplied action type isn't supported", "red")
        return "ControlDevice: Supplied action type isn't supported"
        
    for device in parent.config.getItem("devices", ""):
        if device["index"] == index:
            if action == parent.protocol.enable:
                parent.connection.send((device["clientname"], parent.protocol.writeEnable(index)))
            
            elif action == parent.protocol.disable:
                parent.connection.send((device["clientname"], parent.protocol.writeDisable(index)))
            
            elif action == parent.protocol._write:
                parent.connection.send((device["clientname"], parent.protocol.write(index)))
            
            # Give Arduino some time to respond back so devices get updated before the webUI requests it.
            sleep(0.5)
            return "OK"
    
    parent.logging.logEvent("ControlDevice: Couldn't find device with index " + str(index), "red")
    return "ControlDevice: Couldn't find device with index " + str(index)

def sensorControl(parent, request):
    """
        Performs routines for adding, modifying and deleting sensorcontrol tasks.
    """
    
    tmp, parameters = request.split(";", 1)
    line = tmp.split(" ", 2)
    
    if line[1] == "add" or line[1] == "modify":
        try:
            deviceName, sensorName, sensorType, highThreshold, lowThreshold, isInverted = parameters.split(";")
        
        except:
            parent.logging.logEvent("SensorControl failed: wrong number of arguments provided", "red")
            return "SensorControl failed: Wrong number of argumets provided"
        
        device = None
        sensor = None
        highCallback = "" # Command for action when sensor value exceeds high value.
        lowCallback = "" # Command for action when sensor value passes under low value.
        sensorControl = parent.config.getItem("sensorcontrol", "")
        
        # Loop through sensorcontrol tasks to see if it already exists and user is trying to add a sensorcontrol
        # with same name.
        for task in sensorControl:
            if task["name"] == line[2] and line[1] == "add":
                parent.logging.logEvent("SensorControl: Can't add sensorcontrol with name " + line[2] + ": sensorcontrol already exists", "red")
                return "SensorControl: Can't add sensorcontrol with name " + line[2] + ": sensorcontrol already exists"
        
        for _device in parent.config.getItem("devices", ""):
            if _device["name"] == deviceName:
                device = _device
        
        # Sensorcontrol can't work if device is not found, return and inform the user about it.
        if device == None:
            parent.logging.logEvent("SensorControl failed: Couldn't find device with name " + deviceName, "red")
            return "Couldn't find device with name " + deviceName
            
        for _sensor in parent.config.getItem("sensors", ""):
            if _sensor["name"] == sensorName:
                sensor = _sensor
        
        # Sensorcontrol can't work if sensor is not found, return and inform the user about it.
        if sensor == None:
            parent.logging.logEvent("SensorControl failed: Couldn't find sensor with name " + sensorName, "red")
            return "Couldn't find sensor with name " + sensorName
                
        if not sensorType == "temp" and not sensorType == "humidity" and not sensorType == "hygrometer" and not sensorType == "ultrasound":
            parent.logging.logEvent("SensorControl failed: Sensortype " + sensorType + " not supported", "red")
            return "Sensortype " + sensorType + " not supported"
        
        # Make sure that thresholds are se properly (i.e. are valid numbers). Otherwise return and infor user about the error.
        try:
            highThreshold = float(highThreshold)
            lowThreshold = float(lowThreshold)
        
        except:
            parent.logging.logEvent("SensorControl failed: Threshold not properly formatted", "red")
            return "Threshold not properly formatted"
        
        # Check to see that there are no errors with the given thresholds, such as both values being exactly
        # the same.
        if highThreshold < lowThreshold:
            parent.logging.logEvent("SensorControl failed: Attempting to set thresholds in inverted order", "red")
            return "SensorControl failed: Attempting to set thresholds in inverted order"
        
        elif highThreshold == lowThreshold:
            parent.logging.logEvent("SensorControl failed: First and second thresholds can't have the same value", "red")
            return "SensorControl failed: First and second thresholds can't have the same value"
        
        # Determine whether exceeding high threshold should turn on or off the device. Then assign the inverted
        # action to low threshold callback.
        if isInverted == "0":
            highCallback = "e"
            lowCallback = "d"
        
        elif isInverted == "1":
            highCallback = "d"
            lowCallback = "e"
        
        # Create the new object.
        tmp = {"name": line[2], "devicename": deviceName, "deviceID": device["index"], "sensorname": sensorName, "sensorID": sensor["index"], "sensortype": sensorType, "highthreshold": highThreshold, "lowthreshold": lowThreshold, "highcallback": highCallback, "lowcallback": lowCallback, "isrunning": False, "data": {}}
        
        # If old task is modified, remove it and add the new one.
        if line[1] == "modify":
            for task in sensorControl:
                if task["name"] == line[2]:
                    sensorControl.remove(task)
                    break
                    
        sensorControl.append(tmp)
        parent.config.setItem("sensorcontrol", sensorControl)
        
        # Return and inform the user about success.
        if line[1] == "add":
            parent.logging.logEvent("SensorControl: Successfully added sensorcontrol " + line[2], "green")
            return "Successfully added sensorcontrol " + line[2]
            
        elif line[1] == "modify":
            parent.logging.logEvent("SensorControl: Successfully modified sensorcontrol " + line[2], "green")
            return "Successfully modified sensorcontrol " + line[2]
        
        
    elif line[1] == "del":
        sensorControl = parent.config.getItem("sensorcontrol", "")
        
        # Loop through the sensorcontrol tasks to find the task with the wanted name. Then return and inform
        # the user about success.
        for task in sensorControl:
            if task["name"] == line[2]:
                sensorControl.remove(task)
                parent.config.setItem("sensorcontrol", sensorControl)
                parent.logging.logEvent("SensorControl: Deleted task " + line[2], "orange")
                return "Deleted task " + line[2]
        
        # If we got here, sensorcontrol task with wanted name wasn't found in memory so return and inform the user.
        parent.logging.logEvent("SensorControl: Couldn't find task " + line[2] + " so didn't delete it", "red")
        return "Couldn't find task " + line[2] + " so didn't delete it"
        
def executeSensorControl(parent):
    """
        This function is called by the internal sensorcontrol task. It loops through all the sensorcontrol
        tasks that are saved. It first fetches the most recent sensor data and checks device's state (running
        or not), after which the assigned callback function is called if so required.
    """
    
    sensorControl = parent.config.getItem("sensorcontrol", "")
    
    for task in sensorControl:
        lastReading = None
        device = None

        for sensor in parent.config.getItem("sensors", ""):
            if sensor["index"] == task["sensorID"]:
                lastReading = float(sensor["lastreading"])
                task["lastreading"] = lastReading
                task["lastupdated"] = sensor["lastupdated"]
                break
        
        if lastReading == None:
            parent.logging.logEvent("ExecuteSensorControl: Failed to execute task " + task["name"] + ": Couldn't find reading", "red")
            continue
        
        for _device in parent.config.getItem("devices", ""):
            if _device["index"] == task["deviceID"]:
                device = _device
                task["isrunning"] = device["isrunning"]
                break
        
        if lastReading > task["highthreshold"]:
            if task["highcallback"] == parent.protocol.enable and not task["isrunning"]:
                parent.connection.send((device["clientname"], parent.protocol.writeEnable(task["deviceID"])))
                task["isrunning"] = True
                
                parent.logging.logEvent("SensorControl: Executed " + task["name"] + ", turned on device " + task["devicename"] + " after upper threshold was exceeded", "green")
                
            elif task["highcallback"] == parent.protocol.disable and task["isrunning"]:
                parent.connection.send((device["clientname"], parent.protocol.writeDisable(task["deviceID"])))
                task["isrunning"] = False

                parent.logging.logEvent("SensorControl: Executed " + task["name"] + ", turned off device " + task["devicename"] + " after upper threshold was exceeded", "green")
            
        elif lastReading < task["lowthreshold"]:
            if task["lowcallback"] == parent.protocol.disable and task["isrunning"]:
                parent.connection.send((device["clientname"], parent.protocol.writeDisable(task["deviceID"])))
                task["isrunning"] = False
                
                parent.logging.logEvent("SensorControl: Executed " + task["name"] + ", turned off device " + task["devicename"] + " after reading passed under lower threshold", "green")
                
            elif task["lowcallback"] == parent.protocol.enable and not task["isrunning"]:
                parent.connection.send((device["clientname"], parent.protocol.writeEnable(task["deviceID"])))
                task["isrunning"] = True
        
                parent.logging.logEvent("SensorControl: Executed " + task["name"] + ", turned on device " + task["devicename"] + " after reading passed under lower threshold", "green")
                
    parent.config.setItem("sensorcontrol", sensorControl)

def getTasks(parent):
    """
        Returns the task JSON objects as a string representation, also parses temporary tasks from the task
         manager to JSON and stringifies them.
    """
    
    tmp = []
    
    for task in parent.config.getItem("tasks", ""):
        if task["type"] != "write":
            continue
        
        tmp.append(task)
    
    for task in parent.scheduler.taskManager.tasks:
        if not task.isPermanent():
            tmplist = None
            deviceName = ""
            events = ""
            action = 0
            
            for _device in parent.config.getItem("devices", ""):
                if _device["index"] == task.getPort():
                    deviceName = _device["name"]
            
            for eventTime in task.getScheduledEvents().keys():
                tmpFloat = float(eventTime)/60/60
                hour = int(tmpFloat)
                minute = int(tmpFloat % hour * 60 + 0.5)
                
                if hour < 10: hour = "0" + str(hour)
                if minute < 10: minute = "0" + str(minute)
                
                events += str(hour) + ":" + str(minute) + ","
            
            if events.endswith(","): events = events[:-1]

            if isinstance(task.getAction(), str): tmplist = {"name": task.getName(), "type": "write", "actiontype": task.getAction()[0][1], "device": deviceName, "ispermanent": False, "schedules": events}
            else: tmplist = {"name": task.getName(), "type": "write", "actiontype": task.getAction()[0][1], "device": deviceName, "ispermanent": False, "schedules": events}
            
            tmp.append(tmplist)
    
    return json.dumps(tmp)
    
def taskManagement(parent, request):
    """
        Performs routines for adding, modifying and deleting tasks.
    """
    
    line = request.split(" ", 2)
    
    if line[1] == "del":
        taskName = line[2]
        
        # Loop through the task manager to find the task with corresponding name.
        for task in parent.scheduler.taskManager.tasks:
            if task.getName() == taskName:
                tasks = parent.config.getItem("tasks", "")
                
                # If task is permanent, remove it from the configuration file.
                if tasks and task.isPermanent():
                    for _task in tasks:
                        if _task["name"] == taskName:
                            tasks.remove(_task)
                            parent.config.setItem("tasks", tasks)
                            break
                
                # Remove task from task manager and report back to the user.
                parent.scheduler.taskManager.removeTask(taskName)
                parent.logging.logEvent("Task management: Removed task " + taskName, "orange")
                return "Task management: Removed task " + taskName
        
        # If we got here, task wasn't found, inform the user.
        parent.logging.logEvent("Task management: Couldn't find task " + taskName, "red")
        return "Task management: Couldn't find task " + taskName
                
    elif line[1] == "add" or line[1] == "modify":
        name, deviceName, action, isPermanent, schedules = line[2].split(";")
        device = None
        callback = parent.connection.send # Currently new tasks always want to relay data to Arduino.
        arguments = None
        
        # Prevent user from adding new tasks with same name.
        if parent.scheduler.taskManager.hasTask(name) and line[1] == "add":
            parent.logging.logEvent("Task management: Can't add task with name " + name + ": task already exists", "red")
            return "Task management: Can't add task with name " + name + ": task already exists"
        
        for _device in parent.config.getItem("devices", ""):
            if _device["name"] == deviceName:
                device = _device
        
        # No device found, therefore task couldn't possibly execute right so return and inform the user of the error.
        if not device:
            parent.logging.logEvent("Task management: Device not found", "red")
            return "Task management: Device not found"

        # Pick which action task should perform. Currently they can change relay states.
        if action == parent.protocol.enable:
            arguments = (device["clientname"], parent.protocol.writeEnable(device["index"]))
                        
        elif action == parent.protocol.disable:
            arguments = (device["clientname"], parent.protocol.writeDisable(device["index"]))
        
        elif action == parent.protocol._write:
            arguments = (device["clientname"], parent.protocol.write(device["index"]))
    
        else:
            parent.logging.logEvent("Task management: Couldn't add task: Action isn't supported", "red")
            return "Task management: Couldn't add task: Action isn't supported"
        
        if isPermanent == "true": isPermanent = True
        elif isPermanent == "false": isPermanent = False
        else:
            parent.logging.logEvent("Task management: Couldn't determine if the task was permanent or not during adding a task", "red")
            return "Task management: Couldn't determine if the task was permanent or not during adding a task"
        
        # Create new task objects, newConfigTask works as a placeholder until we determine whether the new task
        # is permanent. Temporary tasks aren't stored in the configuration file.
        newTask = Task(name, "write", arguments, device["index"], 1, callback, isPermanent)
        newConfigTask = {"name": name, "type": "write", "actiontype": action, "device": deviceName, "ispermanent": isPermanent, "schedules": []}
        
        # Because the schedules string we got from the client probably ends with a comma, get rid of the last one.
        if schedules.endswith(","):
            schedules = schedules[:-1]
            
        schedules = schedules.split(",")
        
        # Add events to the task. They are marked as minutes from midnight.
        for time in schedules:
            try:
                hour, minute = time.split(":")
                if int(hour) > 23 or int(hour) < 0 or int(minute) > 60 or int(minute) < 0:
                    parent.logging.logEvent("Task management: Scheduled time " + time + " is not valid in task " + name, "red")
                    return "Task management: Scheduled time " + time + " is not valid in task " + name
                            
                else:
                    taskTime = int(hour)*60*60 + int(minute)*60
                    newTask.addScheduledEvent(taskTime)
                    newConfigTask["schedules"].append(time)
                            
            except:
                parent.logging.logEvent("Task management: Scheduled time " + time + " is not valid in task " + name, "red")
                return "Task management: Scheduled time " + time + " is not valid in task " + name
        
        # Remove the old task if we are modifying it and then replace it with the newly made task object.
        if parent.scheduler.taskManager.hasTask(name):
            parent.scheduler.taskManager.removeTask(name)
            
        parent.scheduler.taskManager.addTask(newTask)

        tasks = parent.config.getItem("tasks", "")
        
        # Also remove the original task from configuration file if we are intending to change it.
        if line[1] == "modify":
            for task in tasks:
                if task["name"] == name:
                    tasks.remove(task)
                    break
        
        # Only store new task in the configuratin file if it's intended to be permanent.
        if isPermanent:
            tasks.append(newConfigTask)
        
        # Save configuration.
        parent.config.setItem("tasks", tasks)
        
        # Report back to the user correspondingly.
        if isPermanent and line[1] == "add":
            parent.logging.logEvent("Task management: Successfully added new task " + name, "green")
            return "Task management: Successfully added new task " + name
        
        elif isPermanent and line[1] == "modify":
            parent.logging.logEvent("Task management: Successfully modified task " + name, "green")
            return "Task management: Successfully modified task " + name
        
        elif not isPermanent and line[1] == "add":
            parent.logging.logEvent("Task management: Successfully added new temporary task " + name, "green")
            return "Task management: Successfully added new temporary task " + name
        
        elif not isPermanent and line[1] == "modify":
            parent.logging.logEvent("Task management: Successfully modified temporary task " + name, "green")
            return "Task management: Successfully modified temporary task " + name
        
    else:
        parent.logging.logEvent("Task management: Couldn't add task", "red")
        return "Task management: Couldn't add task"
    
def getEventLog(parent):
    """
        Return latest eventlog events.
    """
    
    try:
        return json.dumps(parent.logging.getEventLogLatestMessages())
    
    except Exception as e:
        return str(e)
    
def settings(parent, request):
    """
        This function governs changing system settings, such as sensor logging interval or how many lines of
        eventlog should be returned to the webUI.
    """
    
    try:
        command, type, value = request.split(";", 2)
        value = int(value)
    
    except Exception as e:
        parent.logging.logEvent("Settings error: " + str(e), "red")
        return "Settings error: " + str(e)
    
    # Sensor logging interval.
    if type == "logginginterval":
        try:
            if value < 1:
                parent.logging.logEvent("Settings error: Too few minutes given for logging interval", "red")
                return "Settings error: Too few minutes given for logging interval"
                
            time = 0
            task = parent.scheduler.taskManager.getTask("Log sensors")
            
            if task == None:
                parent.logging.logEvent("Settings error: Couldn't find task 'Log sensors'", "red")
                return "Settings error: Couldn't find task 'Log sensors'"
            
            task.removeAllScheduledEvents()
            
            timeInterval = value * 60
            
            while time < 86400:
                task.addScheduledEvent(time)
                time += timeInterval
            
        except:
            parent.logging.logEvent("Settings error: Error changing sensor logging intervals", "red")
            return "Settings error: Error changing sensor logging intervals"
        
        parent.scheduler.taskManager.findNextTask()
        parent.config.setItem("logginginterval", value)
        parent.logging.logEvent("Settings: Changed logging interval to " + str(value) + " minutes", "green")
        return "Changed logging interval to " + str(value) + " minutes"
    
    # Interval for generating the 24 h graphs.
    elif type == "dailyplotinterval":
        try:
            if value < 1:
                parent.logging.logEvent("Settings error: Too few minutes given for daily plots interval", "red")
                return "Settings error: Too few minutes given for daily plots interval"
                
            time = 0
            task = parent.scheduler.taskManager.getTask("dailyplots")
            
            if task == None:
                parent.logging.logEvent("Settings error: Couldn't find task 'dailyplots'", "red")
                return "Settings error: Couldn't find task 'dailyplots'"
                
            task.removeAllScheduledEvents()
            
            timeInterval = value * 60
                        
            while time < 86400:
                task.addScheduledEvent(time)
                time += timeInterval
                            
        except:
            parent.logging.logEvent("Settings error: Error changing daily plots intervals", "red")
            return "Settings error: Error changing daily plots intervals"
        
        parent.scheduler.taskManager.findNextTask()
        parent.config.setItem("dailyplotinterval", value)
        parent.logging.logEvent("Settings: Changed daily plots interval to " + str(value) + " minutes", "green")
        return "Changed daily plots interval to " + str(value) + " minutes"
    
    # Interval for generating the 7 day graphs.
    elif type == "weeklyplotinterval":
        try:
            if value < 1:
                parent.logging.logEvent("Settings error: Too few minutes given for weekly plots interval", "red")
                return "Settings error: Too few minutes given for weekly plots interval"
                
            time = 0
            task = parent.scheduler.taskManager.getTask("weeklyplots")
            
            if task == None:
                parent.logging.logEvent("Settings error: Couldn't find task 'weeklyplots'", "red")
                return "Settings error: Couldn't find task 'weeklyplots'"
                
            task.removeAllScheduledEvents()
            
            timeInterval = value * 60
                        
            while time < 86400:
                task.addScheduledEvent(time)
                time += timeInterval
                            
        except:
            parent.logging.logEvent("Settings error: Error changing weekly plots intervals", "red")
            return "Settings error: Error changing weekly plots intervals"
        
        parent.scheduler.taskManager.findNextTask()
        parent.config.setItem("weeklyplotinterval", value)
        parent.logging.logEvent("Settings: Changed weekly plots interval to " + str(value) + " minutes", "green")
        return "Changed weekly plots interval to " + str(value) + " minutes"
    
    # Interval at which sensorcontrol tasks should be run.
    elif type == "sensorcontrolinterval":
        try:
            if value < 1:
                parent.logging.logEvent("Settings error: Too few minutes given for sensorcontrol interval", "red")
                return "Settings error: Too few minutes given for sensorcontrol interval"
                
            time = 0
            task = parent.scheduler.taskManager.getTask("sensorcontrol")
            
            if task == None:
                parent.logging.logEvent("Settings error: Couldn't find task 'sensorcontrol'", "red")
                return "Settings error: Couldn't find task 'sensorcontrol'"
                
            task.removeAllScheduledEvents()
            
            timeInterval = value * 60
                        
            while time < 86400:
                task.addScheduledEvent(time)
                time += timeInterval
                            
        except:
            parent.logging.logEvent("Settings error: Error changing sensorcontrol intervals", "red")
            return "Settings error: Error changing sensorcontrol intervals"
        
        parent.scheduler.taskManager.findNextTask()
        parent.config.setItem("sensorcontrolinterval", value)
        parent.logging.logEvent("Settings: Changed sensorcontrol interval to " + str(value) + " minutes", "green")
        return "Changed sensorcontrol interval to " + str(value) + " minutes"
    
    # How many lines from eventlog should be returned to the webUI.
    elif type == "eventloglength":
        try:
            if value > 70:
                parent.logging.logEvent("Settings error: Too many lines given for event log length", "red")
                return "Settings error: Too many lines given for event log length"
                
            elif value < 1:
                parent.logging.logEvent("Settings error: Too few lines given for event log length", "red")
                return "Settings error: Too few lines given for event log length"
                
            parent.config.setItem("eventloglength", value)
            
        except:
            parent.logging.logEvent("Settings error: Error changing eventlog length", "red")
            return "Settings error: Error changing eventlog length"

        parent.logging.logEvent("Settings: Changed eventlog length to " + str(value) + " lines", "green")
        return "Changed eventlog length to " + str(value) + " lines"
    
    # Gracefully shut down the system.
    elif type == "shutdown":
        parent.quit()
        
def getIntervals(parent):
    """
        Returns settings related data.
    """
    
    tmp = {}
    tmp["logginginterval"] = parent.config.getItem("logginginterval", "")
    tmp["dailyplotinterval"] = parent.config.getItem("dailyplotinterval", "")
    tmp["weeklyplotinterval"] = parent.config.getItem("weeklyplotinterval", "")
    tmp["sensorcontrolinterval"] = parent.config.getItem("sensorcontrolinterval", "")
    tmp["eventloglength"] = parent.config.getItem("eventloglength", "")
    
    return json.dumps([tmp])    