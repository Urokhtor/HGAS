__author__ = 'Urokhtor'

import sys
sys.path.append("G:\\Programming\Python\\Naga-Automation-Suite\\Naga Automation Suite")

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

try:
    f = open("Conf/Website/deviceview.json", "r")
    tmp = json.load(f)
    f.close()

except:
    tmp = FEET.createSource()

tmp["source"] = {}
mainContainer = FEET.createMainContainer(tmp["source"])

deviceHolder = JFET.addChild(mainContainer, "div")
JFET.addParameter(deviceHolder, "id", "deviceContainer")
JFET.addParameter(deviceHolder, "className", "device")


f = open("Conf/Website/deviceview.json", "w+")
json.dump(tmp, f, indent = 4)
f.close()