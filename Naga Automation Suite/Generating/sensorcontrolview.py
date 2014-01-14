import sys
sys.path.append("G:\\Programming\Python\\Naga-Automation-Suite\\Naga Automation Suite")

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

try:
    f = open("Conf/Website/sensorcontrolview.json", "r")
    tmp = json.load(f)
    f.close()

except:
    tmp = FEET.createSource()

tmp["source"] = {}
mainContainer = FEET.createMainContainer(tmp["source"])

tableMapping = ["Name", "Type", "Client", "Index", "Last reading", "Last update"]

childDiv = FEET.createLeftButtonColumn(mainContainer, "Select sensorcontrol:")
childDivRight = FEET.createRightDivContainer(mainContainer)
childDivViewTable = FEET.createViewTable(childDivRight, "Sensorcontrol info")
childTbody = JFET.findElementById(childDivViewTable, "tableRows")

# REPLACE THE CODE BELOW WITH FEET ROUTINES
j = 0
for i in range(0, int(len(tableMapping)/2)):
    childTr2 = JFET.addChild(childTbody, "tr")

    childTd = JFET.addChild(childTr2, "td")
    JFET.addParameter(childTd, "className", "labelCell")
    JFET.addParameter(childTd, "innerHTML", tableMapping[j])
    childTd2 = JFET.addChild(childTr2, "td")
    JFET.addParameter(childTd2, "className", "dataCell")
    
    mapping = tableMapping[j]
    
    if mapping.find(" ") != -1:
        parts = mapping.split(" ")
        mapping = ""
        
        for part in parts:
            mapping += part[:1].upper() + part[1:]
    
    JFET.addParameter(childTd2, "id", "sensorInfo" + mapping)
    j += 1
    childTd3 = JFET.addChild(childTr2, "td")
    JFET.addParameter(childTd3, "className", "labelCell")
    JFET.addParameter(childTd3, "innerHTML", tableMapping[j])
    childTd4 = JFET.addChild(childTr2, "td")
    JFET.addParameter(childTd4, "className", "dataCell")
    
    mapping = tableMapping[j]
    
    if mapping.find(" ") != -1:
        parts = mapping.split(" ")
        mapping = ""
        
        for part in parts:
            mapping += part[:1].upper() + part[1:]
    
    JFET.addParameter(childTd4, "id", "sensorInfo" + mapping)
    j += 1

# Buttonrow.
childTableViewTable3 = JFET.addChild(childDivViewTable, "table")
JFET.addParameter(childTableViewTable3, "className", "fullWidth")
childDivButtonRow = JFET.addChild(childTableViewTable3, "div")
JFET.addParameter(childDivButtonRow, "className", "buttonRow")

# Sensor plot container.
childTableViewTable4 = JFET.addChild(childDivRight, "table")
childDivPlots = JFET.addChild(childTableViewTable4, "div")
JFET.addParameter(childDivPlots, "id", "sensorPlotsHolder")

f = open("Conf/Website/sensorcontrolview.json", "w")
json.dump(tmp, f, indent = 4)
f.close()