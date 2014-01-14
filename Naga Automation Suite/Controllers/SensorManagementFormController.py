__author__ = 'Urokhtor'

from Controllers.FormController import FormController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper

import json

class SensorManagementFormController(FormController):

    def handleRequest(parent, request, response):
        """

        """

        f = open("Conf/Website/sensormanagementform.json", "r")
        tmp = json.load(f)
        f.close()

        sensors = parent.deviceManager.getSensors()

        if sensors is None: return json.dumps(tmp)

        sensor = None
        selectedIndex = None
        clientValue = None

        if "params" in request and "id" in request["params"]:
            sensor = parent.deviceManager.getSensorById(int(request["params"]["id"]))

        if sensor:
            # Add the chosen sensor's data to the sensor info table.
            JFET.addParameter(JFET.findElementById(tmp["source"], "sensorName"), "value", sensor["name"])
            selectedIndex = sensor["type"]
            clientValue = sensor["clientid"]
            JFET.addParameter(JFET.findElementById(tmp["source"], "sensorIndex"), "value", sensor["index"])
            sensorId = JFET.findElementById(tmp["source"], "sensorId")
            JFET.addParameter(sensorId, "value", str(sensor["id"]))

        sensorType = JFET.findElementById(tmp["source"], "sensorType")
        map = TypeMapper.getSensorTypeMap()
        FEET.createSelectMap(sensorType, map, selectedIndex)

        sensorClient = JFET.findElementById(tmp["source"], "sensorClient")

        client = parent.clientManager.getById(clientValue)
        clientName = None

        if client is not None:
            clientName = client["name"]

        FEET.createSelectMap(sensorClient, parent.clientManager.getAllFromField("name"), clientName)

        return json.dumps(tmp)
