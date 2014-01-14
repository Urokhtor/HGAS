__author__ = 'Urokhtor'

import sys
sys.path.append("G:\\Programming\Python\\Naga-Automation-Suite\\Naga Automation Suite")

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

tmp = FEET.createSource()
tmp["source"] = {}
tableMapping = ["Name", "Type", "Client", "Index"]
inputMapping = [{"element": "input", "type": "text"}, {"element": "select"}, {"element": "select"}, {"element": "input", "type": "text"}]

mainContainer = FEET.createMainContainer(tmp["source"])
form = FEET.createForm(mainContainer, "devicemanagementForm")
viewTable = FEET.createViewTable(form, "Device management:")
childTbody = JFET.findElementById(viewTable, "tableRows")
hiddenInput = FEET.createHiddenInput(childTbody, "deviceId", "deviceId")

FEET.fillViewTable(childTbody, "device", tableMapping, inputMapping)

buttonRow = JFET.findElementById(viewTable, "buttonRow")
buttons = ["Save", "Remove"]
FEET.createButtonRowButtons(buttonRow, buttons)

f = open("Conf/Website/devicemanagementform.json", "w+")
json.dump(tmp, f, indent = 4)
f.close()