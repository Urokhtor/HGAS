__author__ = 'Urokhtor'

import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

tmp = FEET.createSource()
tmp["source"] = {}
tableMapping = ["Name", "Device", "Action", "Events", "Is permanent", ""]
inputMapping = [{"element": "input", "type": "text"}, {"element": "select"}, {"element": "select"}, {"element": "input", "type": "text"}, {"element": "input", "type": "checkbox"}]

mainContainer = FEET.createMainContainer(tmp["source"])
form = FEET.createForm(mainContainer, "taskmanagementForm")
viewTable = FEET.createViewTable(form, "Task management:")
childTbody = JFET.findElementById(viewTable, "tableRows")
hiddenInput = FEET.createHiddenInput(childTbody, "taskId", "taskId")

FEET.fillViewTable(childTbody, "task", tableMapping, inputMapping)

buttonRow = JFET.findElementById(viewTable, "buttonRow")
buttons = ["Save", "Remove"]
FEET.createButtonRowButtons(buttonRow, buttons, form["id"], True)

f = open("Conf/Website/taskmanagementform.json", "w+")
json.dump(tmp, f, indent = 4)
f.close()