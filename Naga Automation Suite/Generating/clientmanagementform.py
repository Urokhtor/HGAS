__author__ = 'Urokhtor'

import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

tmp = FEET.createSource()
tmp["source"] = {}
tableMapping = ["Name", "Type", "Address", ""]
inputMapping = [{"element": "input", "type": "text"},
                {"element": "select"},
                {"element": "input", "type": "text"}]

mainContainer = FEET.createMainContainer(tmp["source"])
form = FEET.createForm(mainContainer, "clientmanagementForm")
viewTable = FEET.createViewTable(form, "Client management:")
childTbody = JFET.findElementById(viewTable, "tableRows")
hiddenInput = FEET.createHiddenInput(childTbody, "clientId", "clientId")

FEET.fillViewTable(childTbody, "client", tableMapping, inputMapping)

buttonRow = JFET.findElementById(viewTable, "buttonRow")
buttons = ["Save", "Remove"]
FEET.createButtonRowButtons(buttonRow, buttons, form["id"], True)

f = open("Conf/Website/clientmanagementform.json", "w+")
json.dump(tmp, f, indent = 4)
f.close()