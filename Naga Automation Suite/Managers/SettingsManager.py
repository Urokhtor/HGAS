from Managers.BaseManager import BaseManager
from Constants import CONFIG_SETTINGS

class SettingsManager(BaseManager):
    
    def getAll(self):
        return self.parent.configManager.getConf(CONFIG_SETTINGS).items()
    
    def getByName(self, name):
        return self.parent.configManager.getConf(CONFIG_SETTINGS).getItem(name, None)
    
    def setByName(self, name, value):
        ##### TODO: Perhaps check for type mismatch?
        try:
            self.parent.configManager.getConf(CONFIG_SETTINGS).setItem(name, value)
            return True
            
        except Exception as e:
            return False
            
    def has(self, name):
        if not self.getByName(name) == None:
            return True
        
        return False
