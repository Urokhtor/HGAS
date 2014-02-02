__author__ = 'Urokhtor'

import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

tmp = FEET.createSource()
tmp["source"] = {}
mainContainer = FEET.createMainContainer(tmp["source"])

deviceHolder = JFET.addChild(mainContainer, "div")
JFET.addParameter(deviceHolder, "id", "settingsContainer")
JFET.addParameter(deviceHolder, "className", "listContainer")

f = open("Conf/Website/settingsmanagementform.json", "w+")
json.dump(tmp, f, indent = 4)
f.close()