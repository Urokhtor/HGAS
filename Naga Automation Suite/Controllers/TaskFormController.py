from Controllers.FormController import FormController
from Constants import *

class TaskFormController(FormController):
    
    def handleSubmit(parent, request, response):
        if request["action"] == FORM_ADD:
            return TaskFormController.handleAdd(parent, request, response)
        
        elif request["action"] == FORM_REMOVE:
            return TaskFormController.handleRemove(parent, request, response)
        
    def validate(parent, request, reject):
        if not "action" in request:
            return '{"' + KEY_REJECT + '": {"id": "action", "reason": "Action was not supplied"}}'
    
        if not "object" in request:
            return '{"' + KEY_REJECT + '": {"id": "object", "reason": "Task object was not supplied"}}'
            
        object = request["object"]
        
        if not "taskInfoName" in object:
            return '{"' + KEY_REJECT + '": {"id": "taskInfoName", "reason": "Task\'s name was not supplied"}}'
        
        if not "taskInfoDevice" in object:
            return '{"' + KEY_REJECT + '": {"id": "taskInfoDevice", "reason": "Task\'s device was not supplied"}}'
        
        if not "taskInfoAction" in object:
            return '{"' + KEY_REJECT + '": {"id": "taskInfoAction", "reason": "Task\'s action was not supplied"}}'
        
        if not "taskInfoEvents" in object:
            return '{"' + KEY_REJECT + '": {"id": "taskInfoEvents", "reason": "Task\'s events were not supplied"}}'
        
        if not "taskInfoIsPermanent" in object:
            return '{"' + KEY_REJECT + '": {"id": "taskInfoIsPermanent", "reason": "Task\'s is permanent was not supplied"}}'
        
        if request["action"] == FORM_REMOVE and not "id" in object:
            return '{"' + KEY_REJECT + '": {"id": "object", "reason": "Task id was not supplied for remove action"}}'
        
        try:
            object["taskInfoAction"] = int(object["taskInfoAction"])
        except ValueError:
            # Reject because wrong type
            pass
            
        try:
            object["taskInfoIsPermanent"] = bool(object["taskInfoIsPermanent"])
        except ValueError:
            # Reject because wrong type
            pass
            
    def handleAdd(parent, request, response):
        object = request["object"]
        
        if parent.taskManager.hasTaskByName(object["taskManagementName"]):
            return '{"' + KEY_ERROR + '": ' + str(TASK_EXISTS_ERROR) + '}'
            
        task = parent.taskManager.createTask(object["taskManagementName"], "write", object["taskManagementExecuteActionList"], object["taskManagementDeviceList"], object["taskManagementIsTemporaryCheckbox"], object["taskManagementSchedules"])
        response = parent.taskManager.insertTask(task)
        
        if "error" in response: return response
        elif response: return '{"' + KEY_RESPONSE + '": ' + str(INSERT_TASK_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_ADD_TASK_ERROR) + '}'
    
    def handleRemove(parent, request, response):
        object = request["object"]
        
        if not parent.taskManager.hasTask(int(object["taskId"])):
            return '{"' + KEY_ERROR + '": ' + str(TASK_DOESNT_EXIST_ERROR) + '}'
            
        response = parent.taskManager.removeTaskById(int(object["taskId"]))
        
        if response: return '{"' + KEY_RESPONSE + '": ' + str(REMOVE_TASK_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_REMOVE_TASK_ERROR) + '}'
        