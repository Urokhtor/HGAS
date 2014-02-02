from Managers.BaseManager import BaseManager
from Scheduler import Task
from Constants import *

class TaskManager(BaseManager):

    def __init__(self, parent):
        BaseManager.__init__(self, parent, CONFIG_CORE, "tasks")

    def create(self, name, taskType, action, device, isPermanent, schedules):
        task = {}
        task["name"] = name
        task["type"] = taskType
        task["action"] = action
        task["deviceid"] = device
        task["ispermanent"] = isPermanent
        task["schedules"] = schedules.replace(" ", "").split(",")
        task["id"] = self.getNextId()
        
        return task
    
    def insert(self, task):
        if self.has(task["id"]):
            return '{"' + KEY_ERROR + '": ' + str(TASK_EXISTS_ERROR) + '}'

        if task["ispermanent"]:
            self.parent.taskManager.add(task)

        return self.parent.taskManager.insertToScheduler(task)

    def insertToScheduler(self, task):
        if self.parent.scheduler.taskManager.hasTask(task["name"]):
            self.parent.scheduler.taskManager.removeTask(task["name"])

        action = None
        device = self.parent.deviceManager.getById(task["deviceid"])

        if device is None: '{"' + KEY_ERROR + '": ' + str(TASK_EXISTS_ERROR) + '}' # Replace with some "device not found" thing.

        if task["action"] == SEND_ENABLE:
            action = (device["clientid"], self.parent.protocol.writeEnable(device))

        elif task["action"] == SEND_DISABLE:
            action = (device["clientid"], self.parent.protocol.writeDisable(device))

        elif task["action"] == SEND_WRITE:
            action = (device["clientid"], self.parent.protocol.write(device))

        newTask = Task(task["name"], action, 1, self.parent.connection.send, task["ispermanent"])

        # TODO: IN FUTURE PERHAPS WE WANT TO ADD INTERVALS TOO
        newTask.scheduleByEvents(task["schedules"])

        success = self.parent.scheduler.taskManager.addTask(newTask)
        print(success)
        return '{"' + KEY_RESPONSE + '": ' + str(INSERT_TASK_SUCCESS) + '}'
    
    def remove(self, task):
        print(task)
        if not self.has(task["id"]):
            return '{"' + KEY_ERROR + '": ' + str(TASK_DOESNT_EXIST_ERROR) + '}'
            
        tasks = self.parent.configManager.getConf(CONFIG_CORE).getItem("tasks", None)
        tasks.remove(task)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("tasks", tasks)
        success = self.parent.scheduler.taskManager.removeTask(task["name"])
        print(success)
        return '{"' + KEY_RESPONSE + '": ' + str(REMOVE_TASK_SUCCESS) + '}'
    
    def removeById(self, id):
        return self.remove(self.getById(id))
