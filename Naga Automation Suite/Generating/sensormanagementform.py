__author__ = 'Urokhtor'

import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

tmp = FEET.createSource()
tmp["source"] = {}
tableMapping = ["Name", "Type", "Client", "Index"]
inputMapping = [{"element": "input", "type": "text"}, {"element": "select"}, {"element": "select"}, {"element": "input", "type": "text"}]

mainContainer = FEET.createMainContainer(tmp["source"])
form = FEET.createForm(mainContainer, "sensormanagementForm")
viewTable = FEET.createViewTable(form, "Sensor management:")
childTbody = JFET.findElementById(viewTable, "tableRows")
hiddenInput = FEET.createHiddenInput(childTbody, "sensorId", "sensorId")

FEET.fillViewTable(childTbody, "sensor", tableMapping, inputMapping)

buttonRow = JFET.findElementById(viewTable, "buttonRow")
buttons = ["Save", "Remove"]
FEET.createButtonRowButtons(buttonRow, buttons, form["id"], True)

f = open("Conf/Website/sensormanagementform.json", "w+")
json.dump(tmp, f, indent = 4)
f.close()