from Controllers.ViewController import ViewController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Constants import *
import json

class NASMenuViewController(ViewController):
    
    def handleRequest(parent, request, response):
        """
        
        """
        
        f = open("Conf/Website/menu.json", "r")
        tmp = json.load(f)
        f.close()

        f = open("Conf/Website/menuElements.json", "r")
        menutmp = json.load(f)
        menuelements = menutmp["source"]["menu"]
        submenuelements = menutmp["source"]["submenu"]
        f.close()
        
        ul = JFET.findElementById(tmp["source"], "menuul")
        submenu = JFET.findElementById(tmp["source"], "submenu")
        
        # Process the main menu level.
        for i in range(1, menuelements["childcount"]+1):
            child = menuelements["child"+str(i)]
            li = JFET.addChild(ul, "li")
            JFET.addParameter(li, "className", "menu")
            JFET.addChildObject(li, child)
        
        for i in range(1, submenuelements["childcount"]+1):
            child = submenuelements["child"+str(i)]
            JFET.addChildObject(submenu, child)

        return json.dumps(tmp)
        