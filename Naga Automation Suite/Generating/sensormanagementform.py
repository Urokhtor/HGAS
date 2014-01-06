__author__ = 'Urokhtor'

import sys
sys.path.append("G:\\Programming\Python\\Naga-Automation-Suite\\Naga Automation Suite")

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

try:
    f = open("Conf/Website/sensormanagementform.json", "r")
    tmp = json.load(f)
    f.close()

except:
    tmp = FEET.createSource()

tmp["source"] = {}
mainContainer = FEET.createMainContainer(tmp["source"])


f = open("Conf/Website/sensormanagementform.json", "w")
json.dump(tmp, f, indent = 4)
f.close()