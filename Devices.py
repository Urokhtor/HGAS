#from Connection import Connection
from Protocol import Protocol

class DeviceManager:
    
    def __init__(self, connection):
        self.connection = connection
        self.devices = {}
        self.sensorDevices = {}
        self.pumpDevices = {}
    
    def addDevice(self, name, device):
        if name not in self.devices:
            self.devices[name] = device
    
    def removeDevice(self, name):
        if name in self.devices:
            del self.devices[name]
    
    def hasDevice(self, name):
        if name in self.devices: return True
        else: return False
    
    def hasDeviceByIndex(self, index):
        for name, device in self.devices.items():
            if device.getIndex() == index:
                return True
        
        return False
    
    def getDevice(self, name):
        if name in self.devices: return self.devices[name]
        else: return None
    
    def getDeviceByIndex(self, index):
        for name, device in self.devices.items():
            if device.getIndex() == index:
                return device
        
        return None
    
    def getDeviceNameByIndex(self, index):
        for name, device in self.devices.items():
            if device.getIndex() == index:
                return name
        
        return None
        
    def addSensorDevice(self, name, device):
        if name not in self.sensorDevices:
            self.sensorDevices[name] = device
            
    def removeSensorDevice(self, name):
        if name in self.sensorDevices:
            del self.sensorDevices[name]
    
    def hasSensorDevice(self, name):
        if name in self.sensorDevices: return True
        else: return False
    
    def hasSensorDeviceByIndex(self, index):
        for name, device in self.sensorDevices.items():
            if device.getIndex() == index:
                return True
        
        return False
    
    def getSensorDevice(self, name):
        if name in self.sensorDevices: return self.sensorDevices[name]
        else: return None
    
    def getSensorDeviceByIndex(self, index):
        for name, device in self.sensorDevices.items():
            if device.getIndex() == index:
                return device
        
        return None
    
    def getSensorDeviceNameByIndex(self, index):
        for name, device in self.sensorDevices.items():
            if device.getIndex() == index:
                return name
        
        return None
    
    def addPumpDevice(self, name, device):
        if name not in self.pumpDevices:
            self.pumpDevices[name] = device
            
    def removePumpDevice(self, name):
        if name in self.pumpDevices:
            del self.pumpDevices[name]
    
    def hasPumpDevice(self, name):
        if name in self.pumpDevices: return True
        else: return False
    
    def hasPumpDeviceByIndex(self, index):
        for name, device in self.pumpDevices.items():
            if device.getIndex() == index:
                return True
        
        return False
    
    def getPumpDevice(self, name):
        if name in self.pumpDevices: return self.pumpDevices[name]
        else: return None

    def getPumpDeviceByIndex(self, index):
        for name, device in self.pumpDevices.items():
            if device.getIndex() == index:
                return device
        
        return None
        
    def getPumpDeviceNameByIndex(self, index):
        for name, device in self.pumpDevices.items():
            if device.getIndex() == index:
                return name
        
        return None
        
class Device:

    def __init__(self, index, type):
        self.index = index
        self.type = type
    
    def setIndex(self, index):
        self.index = index
    
    def getIndex(self):
        return self.index
    
    def setType(self, type):
        self.type = type
    
    def getType(self):
        return self.type
    
class SensorDevice:

    def __init__(self, index, type, lowThreshold = -1024, highThreshold = -1024):
        self.index = index
        self.type = type
        self.lowThreshold = lowThreshold
        self.highThreshold = highThreshold
    
    def setIndex(self, index):
        self.index = index
    
    def getIndex(self):
        return self.index
    
    def setType(self, type):
        self.type = type
    
    def getType(self):
        return self.type
    
    def setHighThreshold(self, highTreshold):
        self.highThreshold = highThreshold
    
    def getHighThreshold(self):
        return self.highThreshold
        
    def setLowThreshold(self, lowThreshold):
        self.lowThreshold = lowThreshold
    
    def getLowThreshold(self):
        return self.lowThreshold

class PumpDevice:

    def __init__(self, index, maxOnTime, usesHumiditySensor, humiditySensorIndex):
        self.index = index
        self.maxOnTime = maxOnTime
        self.usesHumiditySensor = usesHumiditySensor
        self.humiditySensorIndex = humiditySensorIndex
    
    def setIndex(self, index):
        self.index = index
    
    def getIndex(self):
        return self.index
    
    def setMaxOnTime(self, maxOnTime):
        self.maxOnTime = maxOnTime
    
    def getMaxOnTime(self):
        return self.maxOnTime
    
    def setUsesHumiditySensor(self, usesHumiditySensor):
        self.usesHumiditySensor = usesHumiditySensor
        
    def getUsesHumiditySensor(self):
        return self.usesHumiditySensor
    
    def setHumiditySensorIndex(self, humiditySensorIndex):
        self.humiditySensorIndex = humiditySensorIndex
    
    def getHumiditySensorIndex(self):
        return self.humiditySensorIndex