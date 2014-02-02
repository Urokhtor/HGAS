__author__ = 'Urokhtor'

import sys, os
sys.path.append(os.getcwd())

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
import json

try:
    f = open("Conf/Website/sensorcontrolmanagementform.json", "r")
    tmp = json.load(f)
    f.close()

except:
    tmp = FEET.createSource()

tmp["source"] = {}
mainContainer = FEET.createMainContainer(tmp["source"])


f = open("Conf/Website/sensorcontrolmanagementform.json", "w+")
json.dump(tmp, f, indent = 4)
f.close()