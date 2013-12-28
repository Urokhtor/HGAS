import sys
sys.path.append("/home/urokhtor/Documents/Garden automation/Naga Automation System")

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
import json

f = open("Conf/Website/sensorview.json", "r")
tmp = json.load(f)
f.close()

mainContainer = JFET.findElementById(tmp["source"], "mainContainer")
tableMapping = ["Name", "Type", "Client", "Index", "Last reading", "Last update"]

# Left part.
childDiv = JFET.addChild(mainContainer, "div")
JFET.addParameter(childDiv, "id", "leftSensorColumn")
JFET.addParameter(childDiv, "className", "leftcolumn")

#childTable = JFET.addChild(childDiv, "table")
childDivSelect = JFET.addChild(childDiv, "div")
childH3 = JFET.addChild(childDivSelect, "h3")
JFET.addParameter(childH3, "innerHTML", "Select sensor:")

childUl = JFET.addChild(childDiv, "ul")
JFET.addParameter(childUl, "id", "sensorUL")
JFET.addParameter(childUl, "className", "leftcolumnul")

# Right part.
childDivRight = JFET.addChild(mainContainer, "div")
JFET.addParameter(childDivRight, "id", "rightSensorColumn")
JFET.addParameter(childDivRight, "className", "rightcolumn")

childDivViewTable = JFET.addChild(childDivRight, "div")
JFET.addParameter(childDivViewTable, "className", "viewTable")

# Thead.
childTableViewTable = JFET.addChild(childDivViewTable, "table")
JFET.addParameter(childTableViewTable, "className", "fullWidth")

childThead = JFET.addChild(childTableViewTable, "thead")
childTr = JFET.addChild(childThead, "tr")
childTh = JFET.addChild(childTr, "th")
JFET.addParameter(childTh, "className", "headCell")
JFET.addParameter(childTh, "innerHTML", "Sensor info:")

# Actual table.
childTableViewTable2 = JFET.addChild(childDivViewTable, "table")
JFET.addParameter(childTableViewTable2, "className", "fullWidth")
childTbody = JFET.addChild(childTableViewTable2, "tbody")

j = 0
for i in range(0, 3):
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

f = open("Conf/Website/sensorview_test.json", "w")
json.dump(tmp, f, indent = 4)
f.close()