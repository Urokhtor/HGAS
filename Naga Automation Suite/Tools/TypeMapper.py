
class TypeMapper:

    def getSensorTypeMap():
        return ["default", "temperature", "humidity", "ultrasound", "BMP085 temperature", "BMP085 pressure", "BMP085 altitude"] # This shouldn't probably be hardcoded.

    def getDeviceTypeMap():
        return ["Lights", "Pump"]

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