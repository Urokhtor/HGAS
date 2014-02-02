__author__ = 'Urokhtor'

import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET

tmp = FEET.createSource()
mainContainer = FEET.createMainContainer(tmp["source"])

tableMapping = ["Name", "Type", "Address", ""]

childDiv = FEET.createLeftButtonColumn(mainContainer, "Select client:", "clientUL")
childDivRight = FEET.createRightDivContainer(mainContainer)
childDivViewTable = FEET.createViewTable(childDivRight, "Client info:", "clientView")
childTbody = JFET.findElementById(childDivViewTable, "tableRows")

FEET.fillViewTable(childTbody, "client", tableMapping)

buttonRow = JFET.findElementById(childDivViewTable, "buttonRow")
buttons = ["Modify"]
FEET.createButtonRowButtons(buttonRow, buttons, "", False, "Client")

FEET.saveFile(tmp, "clientview")