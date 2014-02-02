
class TypeMapper:

    def getSensorTypeMap():
        return [(0, "default"),
                (1, "temperature"),
                (2, "humidity"),
                (3, "ultrasound"),
                (4, "BMP085 temperature"),
                (5, "BMP085 pressure"),
                (6, "BMP085 altitude")] # This shouldn't probably be hardcoded.

    def getDeviceTypeMap():
        return [(0, "Lights"),
                (1, "Pump")]

    def getTaskActionMap():
        return [(204, "On"),
                (205, "Off"),
                (201, "Toggle")]

    def getClientTypeMap():
        return [(600, "Arduino"),
                (601, "Telldus")]

    def mapSensorTypeToString(typeId):
        typeMap = ["default", "temperature", "humidity", "ultrasound", "BMP085 temperature", "BMP085 pressure", "BMP085 altitude"] # This shouldn't probably be hardcoded.
        
        if typeId >= len(typeMap) or typeId < 0:
            return None
            
        return typeMap[typeId]
        
    def mapSensorTypeToUnit(typeId):
        unitMap = ["", "C", "%", "cm", "C", "hPa", "m"]
        
        if typeId >= len(unitMap) or typeId < 0:
            return None
        
        return unitMap[typeId]

    def mapDeviceState(state):
        stateMap = ["Off", "On"]

        if state >= len(stateMap) or state < 0:
            return None

        return stateMap[state]

    def mapBoolean(bool):
        boolMap = ["No", "Yes"]

        if bool is True:
            return boolMap[1]

        elif bool is False:
            return boolMap[0]

        else:
            return ""

    def mapClientType(typeId):
        clientMap = {600: "Arduino", 601: "Telldus"}

        if typeId in clientMap:
            return clientMap[typeId]

    def mapTaskAction(actionId):
        actionMap = {204: "On", 205: "Off"}

        if actionId in actionMap:
            return actionMap[actionId]