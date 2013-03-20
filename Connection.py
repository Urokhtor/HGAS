import socket
import socketserver
from time import sleep
from threading import Thread

class Connection:
    """
        This class handles the low-level interfacing with remote Arduino controller logic using
        sockets as the means of communication. Note that this class has nothing to do with the
        communication protocol which is defined in a separate class.
    """
    
    def __init__(self, logging):
        self.running = True
        self.logging = logging
        self.server = []
        
        self.listenToHost = "xxx.xxx.xxx.xx" # Address of the Arduino
        self.hostAddress = "xxx.xxx.xxx.xx" # Your own home network address.
        self.port = 80
        
        self.updateThread = Thread(target=self.update)
        self.updateThread.start()

    def update(self):
        """
            This function should run in a thread. It opens a socket and binds it
            to the host address and the communication port. It then listens for
            incoming traffic and handles reading and dispatching the messages
            to the Logging module.
        """
        
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.hostAddress, self.port))
        
        while self.running:
            serverSocket.listen(1)
            conn, addr = serverSocket.accept()
            data = conn.recv(4096)
            if not data: return
            self.logging.inputQueue.put(data.decode().strip())
            sleep(0.5)
    
    def send(self, message):
        """
            Attempts to send a message to the Arduino.
        """
        
        s = None
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            s = None
            # Log error
        
        try:
            s.connect((self.listenToHost, self.port))
        except socket.error as e:
            s.close()
            s = None
            # Log error
        
        s.send(message.encode())
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        s = None
