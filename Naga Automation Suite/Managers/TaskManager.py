from Managers.BaseManager import BaseManager
from Scheduler import Task
from Constants import *

class TaskManager(BaseManager):

    def createTask(self, name, type, action, device, isTemporary, schedules):
        task = {}
        task["name"] = name
        task["type"] = type
        task["action"] = action
        task["device"] = device
        task["ispermanent"] = not isTemporary # Bit ugly, but it makes sense to display isTemporary to the user but handle it the other way around.
        task["schedules"] = schedules.replace(" ", "").split(",")
        task["id"] = self.getNextId()
        
        return task
    
    def insertTask(self, task):
        if self.hasTask(task["id"]):
            return '{"' + KEY_ERROR + '": ' + str(TASK_EXISTS_ERROR) + '}'
            
        tasks = self.parent.configManager.getConf(CONFIG_CORE).getItem("tasks", None)
        tasks.append(task)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("tasks", tasks)
        
        if self.parent.scheduler.taskManager.hasTask(task["name"]):
            self.parent.scheduler.taskManager.removeTask(task["name"])
        
        newTask = Task(task["name"], task["type"], task["action"], task["device"], 1, self.parent.connection.send, task["ispermanent"])
        success = self.parent.scheduler.taskManager.addTask(newTask)
        print(success)
        return '{"' + KEY_RESPONSE + '": ' + str(INSERT_TASK_SUCCESS) + '}'
    
    def removeTask(self, task):
        if not self.hasTask(task["id"]):
            return '{"' + KEY_ERROR + '": ' + str(TASK_DOESNT_EXIST_ERROR) + '}'
            
        tasks = self.parent.configManager.getConf(CONFIG_CORE).getItem("tasks", None)
        tasks.remove(task)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("tasks", tasks)
        success = self.parent.scheduler.taskManager.removeTask(task["name"])
        print(success)
        return '{"' + KEY_RESPONSE + '": ' + str(REMOVE_TASK_SUCCESS) + '}'
    
    def removeTaskById(self, id):
        return self.removeTask(self.getTaskById(id))
    
    def getTasks(self):
        return self.parent.configManager.getConf(CONFIG_CORE).getItem("tasks", None)
    
    def getTaskById(self, id):
        tasks = self.parent.configManager.getConf(CONFIG_CORE).getItem("tasks", None)
        
        if not id == None:
            for task in tasks:
                if task["id"] == id:
                    return task
        
        return None
    
    def hasTask(self, id):
        tasks = self.parent.configManager.getConf(CONFIG_CORE).getItem("tasks", None)
        
        for task in tasks:
            if task["id"] == id:
                return True
        
        return False
    
    def hasTaskByName(self, name):
        tasks = self.parent.configManager.getConf(CONFIG_CORE).getItem("tasks", None)
        
        for task in tasks:
            if task["name"] == name:
                return True

        return False
