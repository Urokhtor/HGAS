import sys
sys.path.append("/home/urokhtor/Documents/Garden automation/Naga Automation System")

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
import json

f = open("Conf/Website/menuElements.json", "r")
tmp = json.load(f)
f.close()

submenu = JFET.findElementById(tmp["source"]["submenu"], "submenu")
section = ["sensor", "device", "task", "sensorcontrol", "eventlog", "settings", "documentation"]
value = ["Info", "Devices", "Tasks", "Sensorcontrol", "Eventlog", "Settings", "Docs"]

for i in range(0, 7):
    childDiv = JFET.addChild(submenu, "div")
    JFET.addParameter(childDiv, "id", "submenu_" + section[i])
    JFET.addParameter(childDiv, "className", "submenu")
    JFET.addParameter(childDiv, "style", "display:none;")

    childUl = JFET.addChild(childDiv, "ul")
    JFET.addParameter(childUl, "className", "menu")
    
    childLi = JFET.addChild(childUl, "li")
    JFET.addParameter(childLi, "className", "menu")
    
    childInput = JFET.addChild(childLi, "input")
    JFET.addParameter(childInput, "type", "button")
    JFET.addParameter(childInput, "id", section[i] + "Page")
    JFET.addParameter(childInput, "value", value[i])
    JFET.addParameter(childInput, "className", "submenubutton")
    
    # Generate management page for first four tabs.
    if i <= 3:
        childLi = JFET.addChild(childUl, "li")
        JFET.addParameter(childLi, "className", "menu")
    
        childInput = JFET.addChild(childLi, "input")
        JFET.addParameter(childInput, "type", "button")
        JFET.addParameter(childInput, "id", section[i] + "managementPage")
        JFET.addParameter(childInput, "value", "Management")
        JFET.addParameter(childInput, "className", "submenubutton")

f = open("Conf/Website/menuElements_test.json", "w")
json.dump(tmp, f, indent = 4)
f.close()