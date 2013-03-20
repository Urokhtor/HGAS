from Protocol import Protocol
import Devices
from Scheduler import Task

class Config:

    def __init__(self, parent):
        self.parent = parent
        self.fileName = "config.txt"
        self.errlogFileName = "errlog.txt"
        self.header = "[header]"
        self.sensor = "[sensor]"
        self.pump = "[pump]"
        self.lamp = "[lamp]"
        self.task = "[task]"
        self.uploadConf = True
    
    def loadConf(self):
        seeking = 0
        foundHeader = False
        f = open(self.fileName, "r")
        err = open(self.errlogFileName, "w")
        line = f.readline()
        
        #self.parent.connection.send(self.parent.protocol.setupStart())
        
        while line != "":
            if len(line) == 1:
                pass
                
            elif line.startswith("#"):
                pass
            
            elif line.find(self.header) != -1:
                seeking = 1
                foundHeader = True
                
            elif line.find(self.sensor) != -1:
                if not foundHeader:
                    err.write("Sensor definitions before header!")
                    break
                    
                seeking = 2
                
            elif line.find(self.pump) != -1:
                if not foundHeader:
                    err.write("Pump definitions before header!")
                    break
                    
                seeking = 3
            
            elif line.find(self.lamp) != -1:
                if not foundHeader:
                    err.write("Lamp definitions before header!")
                    break
                
                seeking = 4
            
            elif line.find(self.task) != -1:
                if not foundHeader:
                    err.write("Task definitions before header!")
                    break
                
                seeking = 5
            
            # Read header data into memory
            elif seeking == 1:
                if line.find("upload config = false") != -1:
                    self.uploadConf = False
                    
            # Read sensors into memory
            elif seeking == 2:
                name = ""
                index = 0
                type = 0
                highThreshold = -1024
                lowThreshold = -1024
                
                if len(line.split(" ")) == 2:
                    name, index = line.split(" ")
                elif len(line.split(" ")) == 3:
                    name, index, type = line.split(" ")
                elif len(line.split(" ")) == 4:
                    name, index, type, highThreshold = line.split(" ")
                elif len(line.split(" ")) == 5:
                    name, index, type, highThreshold, lowThreshold = line.split(" ")
                
                device = Devices.SensorDevice(int(index), int(type), int(highThreshold), int(lowThreshold))
                self.parent.deviceManager.addSensorDevice(name, device)
                
                
                if self.uploadConf:
                    self.parent.connection.send(self.parent.protocol.insertSensor(device.getIndex(), device.getType(), device.getLowThreshold(), device.getHighThreshold()))
    
            # Read pumps into memory
            elif seeking == 3:
                name = ""
                index = 0
                maxOnTime = 0
                usesHygrometer = False
                hygrometerIndex = -1
                
                if len(line.split(" ")) == 2:
                    name, index = line.split(" ")
                elif len(line.split(" ")) == 3:
                    name, index, maxOnTime = line.split(" ")
                elif len(line.split(" ")) == 4:
                    name, index, maxOnTime, usesHygrometer = line.split(" ")
                elif len(line.split(" ")) == 5:
                    name, index, maxOnTime, usesHygrometer, hygrometerIndex = line.split(" ")
                
                # If usesHygrometer can't have a boolean value (i.e. 0 or 1), force it to false.
                if int(usesHygrometer) > 1 or int(usesHygrometer) < 0:
                    usesHygrometer = "0"
                
                device = Devices.PumpDevice(int(index), int(maxOnTime), bool(usesHygrometer), int(hygrometerIndex))
                self.parent.deviceManager.addPumpDevice(name, device)

                if self.uploadConf:
                    self.parent.connection.send(self.parent.protocol.insertPump(device.getIndex(), device.getMaxOnTime(), device.getUsesHumiditySensor(), device.getHumiditySensorIndex()))
            
            elif seeking == 4:
                name = ""
                index = 0
                type = 0
                
                if len(line.split(" ")) == 2:
                    name, index = line.split(" ")
                
                device = Devices.Device(int(index), int(type))
                self.parent.deviceManager.addDevice(name, device)
            
            elif seeking == 5:
                name = ""
                action = ""
                device = ""
                schedules = []
                isInterval = False
                
                parameters = line.split("(")[0].strip().split(" ")
                
                if line.find("(") != -1:
                    if line.split("(")[1].find("min") != -1:
                        schedules = line.split("(")[1].split("min")[0].strip()
                        isInterval = True
                        
                    else:
                        schedules = line.split("(")[1].strip().split(")")[0].replace(" ", "").replace(":", " ").split(",")
                
                
                if len(parameters) < 3 or len(parameters) > 3:
                    err.write("Erroneous task: wront number of arguments.")
                    break
                
                name, action, device = parameters
                _device = {}
                task = {}
                
                if self.parent.deviceManager.hasDevice(device):
                    _device = self.parent.deviceManager.getDevice(device)
                elif self.parent.deviceManager.hasSensorDevice(device):
                    _device = self.parent.deviceManager.getSensorDevice(device)
                elif self.parent.deviceManager.hasPumpDevice(device):
                    _device = self.parent.deviceManager.getPumpDevice(device)
                
                if action.find("write") != -1:
                    task = Task(name, self.parent.protocol.write(_device.getIndex()), _device.getIndex(), self.parent.connection.send)
                elif action.find("read") != -1:
                    task = Task(name, self.parent.protocol.readSensor(_device.getIndex()), _device.getIndex(), self.parent.connection.send)
                
                # If we want to add time by interval, do so. I.e. execute every 10 minutes and so on.
                # Otherwise read the specified schedules, i.e. execute at clock 15:00:00.
                if isInterval:
                    _time = 0
                    timeInterval = int(schedules)*60
                    
                    while _time < 86400:
                        task.addScheduledEvent(_time)
                        _time += timeInterval
                
                else:
                    for schedule in schedules:
                        taskTime = schedule.split(" ")
                        taskTimeInt = int(taskTime[0])*60*60 + int(taskTime[1])*60 + int(taskTime[2])
                            
                        if taskTimeInt > 86400:
                            err.write("Couldn't add scheduled event: time doesn't exist.")
                            continue
                            
                        task.addScheduledEvent(taskTimeInt)
                
                self.parent.scheduler.taskManager.addTask(task)
            
            line = f.readline()
        
        #self.parent.connection.send(self.parent.protocol.setupEnd())
        f.close()
        err.close()