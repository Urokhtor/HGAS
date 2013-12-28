from importlib import import_module
from imp import reload
from sys import modules

class ModuleManager:

    def __init__(self, parent):
        self.modules = {}
        self.parent = parent
    
    def getModule(self, moduleName):
        """
            Searches for module in loaded modules and returns it if it's found.
        """
        
        if moduleName in self.modules:
            tmp = moduleName
            if moduleName.find(".") != -1:
                tmp = moduleName.split(".", 1)[1]
            return getattr(modules[moduleName], tmp)
        
        else: return None
    
    def getModules(self):
        """
            Returns the dict storing all the loaded modules.
        """
        
        return self.modules
    
    def loadModules(self, config):
        """
            Attempts to load all the modules specified in the parent config file.
        """

        if type(config) is list:
            for obj in config:
                if not self.loadModule(obj["module"]):
                    self.parent.logging.logEvent("ModuleManager: Couldn't load module " + obj["module"], "red")

        elif type(config) is dict:
            for module in config:
                if not self.loadModule(module):
                    self.parent.logging.logEvent("ModuleManager: Couldn't load module " + module, "red")

    def loadModule(self, moduleName):
        """
            Attempts to load a module from IRCCommand subfolder and stores the module in a dict
            if it's successful.
        """
        
        if moduleName in self.modules:
            return False
        
        try:
            module = import_module(moduleName)
            self.modules[moduleName] = module
            return True
        
        except ImportError:
            return False
    
    def reloadModule(self, moduleName):
        """
            Attempts to reload a module by passing the old import object to imp.reload() which
            returns the new import object if reload was successful.
        """
        
        if moduleName in self.modules:
            self.modules[moduleName] = reload(self.modules[moduleName])
            return True
                
        else:
            return False
            