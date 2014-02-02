
import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET

tmp = FEET.createSource()
mainContainer = FEET.createMainContainer(tmp["source"])

tableMapping = ["Name", "Type", "Client", "Index", "Last reading", "Last update"]

childDiv = FEET.createLeftButtonColumn(mainContainer, "Select sensor:", "sensorUL")
childDivRight = FEET.createRightDivContainer(mainContainer)
childDivViewTable = FEET.createViewTable(childDivRight, "Sensor info:", "sensorView")
childTbody = JFET.findElementById(childDivViewTable, "tableRows")

FEET.fillViewTable(childTbody, "sensorInfo", tableMapping)

buttonRow = JFET.findElementById(childDivViewTable, "buttonRow")
buttons = ["Modify"]
FEET.createButtonRowButtons(buttonRow, buttons, "", False, "Sensor")

# Sensor plot container.
childTableViewTable4 = JFET.addChild(childDivRight, "table")
childDivPlots = JFET.addChild(childTableViewTable4, "div")
JFET.addParameter(childDivPlots, "id", "sensorPlotsHolder")

FEET.saveFile(tmp, "sensorview")