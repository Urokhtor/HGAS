__author__ = 'Urokhtor'

import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET

tmp = FEET.createSource()
mainContainer = FEET.createMainContainer(tmp["source"])

tableMapping = ["Name", "Device", "Action", "Events", "Is permanent", ""]

childDiv = FEET.createLeftButtonColumn(mainContainer, "Select task:", "taskUL")
childDivRight = FEET.createRightDivContainer(mainContainer)
childDivViewTable = FEET.createViewTable(childDivRight, "Task info:", "taskView")
childTbody = JFET.findElementById(childDivViewTable, "tableRows")

FEET.fillViewTable(childTbody, "task", tableMapping)

buttonRow = JFET.findElementById(childDivViewTable, "buttonRow")
buttons = ["Modify"]
FEET.createButtonRowButtons(buttonRow, buttons, "", False, "Task")

FEET.saveFile(tmp, "taskview")