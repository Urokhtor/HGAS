from Managers.BaseManager import BaseManager
from Constants import *

class DeviceManager(BaseManager):

    def __init__(self, parent):
        BaseManager.__init__(self, parent, CONFIG_CORE, "devices")
        
    def updateDeviceState(self, id, state):
        device = self.getById(id)
            
        if device is None:
            return False
        
        device["state"] = int(state)
        self.set(device)
        #devices = self.parent.configManager.getConf(CONFIG_CORE).getItem("devices", None)
        #self.parent.configManager.getConf(CONFIG_CORE).setItem("devices", devices)
        return True
    
    def create(self, name, type, clientid, index, maxontime, useshygrometer = False, hygrometerindex = -1):
        """
            Creates a new device object with the parameters supplied and assigns a new unique ID to it
            and then returns it. Use DeviceManager.insertDevice(device) to add the newly created device
            to the list.
        """
        
        device = {}
        device["name"] = name
        device["type"] = type
        device["index"] = index
        device["clientid"] = clientid
        device["telldusid"] = None
        device["state"] = 0
        device["maxontime"] = maxontime
        device["useshygrometer"] = useshygrometer
        device["hygrometerindex"] = hygrometerindex
        device["id"] = self.getNextId()
        
        return device
        
    def insert(self, device, isStartup = False):
        if self.has(device["id"] and not isStartup):
            return '{"' + KEY_ERROR + '": ' + str(PUMP_EXISTS_ERROR) + '}'
        
        response = {}
        
        if device["type"] == DEVICE_TYPE_PUMP:
            response = self.parent.connection.send(self.parent.protocol.insert(device, TYPE_PUMP, isStartup))
            
            if KEY_ERROR in response: return response
            if response[KEY_RESPONSE] != INSERT_PUMP_SUCCESS: return response
            
            if not isStartup:
                devices = self.parent.configManager.getConf(CONFIG_CORE).getItem("devices", None)
                devices.append(device)
                self.parent.configManager.getConf(CONFIG_CORE).setItem("devices", devices)
            
        return response
    
    def remove(self, device):
        if not self.has(device["id"]):
            return '{"' + KEY_ERROR + '": ' + str(PUMP_DOESNT_EXIST_ERROR) + '}'
            
        response = self.parent.connection.send(self.parent.protocol.remove(device, TYPE_PUMP))
        
        if KEY_ERROR in response: return response
        
        devices = self.parent.configManager.getConf(CONFIG_CORE).getItem("devices", None)
        devices.remove(device)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("devices", devices)
        return response
    
    def removeById(self, id):
        return self.remove(self.getById(id))

    def enable(self, id):
        pass

    def disable(self, id):
        pass

    def toggle(self, id):
        pass