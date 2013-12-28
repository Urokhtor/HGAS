
class TypeMapper:
    
    def mapSensorTypeToString(typeId):
        typeMap = ["default", "temperature", "humidity", "ultrasound", "BMP085 temperature", "BMP085 pressure", "BMP085 altitude"]
        
        if typeId >= len(typeMap) or typeId < 0:
            return None
            
        return typeMap[typeId]
        
    def mapSensorTypeToUnit(typeId):
        unitMap = ["", "C", "%", "cm", "C", "hPa", "m"]
        
        if typeId >= len(unitMap) or typeId < 0:
            return None
        
        return unitMap[typeId]
