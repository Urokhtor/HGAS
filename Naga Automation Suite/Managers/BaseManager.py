from Constants import CONFIG_SETTINGS

class BaseManager:
    
    def __init__(self, parent):
        self.parent = parent
    
    def getNextId(self):
        currentId = self.parent.configManager.getConf(CONFIG_SETTINGS).getItem("idsequence", None)
        nextId = currentId + 1
        self.parent.configManager.getConf(CONFIG_SETTINGS).setItem("idsequence", nextId)
        return nextId
    
    def create(self):
        raise NotImplementedError("Create was not implemented by a class inheriting from BaseManager")