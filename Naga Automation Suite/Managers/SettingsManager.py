from Managers.BaseManager import BaseManager
from Constants import CONFIG_SETTINGS

class SettingsManager(BaseManager):

    def __init__(self, parent):
        BaseManager.__init__(self, parent, CONFIG_SETTINGS, "settings")

    def getValueByName(self, name):
        settings = self.parent.configManager.getConf(CONFIG_SETTINGS).getItem("settings", None)

        for setting in settings:
            if setting["name"] == name:
                return setting["value"]

        return None
    
    def setByName(self, name, value):
        ##### TODO: Perhaps check for type mismatch?
        try:
            settings = self.parent.configManager.getConf(CONFIG_SETTINGS).getItem("settings", None)

            for setting in settings:
                if setting["name"] == name:
                    setting["value"] = value
                    self.parent.configManager.getConf(CONFIG_SETTINGS).setItem("settings", settings)
                    return True
            
        except Exception as e:
            return False