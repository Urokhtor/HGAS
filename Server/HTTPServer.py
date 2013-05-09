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

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import json
from hashlib import sha512

class requestHandler(BaseHTTPRequestHandler):
    """
        Custom requesthandler for handling webUI requests. A login system is also implemented.
    """
    
    f = open("configuration.json", "r")
    localip = json.load(f)["localip"]
    f.close()

    def do_AUTHHEAD(self):
        """
            Ask the user to authenticate before access is granted.
        """
        
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Authenticate or thou shall not pass!\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        """
            Server requests to fetch web information, such as the frontpage and the JavaScript file and
            images.
        """
        
        # Read password into memory, note that it's never stored for a long time, it's always discarded after
        # serving a request.
        f = open(".passwd.json", "r")
        data = json.load(f)
        f.close()

        # No access without authentication.
        if not "Authorization" in self.headers:
            self.do_AUTHHEAD()
            self.wfile.write("No auth header received".encode("UTF-8"))
            return
            
        auth = self.headers["Authorization"]
        authPass = ""
        
        if auth == None: return
        
        # Process the given auth and encrypt it so we can compare the given user and password to the one
        # stored in the database.
        if auth.find("Basic ") != -1:
            authPass = auth.split(" ", 1)[1]
        
        # Use some proper encryption.
        m = sha512()
        m.update(authPass.encode("UTF-8", "replace"))
        hashedString = m.digest().decode("UTF-8", "replace")
        
        # Send an another authentication request if the user and password didn't match.
        if hashedString != data["auth"]:
            self.do_AUTHHEAD()
            return
        
        # Given authentication is a match, start serving the request.
        elif hashedString == data["auth"]:
            rootdir = "Website/" #file location
            
            try:
                # If the requested file is an image, it's a graph so fetch it from the Plots-folder. Otherwise
                # server the request from Website-folder.
                if self.path == "/": self.path = "frontpage.html"
                elif self.path.endswith(".png"): rootdir = "Plots/"
                self.path = self.path.replace("/", "")
                files = os.listdir(rootdir)
                
                if self.path in files:
                    f = None
                    
                    # Send images with a separate routine.
                    if self.path.endswith(".png"):
                        f = open("Plots/" + self.path, "rb")
                        try: self.wfile.write(f.read())
                        except: return # Broken pipe probably
                        f.close()
                        return
                        
                    else:
                        f = open(rootdir + self.path) # Open requested file
                    
                    # Send code 200 response
                    self.send_response(200)

                    # Send header first
                    self.send_header('Content-type','text-html')
                    self.end_headers()
                    
                    # Send file content to client
                    try: self.wfile.write(f.read().encode("UTF-8"))
                    except: return # Broken pipe probably
                        
                    f.close()
                    return
                
            except IOError:
                self.send_error(404, 'file not found')
    
    def do_POST(self):
        """
            Serve posts which are webUI's requests to fetch data from the server or commands sent from it.
        """
        
        self.send_response(200)
        self.end_headers()
        contentLength = int(self.headers['Content-Length'])
        request = self.rfile.read(contentLength).decode("UTF-8")
        s = None
        
        # Try to create a socket object.
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            s = None
            return
        
        # Try to connect to the internal webserver handler.
        try:
            s.connect((self.localip, 6718))
        except socket.error as e:
            s.close()
            s = None
            return
        
        # Send the request and wait for result.
        try:
            s.sendall(request.encode("UTF-8", "repace"))
            result = s.recv(16384)
        
        except:
            s.close()
            s = None
            return
            
        s.close()
        s = None
        
        # Write the result back to the webUI and return.
        try: self.wfile.write(result)
        except: return # Broken pipe probably
        
        return
        
class WebServer:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def setUp(self):
        httpd = HTTPServer((self.host, self.port), requestHandler)
        httpd.serve_forever()