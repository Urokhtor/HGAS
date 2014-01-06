__author__ = 'Urokhtor'

from Controllers.FormController import FormController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.TypeMapper import TypeMapper

import json
from datetime import datetime

class SensorManagementFormController(FormController):

    def handleRequest(parent, request, response):
        """

        """

        f = open("Conf/Website/sensormanagementform.json", "r")
        tmp = json.load(f)
        f.close()
        print(tmp)
        #sensorUL = JFET.findElementById(tmp["source"], "sensorUL")

        sensors = parent.deviceManager.getSensors()

        if sensors is None: return json.dumps(tmp)
        else: return json.dumps(tmp)
