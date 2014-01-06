import sys
sys.path.append("G:\\Programming\Python\\Naga-Automation-Suite\\Naga Automation Suite")

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
import json

f = open("Conf/Website/menuElements.json", "r")
tmp = json.load(f)
f.close()

submenu = JFET.findElementById(tmp["source"]["submenu"], "submenu")
submenu = {}
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
    #childInput = JFET.addChild(childLi, "a")
    JFET.addParameter(childInput, "type", "button")
    JFET.addParameter(childInput, "className", "menu submenubutton")
    JFET.addParameter(childInput, "id", section[i] + "Selectbutton")
    JFET.addParameter(childInput, "value", value[i])
    #JFET.addParameter(childInput, "innerHTML", value[i])
    #JFET.addParameter(childInput, "className", "submenubutton")
    #JFET.addParameter(childInput, "href", "/test/" + value[i].lower())
    
    # Generate management page for first four tabs.
    if i <= 3:
        childLi = JFET.addChild(childUl, "li")
        JFET.addParameter(childLi, "className", "menu")
    
        childInput = JFET.addChild(childLi, "input")
        #childInput = JFET.addChild(childLi, "a")
        JFET.addParameter(childInput, "type", "button")
        JFET.addParameter(childInput, "className", "submenubutton")
        JFET.addParameter(childInput, "id", section[i] + "managementSelectbutton")
        JFET.addParameter(childInput, "value", "Management")
        #JFET.addParameter(childInput, "innerHTML", "Management")
        #JFET.addParameter(childInput, "className", "submenubutton")
        #JFET.addParameter(childInput, "href", "/test/management")

tmp["source"]["submenu"] = submenu

f = open("Conf/Website/menuElements.json", "w")
json.dump(tmp, f, indent = 4)
f.close()
