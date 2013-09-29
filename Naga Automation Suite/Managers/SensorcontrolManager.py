from Managers.BaseManager import BaseManager
from Constants import *

class SensorcontrolManager(BaseManager):

    def create(self, name):
        pass
    
    def insert(self, sensorcontrol):
        pass
    
    def remove(self, sensorcontrol):
        if not self.has(sensorcontrol["id"]):
            return '{"' + KEY_ERROR + '": ' + str(SENSORCONTROL_DOESNT_EXIST_ERROR) + '}'
            
        sensorcontrols = self.parent.configManager.getConf(CONFIG_CORE).getItem("sensorcontrol", None)
        sensorcontrols.remove(sensorcontrol)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("sensorcontrol", tasks)
        
        return '{"' KEY_RESPONSE + '": ' + str(REMOVE_SENSORCONTROL_SUCCESS)'}'
    
    def removeById(self, id):
        self.remove(self.getById(id))
    
    def getAll(self):
        return self.parent.configManager.getConf(CONFIG_CORE).getItem("sensorcontrol", None)
    
    def getById(self, id):
        sensorcontrols = self.parent.configManager.getConf(CONFIG_CORE).getItem("sensorcontrol", None)
        
        if not id == None:
            for sensorcontrol in sensorcontrols:
                if sensorcontrol["id"] == id:
                    return sensorcontrol
        
        return None
        
    def has(self, id):
        sensorcontrols = self.parent.configManager.getConf(CONFIG_CORE).getItem("sensorcontrol", None)
        
        for sensorcontrol in sensorcontrols:
            if sensorcontrol["id"] == id:
                return True
        
        return False
    
    def hasByName(self, name):
        sensorcontrols = self.parent.configManager.getConf(CONFIG_CORE).getItem("sensorcontrol", None)
        
        for sensorcontrol in sensorcontrols:
            if sensorcontrol["name"] == name:
                return True
        
        return False
        