
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

from time import sleep, strftime, time
from datetime import datetime
from Constants import *
import json
from os import listdir

class Logging:
    """
        This class handles logging all the data from webUI and Arduino(s) and then fetching the logged data
        back to the webUI.
    """
    
    def __init__(self, parent):
        self.__name__ = "Logging"
        self.parent = parent # Needed to access device manager.
        
        #self.messageThread = Thread(target = self.parseMessage).start()
        #self.messageThread = Thread(target = self.logMessage).start()
        
    def getFiles(self):
        """
            Returns a list of files that exist.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "getFiles")
        
    
        return listdir("Logs/")
        
    def getSensorFileData(self, file, timeSecondsFromStart, startFromTime = -1):
        """
            Returns the data stored in a file.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "getSensorFileData")
        
        tmp = []
        startTime = 0
        endTime = 0
        
        for line in reversed(open("Logs/" + file, "r").readlines()):
            try:
                unixTime, value = line.split(",")
                unixTime = int(float(unixTime))
                value = float(value)
                
                # If user wants logs from some specified timeframe but the current line
                # happened after this specified timeframe, skip the line. This step will be
                # skipped if startFromTime is <= 0. In that case the logs are taken from the most
                # recent log event backwards.
                if unixTime > startFromTime and startFromTime > 0:
                    continue
                
                # If tmp contains nothing then we are processing the first element in the file.
                # Mark up the time of the most recent sensor reading and calculate how far back we
                # need to dig up sensor data.
                if len(tmp) == 0:
                    startTime = unixTime
                    endTime = startTime - timeSecondsFromStart
                
                # If we haven't reached the end of our logging scope, log the current reading and time.
                if unixTime >= endTime:
                    tmp.append((unixTime, value))
                
                # We've reached the end of our scope, so exit the loop and return the data.
                else:
                    break
            
            except:
                # We couldn't parse a line so discard it.
                pass
        
        return tmp
    
    def getSensorReading(self, sensor):
        """
            Sends a request to get the reading for one sensor supplied as the parameter.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "getSensorReading")
        
        
        return self.parent.connection.send((sensor["clientname"], self.parent.protocol.readSensor(sensor["id"], sensor["index"])))
    
    def getSensorReadings(self, params):
        """
            Loops through all the sensors and polls their reading separately.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "getSensorReadings")
        
        tmp = []
        
        for sensor in self.parent.deviceManager.getSensors():
            tmp.append(self.getSensorReading(sensor))
    
        return tmp
        
    def getEventLogLatestMessages(self):
        """
            Returns the defined number of lines from eventlog.
        """
        self.parent.logging.logDebug(self.__name__ + "." + "getEventLogLatestMessages")
        
        
        tmp = []
        linesToRead = self.parent.configManager.getConf(CONFIG_SETTINGS).getItem("eventloglength", 40)
        
        for line in reversed(open("Logs/eventlog.csv", "r").readlines()):
            try:
                unixTime, text = line.split(",", 1)
                tmpTime = datetime.fromtimestamp(float(unixTime))
                
                day = str(tmpTime.day)
                month = str(tmpTime.month)
                hour = str(tmpTime.hour)
                minute = str(tmpTime.minute)
                
                if len(day) == 1: day = "0" + day
                if len(month) == 1: month = "0" + month
                if len(hour) == 1: hour = "0" + hour
                if len(minute) == 1: minute = "0" + minute
                    
                
                tmp.append("[" + day + "." + month + " " + hour + ":" + minute + "] " + text)
                
                if len(tmp) >= linesToRead:
                    break
                
            except:
                pass
                
        return tmp

    def logMessage(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logMessage")
        
        try:
            if KEY_ERROR in response:
                self.logError(response, client, request)
                
            elif request[KEY_COMMAND] == SEND_READ:
                self.logRead(response, client, request)
                        
            elif request[KEY_COMMAND] == SEND_WRITE:
                self.logWrite(response, client, request)
                        
            elif request[KEY_COMMAND] == SEND_ENABLE:
                self.logWrite(response, client, request)
                        
            elif request[KEY_COMMAND] == SEND_DISABLE:
                self.logWrite(response, client, request)
                        
            elif request[KEY_COMMAND] == SEND_INSERT:
                self.logInsert(response, client, request)
            
            elif request[KEY_COMMAND] == SEND_MODIFY:
                self.logModify(response, client, request)
                
            elif request[KEY_COMMAND] == SEND_REMOVE:
                self.logRemove(response, client, request)
                
            elif request[KEY_COMMAND] == SEND_FREEMEMORY:
                self.logFreeMemory(response, client, request)
                
        except Exception as e:
            self.logEvent("Log message error: " + str(e), "red")
            
    def logError(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logError")
        
        if response[KEY_ERROR] == NO_COMMAND_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(NO_COMMAND_ERROR), "red")
        elif response[KEY_ERROR] == NO_INDEX_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(NO_INDEX_ERROR), "red")
        elif response[KEY_ERROR] == NO_DEVICE_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(NO_DEVICE_ERROR), "red")
        elif response[KEY_ERROR] == NO_TYPE_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(NO_TYPE_ERROR), "red")
        elif response[KEY_ERROR] == WRONG_TYPE_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(WRONG_TYPE_ERROR), "red")
        elif response[KEY_ERROR] == UNRECOGNISED_COMMAND_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(UNRECOGNISED_COMMAND_ERROR), "red")
        elif response[KEY_ERROR] == NO_ARDUINO_RESPONSE:
            self.logEvent("Log message error: Received error with ID " + str(NO_ARDUINO_RESPONSE), "red")
        elif response[KEY_ERROR] == MESSAGE_TOO_LONG_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(MESSAGE_TOO_LONG_ERROR), "red")
        elif response[KEY_ERROR] == SENSOR_EXISTS_ERROR:
            if request[KEY_IS_STARTUP]:
                response = json.loads('{"' + KEY_RESPONSE + '": ' + str(INSERT_SENSOR_SUCCESS) + '}')
                self.logInsert(response, client, request)
                
            else:
                self.logEvent("Log message error: Received error with ID " + str(SENSOR_EXISTS_ERROR), "red")
                
        elif response[KEY_ERROR] == PUMP_EXISTS_ERROR:
            if request[KEY_IS_STARTUP]:
                response = json.loads('{"' + KEY_RESPONSE + '": ' + str(INSERT_PUMP_SUCCESS) + '}')
                self.logInsert(response, client, request)
                
            else:
                self.logEvent("Log message error: Received error with ID " + str(PUMP_EXISTS_ERROR), "red")
                
        elif response[KEY_ERROR] == SENSOR_DOESNT_EXIST_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(SENSOR_DOESNT_EXIST_ERROR), "red")
        elif response[KEY_ERROR] == PUMP_DOESNT_EXIST_ERROR:
            self.logEvent("Log message error: Received error with ID " + str(PUMP_DOESNT_EXIST_ERROR), "red")
    
    def logRead(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logRead")
        
        sensor = self.parent.deviceManager.getSensorById(request[KEY_ID])
        
        if sensor == None:
            return
        
        if response[KEY_RESPONSE] == READ_SENSOR_SUCCESS and KEY_READING in response:
            self.parent.deviceManager.updateSensorReading(request[KEY_ID], response[KEY_READING])
            file = "Logs/" + str(sensor["id"]) + "_" + str(sensor["type"]) + ".csv"
            f = open(file, "a")
            f.write(str(time()) + "," + str(response[KEY_READING]) + "\n")
            f.close()
            
        else:
            if response[KEY_RESPONSE] != READ_SENSOR_SUCCESS:
                self.logEvent("Log message error: Response to getSensorReading(" + sensor["name"] + ") wasn't of the right type", "red")
                return
                
            elif not KEY_READING in response:
                self.logEvent("Log message error: No reading received for getSensorReading(" + sensor["name"] + ")", "red")
                return
                
    def logWrite(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logWrite")
        
        device = self.parent.deviceManager.getDeviceById(request[KEY_ID])
        
        if device == None:
            return
            
        if response[KEY_RESPONSE] == RUN_DEVICE_SUCCESS:
            if response[KEY_STATE] == DEVICE_STATE_ON:
                self.parent.deviceManager.updateDeviceState(request[KEY_ID], DEVICE_STATE_ON)
                self.logEvent("Received message: Turned on device " + device["name"], "green")
            
            elif response[KEY_STATE] == DEVICE_STATE_OFF:
                self.parent.deviceManager.updateDeviceState(request[KEY_ID], DEVICE_STATE_OFF)
                self.logEvent("Received message: Turned off device " + device["name"], "green")
            
            elif response[KEY_STATE] == -1:
                self.logEvent("Received message: Couldn't toggle device " + device["name"] + " state", "red")
        
        elif response[KEY_RESPONSE] == TOGGLED_DEVICE_OFF:
            self.parent.deviceManager.updateDeviceState(request[KEY_ID], DEVICE_STATE_OFF)
            self.logEvent("Received message: Turned off device " + device["name"], "green")
        
        # Device's state didn't change.
        elif response[KEY_RESPONSE] == NO_ACTION_NEEDED:
            return
        
        else:
            self.logEvent("Log message error: Response to insert action was not of correct type", "red")
    
    def logInsert(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logInsert")
        
        if response[KEY_RESPONSE] == INSERT_SENSOR_SUCCESS:
            sensor = self.parent.deviceManager.getSensorById(request[KEY_ID])
            
            if sensor != None and not request[KEY_IS_STARTUP]:
                self.logEvent("Log message error: Couldn't insert sensor, it already exists", "red")
                return
                
            if sensor != None and request[KEY_IS_STARTUP]:
                self.logEvent("Received message: Inserted sensor with id " + str(request[KEY_ID]), "green")
                return
            
            else:
                self.logEvent("Received message: Inserted sensor with id " + str(request[KEY_ID]), "green")
        
        elif response[KEY_RESPONSE] == INSERT_PUMP_SUCCESS:
            device = self.parent.deviceManager.getDeviceById(request[KEY_ID])
            
            if device != None and not request[KEY_IS_STARTUP]:
                self.logEvent("Log message error: Couldn't insert device, it already exists", "red")
                return
                
            if device != None and request[KEY_IS_STARTUP]:
                self.logEvent("Received message: Inserted device with id " + str(request[KEY_ID]), "green")
                return
            
            else:
                self.logEvent("Received message: Inserted device with id " + str(request[KEY_ID]), "green")
                
        else:
            self.logEvent("Log message error: Response to insert action was not of correct type", "red")
    
    def logModify(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logModify")
        
        if response[KEY_RESPONSE] == MODIFY_SENSOR_SUCCESS:
            sensor = self.parent.deviceManager.getDeviceById(request[KEY_ID])
            
            if sensor == None:
                self.logEvent("Log message error: Couldn't modify sensor, it doesn't exist", "red")
                return
            
            else:
                # Handle performed action here. This include updating the sensor object.
                return
                
        elif response[KEY_RESPONSE] == MODIFY_PUMP_SUCCESS:
            device = self.parent.deviceManager.getDeviceById(request[KEY_ID])
            
            if device == None:
                self.logEvent("Log message error: Couldn't modify device, it doesn't exist", "red")
                return
            
            else:
                # Handle performed action here. This include updating the device object.
                return
                
        else:
            self.logEvent("Log message error: Response to modify action was not of correct type", "red")
    
    def logRemove(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logRemove")
        
        if response[KEY_RESPONSE] == REMOVE_SENSOR_SUCCESS:
            sensor = self.parent.deviceManager.getSensorById(request[KEY_ID])
            
            if sensor == None:
                self.logEvent("Log message error: Sensor doesn't exist, couldn't remove it", "red")
                return
            
            else:
                name = sensor["name"]
                self.logEvent("Received message: Removed sensor " + name, "green")
                
        elif response[KEY_RESPONSE] == REMOVE_PUMP_SUCCESS:
            device = self.parent.deviceManager.getDeviceById(request[KEY_ID])
            
            if device == None:
                self.logEvent("Log message error: Device doesn't exist, couldn't remove it", "red")
                return
            
            else:
                name = device["name"]
                self.logEvent("Received message: Removed device " + name, "green")
                
        else:
            self.logEvent("Log message error: Response to insert action was not of correct type", "red")
    
    def logFreeMemory(self, response, client, request):
        self.parent.logging.logDebug(self.__name__ + "." + "logFreeMemory")
        
        if response[KEY_RESPONSE] == READ_FREEMEMORY_SUCCESS:
            self.logEvent("Received message: Arduino client " + client + "'s free memory is " + response[KEY_READING] + " KiB", "green")
        
        else:
            self.logEvent("Log message error: Response to free memory was not of correct type", "red")
    
    def createMessage(self, response):
        self.parent.logging.logDebug(self.__name__ + "." + "createMessage")
        
        device = self.parent.deviceManager.getDeviceById(response[KEY_ID])
            
        if device == None:
            self.logEvent("Log message error: Couldn't create message because couldn't find the device with ID " + str(response[KEY_ID]), "red")
            return None, None
    
        if response[KEY_RESPONSE] == TOGGLED_DEVICE_OFF:
            client = device["clientname"]
            request = self.parent.protocol.writeEnable(device["id"], device["index"])
            return client, json.loads(request)
        
        else:
            return None, None
    
    def logEvent(self, message, colour = "black"):
        """
            The standard logger function which takes the message as an argument and writes it to the
            event log.
        """
        
        text = '<span style="color:' + colour + '">' + message + '</span>'
        
        try:
            file = "Logs/eventlog.csv"
            
            f = open(file, mode="a")
            f.write(str(time()) + "," + text + "\n")
            f.close()
            
            if self.parent.configManager.getConf(CONFIG_SETTINGS).getItem("verbose", True):
                print("[" + strftime("%H:%M:%S") + "] " + message) # Debug code. Add handling to the Config module so this can be made optional.
        
        except:
            pass
    
    def logDebug(self, message):
        """
            Debug logger used to log which methods have been called. Also displays the call time in milliseconds.
            Can be disabled with the debug flag in conf. Currently this debug logging isn't stored anywhere,
            it exists only in the console where the debug data is written into.
        """
        
        if self.parent.configManager.getConf(CONFIG_SETTINGS).getItem("debug", False):
            print("[" + datetime.fromtimestamp(time()).strftime("%H:%M:%S.%f") + "] " + message)
            #print("[" + str(tmp.hour) + ":" + str(tmp.minute) + ":" + str(tmp.second) + "." + str(round(tmp.microsecond/1000)) + "] " + message)
        
        