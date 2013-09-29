<<<<<<< HEAD
from Controllers.FormController import FormController
from Constants import *

class SensorFormController(FormController):
    
    def handleSubmit(parent, request, response):
        if request["action"] == FORM_ADD:
            return SensorFormController.handleAdd(parent, request, response)
        
        elif request["action"] == FORM_REMOVE:
            return SensorFormController.handleRemove(parent, request, response)
        
    def validate(parent, request, reject):
        if not "action" in request:
            return '{"' + KEY_REJECT + '": {"id": "action", "reason": "Action was not supplied"}}'
        
        if not "object" in request:
            return '{"' + KEY_REJECT + '": {"id": "object", "reason": "Sensor object was not supplied"}}'
            
        object = request["object"]
        
        if not "sensorName" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorName", "reason": "Sensor\'s name was not supplied"}}'
        
        if not "sensorType" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorType", "reason": "Sensor\'s type was not supplied"}}'
            
        if not "sensorClient" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorType", "reason": "Sensor\'s clientname was not supplied"}}'
        
        if not "sensorIndex" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorType", "reason": "Sensor\'s index was not supplied"}}'
        
        if request["action"] == FORM_REMOVE and not "id" in object:
            return '{"' + KEY_REJECT + '": {"id": "object", "reason": "Sensor id was not supplied for remove action"}}'
        
        
        try:
            object["sensorType"] = int(object["sensorType"])
        except ValueError:
            # Reject because wrong type
            pass
            
        try:
            object["sensorIndex"] = int(object["sensorIndex"])
        except ValueError:
            # Reject because wrong type
            pass
        
        try:
            object["sensorId"] = int(object["sensorId"])
        except ValueError:
            pass
        
        return True
    
    def handleAdd(parent, request, response):
        object = request["object"]
        
        if parent.deviceManager.hasSensorByName(object["sensorName"]):
            # Return error telling sensor already exists with that name.
            return '{"' + KEY_ERROR + '": ' + str(SENSOR_EXISTS_ERROR) + '}'
        
        sensor = parent.deviceManager.createSensor(object["sensorName"], object["sensorType"], object["sensorClient"], object["sensorIndex"])
        response = parent.deviceManager.insertSensor(sensor)
        
        if "error" in response: return response
        elif response: return '{"' + KEY_RESPONSE + '": ' + str(INSERT_SENSOR_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_ADD_SENSOR_ERROR) + '}'
    
    def handleRemove(parent, request, response):
        object = request["object"]
        
        if not parent.deviceManager.hasSensor(int(object["sensorId"])):
            return '{"' + KEY_ERROR + '": ' + str(SENSOR_DOESNT_EXIST_ERROR) + '}'
            
        response = parent.deviceManager.removeSensorById(int(object["sensorId"]))
        
        if response: return '{"' + KEY_RESPONSE + '": ' + str(REMOVE_SENSOR_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_REMOVE_SENSOR_ERROR) + '}'
=======
from Controllers.FormController import FormController
from Constants import *

class SensorFormController(FormController):
    
    def handleSubmit(parent, request, response):
        if request["action"] == FORM_ADD:
            return SensorFormController.handleAdd(parent, request, response)
        
        elif request["action"] == FORM_REMOVE:
            return SensorFormController.handleRemove(parent, request, response)
        
    def validate(parent, request, reject):
        if not "action" in request:
            return '{"' + KEY_REJECT + '": {"id": "action", "reason": "Action was not supplied"}}'
        
        if not "object" in request:
            return '{"' + KEY_REJECT + '": {"id": "object", "reason": "Sensor object was not supplied"}}'
            
        object = request["object"]
        
        if not "sensorName" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorName", "reason": "Sensor\'s name was not supplied"}}'
        
        if not "sensorType" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorType", "reason": "Sensor\'s type was not supplied"}}'
            
        if not "sensorClient" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorType", "reason": "Sensor\'s clientname was not supplied"}}'
        
        if not "sensorIndex" in object:
            return '{"' + KEY_REJECT + '": {"id": "sensorType", "reason": "Sensor\'s index was not supplied"}}'
        
        if request["action"] == FORM_REMOVE and not "id" in object:
            return '{"' + KEY_REJECT + '": {"id": "object", "reason": "Sensor id was not supplied for remove action"}}'
        
        
        try:
            object["sensorType"] = int(object["sensorType"])
        except ValueError:
            # Reject because wrong type
            pass
            
        try:
            object["sensorIndex"] = int(object["sensorIndex"])
        except ValueError:
            # Reject because wrong type
            pass
        
        try:
            object["sensorId"] = int(object["sensorId"])
        except ValueError:
            pass
        
        return True
    
    def handleAdd(parent, request, response):
        object = request["object"]
        
        if parent.deviceManager.hasSensorByName(object["sensorName"]):
            # Return error telling sensor already exists with that name.
            return '{"' + KEY_ERROR + '": ' + str(SENSOR_EXISTS_ERROR) + '}'
        
        sensor = parent.deviceManager.createSensor(object["sensorName"], object["sensorType"], object["sensorClient"], object["sensorIndex"])
        response = parent.deviceManager.insertSensor(sensor)
        
        if "error" in response: return response
        elif response: return '{"' + KEY_RESPONSE + '": ' + str(INSERT_SENSOR_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_ADD_SENSOR_ERROR) + '}'
    
    def handleRemove(parent, request, response):
        object = request["object"]
        
        if not parent.deviceManager.hasSensor(int(object["sensorId"])):
            return '{"' + KEY_ERROR + '": ' + str(SENSOR_DOESNT_EXIST_ERROR) + '}'
            
        response = parent.deviceManager.removeSensorById(int(object["sensorId"]))
        
        if response: return '{"' + KEY_RESPONSE + '": ' + str(REMOVE_SENSOR_SUCCESS) + '}'
        else: return '{"' + KEY_ERROR + '": ' + str(COULD_NOT_REMOVE_SENSOR_ERROR) + '}'
>>>>>>> cbd3bf5dabe3e29b4f5be216a7b15ab66f6732ef
        