
class JSONFrontEndTool:
    
    def addChild(base, element):
        """
            Adds a new element to the base object, incrementing the child element count. Once it's done,
            it then returns the newly created child object.
        """
        
        tmp = {}
        tmp["element"] = element
        
        if not "childcount" in base: base["childcount"] = 0
        
        base["childcount"] += 1
        base["child" + str(base["childcount"])] = tmp
        
        return tmp
    
    def addChildObject(base, object):
        """
            Adds a new child object to the base object.
        """
        
        if not "childcount" in base: base["childcount"] = 0
        
        base["childcount"] += 1
        base["child" + str(base["childcount"])] = object
        
        return object
    
    def addParameter(base, key, value):
        """
            Adds a new parameter to the JSON object passed to the method.
        """
        
        base[key] = value
        
        return base
    
    def findElementById(base, id):
        """
            Recursively searches for an object that contains the given ID. Returns only the first occurence
            of the ID.
        """
        
        return JSONFrontEndTool.findElementByKeyValue(base, "id", id)
        
    def findElementByKeyValue(base, key, value):
        if key in base:
            if base[key] == value:
                return base
        
        if not "childcount" in base:
            return None
        
        if base["childcount"] == 0:
            return None
        
        if base["childcount"] > 0:
            for i in range(0, base["childcount"]):
                tmp = JSONFrontEndTool.findElementById(base["child"+str(i+1)], value)
                
                if tmp: return tmp
        
        return None
        