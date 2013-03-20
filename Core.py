from Connection import Connection
from Protocol import Protocol
from Scheduler import Scheduler
from Scheduler import Task
from Devices import DeviceManager
from Config import Config
from Logging import Logging
from time import sleep

class Core:
    """
        Initializes all the submodules and updates them when needed,
        although some modules are threaded so they take care of themselves.
    """
    
    def __init__(self):
        self.logging = Logging(self)
        self.protocol = Protocol()
        self.connection = Connection(self.logging)
        self.scheduler = Scheduler()
        self.deviceManager = DeviceManager(self.connection)
        self.config = Config(self)

    def initialize(self):
        self.config.loadConf()
        self.scheduler.initialize()
        
    def update(self):
        self.logging.parseMessage()

def main():
    server = Core()
    server.initialize()
    
    while True:
        server.update()
        sleep(0.1)

if __name__ == "__main__":
    main()