from Controllers.FormController import FormController
from Constants import *

class SensorcontrolFormController(FormController):
    
    def handleSubmit(parent, request, response):
        if request["action"] == FORM_ADD:
            return SensorcontrolFormController.handleAdd(parent, request, response)
        
        elif request["action"] == FORM_REMOVE:
            return SensorcontrolFormController.handleRemove(parent, request, response)
        
    def validate(parent, request, reject):
        if not "action" in request:
            return '{"' + KEY_REJECT + '": {"id": "action", "reason": "Action was not supplied"}}'
    
        if not "object" in request:
            return '{"' + KEY_REJECT + '": {"id": "object", "reason": "Task object was not supplied"}}'
            
        object = request["object"]
            
    def handleAdd(parent, request, response):
        object = request["object"]
        
        if parent.sensorcontrolManager.hasByName(object["sensorcontrolManagementName"]):
            return '{"' + KEY_ERROR + '": ' + str(SENSORCONTROL_EXISTS_ERROR) + '}'
        
        sensorcontrol = parent.sensorcontrolManager.createTask(object["sensorcontrolManagementName"], "write", object["taskInfoAction"], object["taskInfoDevice"], object["taskInfoIsPermanent"], object["taskInfoEvents"])
        response = parent.sensorcontrolManager.insert(sensorcontrol)
        
        if "error" in response: return response
        elif response: return '{"' + KEY_RESPONSE + '": ' + str(INSERT_SENSORCONTROL_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_ADD_SENSORCONTROL_ERROR) + '}'
    
    def handleRemove(parent, request, response):
        object = request["object"]
        
        if not parent.sensorcontrolManager.has(int(object["sensorcontrolId"])):
            return '{"' + KEY_ERROR + '": ' + str(SENSORCONTROL_DOESNT_EXIST_ERROR) + '}'
            
        response = parent.sensorcontrolManager.removeById(int(object["sensorcontrolId"]))
        
        if response: return '{"' + KEY_RESPONSE + '": ' + str(REMOVE_SENSORCONTROL_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_REMOVE_SENSORCONTROL_ERROR) + '}'
    