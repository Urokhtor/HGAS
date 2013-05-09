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

class Connection:
    """
        This class handles the low-level interfacing with remote Arduino controller logic using
        sockets as the means of communication. Note that this class has nothing to do with the
        communication protocol which is defined in a separate class.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.running = True
        
        self.clients = parent.config.getItem("clients", "")
        self.hostAddress = parent.config.getItem("localip", "") # Your own home network address.
        self.port = parent.config.getItem("arduinoport", 48371)
        
        self.updateThread = Thread(target = self.listen).start()
        self.webserverThread = Thread(target = self.webserver).start()

    def listen(self):
        """
            This function should run in a thread. It opens a socket and binds it
            to the host address and the communication port. It then listens for
            incoming traffic and handles reading and dispatching the messages
            to the Logging module.
        """
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.hostAddress, self.port))
        serverSocket.settimeout(1) # Use nonblocking socket so the thread doens't get stuck waiting for incoming traffic.
        
        while self.running:
            try:
                serverSocket.listen(0.5)
                conn, addr = serverSocket.accept()
            
            except socket.timeout:
                sleep(0.1)
                continue
                
            data = conn.recv(4096)
            if not data: return
            self.parent.logging.inputQueue.put(data.decode("UTF-8").strip())
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
                    
                if tmp == None:
                    tmp = "Action returned NoneType"
                
            except Exception as e:
                self.parent.logging.logEvent("Webserver handler encountered an exception while executing task: " + str(e), "red")
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
    
    def send(self, message):
        """
            Attempts to send a message to the Arduino.
        """
        
        s = None
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            s = None
            self.parent.logging.logEvent("Connection error: Couldn't send message " + message[1] + " to client " + message[0], "red")
            return
        
        try:
            s.connect((self.clients[message[0]], self.port))
        except socket.error as e:
            s.close()
            s = None
            self.parent.logging.logEvent("Connection error: Couldn't send message " + message[1] + " to client " + message[0], "red")
            return
        
        try:
            s.send(message[1].encode())
        except:
            s.close()
            s = None
            self.parent.logging.logEvent("Connection error: Couldn't send message " + message[1] + " to client " + message[0], "red")
            return
            
        s.close()
        s = None
    
    def sendList(self, message):
        """
            Loops through the supplied list, sending each list item separately. Not really needed anymore.
        """
        
        for msg in message:
            self.send(msg)
    