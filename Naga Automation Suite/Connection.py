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

import socket
from time import sleep
from threading import Thread
import json
import Utils
from Constants import *
from inspect import stack

class Connection:
    """
        This class handles the low-level interfacing with remote Arduino controller logic using
        sockets as the means of communication. Note that this class has nothing to do with the
        communication protocol which is defined in a separate class.
    """
    
    def __init__(self, parent):
        self.__name__ = "Connection"
        self.parent = parent
        self.running = True
        
        self.clients = parent.configManager.getConf(CONFIG_CORE).getItem("clients", "")
        self.hostAddress = parent.configManager.getConf(CONFIG_SETTINGS).getItem("localip", "") # Your own home network address.
        self.port = parent.configManager.getConf(CONFIG_SETTINGS).getItem("arduinoport", 48371)
        self.listenPort = parent.configManager.getConf(CONFIG_SETTINGS).getItem("arduinolistenport", 48372)
        
        self.updateThread = Thread(target = self.listenArduinos).start()
        self.webserverThread = Thread(target = self.webserver).start()

    def listenArduinos(self):
        """
            This function should run in a thread. It opens a socket and binds it
            to the host address and the communication port. It then listens for
            incoming traffic and handles reading and dispatching the messages
            to the Logging module.
        """
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.hostAddress, self.listenPort))
        serverSocket.settimeout(1) # Use nonblocking socket so the thread doens't get stuck waiting for incoming traffic.
        
        while self.running:
            try:
                serverSocket.listen(1)
                conn, addr = serverSocket.accept()
            
            except socket.timeout:
                sleep(0.1)
                continue
                
            data = conn.recv(4096)
            if not data: return
            
            response = json.loads(data.decode("UTF-8").strip())
            client, request = self.parent.logging.createMessage(response)
            
            if client == None or request == None:
                sleep(0.1)
                continue
                
            self.parent.logging.logMessage(response, client, request)
            sleep(0.1)
    
    def webserver(self):
        """
            This function handles communications between the webserver and the rest of the system.
        """
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.hostAddress, 6718))
        serverSocket.settimeout(1) # Use nonblocking socket so the thread doens't get stuck waiting for incoming traffic.
        
        while self.running:
            try:
                serverSocket.listen(1)
                conn, addr = serverSocket.accept()
            
            except socket.timeout:
                sleep(0.1)
                continue
                
            try:
                data = conn.recv(16384)
            
            except:
                sleep(0.1)
                continue
            
            if not data: continue
            request = data.decode("UTF-8").strip()
            tmp = ""
            
            try:
                if request.startswith("{") and request.endswith("}"):
                    tmp = json.dumps(Utils.dispatchRequest(self.parent, json.loads(request)))
                
                if request == "getSensors":
                    tmp = Utils.getSensors(self.parent)

                elif request == "getDevices":
                    tmp = Utils.getDevices(self.parent)
                
                elif request.startswith("controlDevice"):
                    tmp = Utils.controlDevice(self.parent, request)
                
                elif request == "getSensorControl":
                    tmp = Utils.getSensorControl(self.parent)
                    
                elif request.startswith("sensorControl"):
                    tmp = Utils.sensorControl(self.parent, request)
                    
                elif request == "getTasks":
                    tmp = Utils.getTasks(self.parent)
                
                elif request.startswith("task"):
                    tmp = Utils.taskManagement(self.parent, request)
                
                elif request == "getEvents":
                    tmp = Utils.getEventLog(self.parent)
                
                elif request.startswith("settings"):
                    tmp = Utils.settings(self.parent, request)
                    
                elif request == "getIntervals":
                    tmp = Utils.getIntervals(self.parent)
                    
                elif request.startswith("getFreeMemory"):
                    tmp = Utils.getFreeMemory(self.parent, request)
                    
                if tmp == None:
                    tmp = "Action returned NoneType"
                
            except Exception as e:
                self.parent.logging.logEvent("Webserver handler encountered an exception while executing task: " + str(e), "red")
                conn.sendall("".encode("UTF-8", "replace"))
                conn.close()
                continue
                
            try:
                conn.sendall(tmp.encode("UTF-8", "replace"))
            
            except Exception as e:
                self.parent.logging.logEvent("Webserver handler encountered an exception: " + str(e), "red")
                conn.close()
                continue
                
            conn.close()
            sleep(0.01)
    
    def send(self, message, waitForResponse = True):
        """
            Attempts to send a message to the Arduino.
        """
        
        self.parent.logging.logDebug(self.__name__ + "." + stack()[0][3])
        
        s = None
        response = ""
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            s = None
            self.parent.logging.logMessage(json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}'), message[0], json.loads(message[1]))
            return json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}')
        
        try:
            s.settimeout(5)
            s.connect((self.clients[message[0]], self.port))
        except socket.error as e:
            s.close()
            s = None
            self.parent.logging.logMessage(json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}'), message[0], json.loads(message[1]))
            return json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}')
        
        try:
            # aJson lib only supports strings up to length of 255 characters and memory deallocation will
            # fail if we try to send longer strings than that, so prevent it.
            #if len(message[1]) > MAX_MESSAGE_LENGTH:
            #    self.parent.logging.logMessage(json.loads('{"' + KEY_ERROR + '": ' + str(MESSAGE_TOO_LONG_ERROR) + '}'), message[0], json.loads(message[1]))
            #    return json.loads('{"' + KEY_ERROR + '": ' + str(MESSAGE_TOO_LONG_ERROR) + '}')
            
            s.send((message[1] + "/").encode())
        except:
            s.close()
            s = None
            self.parent.logging.logMessage(json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}'), message[0], json.loads(message[1]))
            return json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}')
        
        # If user has defined it wants to get an answer from Arduino, wait fo the answer.
        if waitForResponse:
            try:
                tmp = s.recv(4096).decode("UTF-8").strip()
                
                response = json.loads(tmp)
                #response = json.loads(s.recv(4096).decode("UTF-8").strip())
                self.parent.logging.logMessage(response, message[0], json.loads(message[1])) # Send automatically to logger, user doesn't need to bother with that.
            except: #socket.timeout as e:
                s.close()
                s = None
                self.parent.logging.logMessage(json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}'), message[0], json.loads(message[1]))
                return json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}')
        
        s.close()
        s = None
        return response
    