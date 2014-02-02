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
#from rauth import OAuth1Service
from Constants import *

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

        self.port = parent.settingsManager.getValueByName("arduinoport")
        self.listenPort = parent.settingsManager.getValueByName("arduinolistenport")
        
        #self.updateThread = Thread(target = self.listenArduinos).start()
        self.webserverThread = Thread(target = self.webserver).start()

    def listenArduinos(self):
        """
            This function should run in a thread. It opens a socket and binds it
            to the host address and the communication port. It then listens for
            incoming traffic and handles reading and dispatching the messages
            to the Logging module.
        """
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.getLocalIP(), self.listenPort))
        serverSocket.settimeout(1) # Use nonblocking socket so the thread doens't get stuck waiting for incoming traffic.
        
        while self.running:
            try:
                serverSocket.listen(1)
                conn, addr = serverSocket.accept()
            
            except socket.timeout:
                sleep(0.01)
                continue
                
            data = conn.recv(4096)
            if not data: return
            
            response = json.loads(data.decode("UTF-8").strip())
            client, request = self.parent.logging.createMessage(response)
            
            if client is None or request is None:
                sleep(0.01)
                continue
                
            self.parent.logging.logMessage(response, self.parent.clientManager.getById(client), request)
            sleep(0.01)
    
    def webserver(self):
        """
            This function handles communications between the webserver and the rest of the system.
        """
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.getLocalIP(), 6719))
        serverSocket.settimeout(1) # Use nonblocking socket so the thread doens't get stuck waiting for incoming traffic.
        
        while self.running:
            try:
                serverSocket.listen(1)
                conn, addr = serverSocket.accept()
            
            except socket.timeout:
                sleep(0.01)
                continue
                
            try:
                data = conn.recv(16384)
            
            except:
                sleep(0.01)
                continue
            
            if not data: continue
            request = data.decode("UTF-8").strip()
            tmp = ""
            
            try:
                if request.startswith("{") and request.endswith("}"):
                    tmp = json.dumps(Utils.dispatchRequest(self.parent, json.loads(request)))

                if tmp is None:
                    tmp = "{\"" + KEY_ERROR + ": \"Action returned NoneType\"}"
                
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
    
    def send(self, document, waitForResponse = True):
        """
            Attempts to send a message to the Arduino.
        """
        
        self.parent.logging.logDebug(self.__name__ + "." + "send")

        client = self.parent.clientManager.getById(document["clientid"])
        protocol = document["protocol"]

        if client is None:
            self.parent.logging.logMessage(json.loads('{"' + KEY_ERROR + '": ' + str(CLIENT_DOESNT_EXIST_ERROR) + '}'), client, json.loads(document))
            return json.loads('{"' + KEY_ERROR + '": ' + str(CLIENT_DOESNT_EXIST_ERROR) + '}')

        if protocol == CLIENT_TYPE_ARDUINO:
            message = json.dumps(document["message"])
            s = None
            response = ""

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5) # Arduino takes some time to respond, give it 5 seconds to process the request.
                s.connect((client["ip"], self.port))
                s.send((message + "/").encode())

                # If user has defined it wants to get an answer from Arduino, wait fo the answer.
                if waitForResponse:
                    response = json.loads(s.recv(4096).decode("UTF-8").strip())
                    self.parent.logging.logMessage(response, client, json.loads(message)) # Send automatically to logger, user doesn't need to bother with that.

            except:
                s.close()
                s = None
                self.parent.logging.logMessage(json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}'), client, json.loads(message))
                return json.loads('{"' + KEY_ERROR + '": ' + str(NO_ARDUINO_RESPONSE) + '}')

            s.close()
            s = None
            return response

        elif protocol == CLIENT_TYPE_TELLDUS:
            self.telldusRequest(document["message"])

    def telldusRequest(self, message):
        method = message["method"]
        params = message["params"]

        #oauth = OAuth1Service() # TODO: Build the oauth session.

        # TODO: Send the request
        # TODO: Log the response (how should the response be sent to logging service? We are mostly concerned about device states and sensor readings.)
        # TODO: When adding sensors and devices the values should be mapped to a NAS object. Things like ID of the Telldus object will be put to field "telldusid" and the "id" will be NAS ID.

    def getLocalIP(self):
        return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]