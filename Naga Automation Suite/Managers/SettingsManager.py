<<<<<<< HEAD
from Managers.BaseManager import BaseManager

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
=======
from Managers.BaseManager import BaseManager

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
>>>>>>> cbd3bf5dabe3e29b4f5be216a7b15ab66f6732ef
        