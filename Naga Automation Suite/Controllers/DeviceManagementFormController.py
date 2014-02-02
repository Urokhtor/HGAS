__author__ = 'Urokhtor'

from Controllers.FormController import FormController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper

import json

class DeviceManagementFormController(FormController):

    def handleRequest(parent, request, response):
        """

        """

        f = open("Conf/Website/devicemanagementform.json", "r")
        tmp = json.load(f)
        f.close()

        devices = parent.deviceManager.getAll()

        if devices is None: return json.dumps(tmp)

        device = None
        selectedIndex = None
        clientValue = None

        if "params" in request and "id" in request["params"]:
            device = parent.deviceManager.getById(int(request["params"]["id"]))

        if device:
            # Add the chosen sensor's data to the sensor info table.
            JFET.addParameter(JFET.findElementById(tmp["source"], "deviceName"), "value", device["name"])
            selectedIndex = device["type"]
            clientValue = device["clientid"]
            JFET.addParameter(JFET.findElementById(tmp["source"], "deviceIndex"), "value", device["index"])
            deviceId = JFET.findElementById(tmp["source"], "deviceId")
            JFET.addParameter(deviceId, "value", str(device["id"]))

        else:
            JFET.addParameter(JFET.findElementById(tmp["source"], "removeSendbutton"), "disabled", "true")

        deviceType = JFET.findElementById(tmp["source"], "deviceType")
        map = TypeMapper.getDeviceTypeMap()
        FEET.createSelectMap(deviceType, map, selectedIndex)

        deviceClient = JFET.findElementById(tmp["source"], "deviceClient")

        client = parent.clientManager.getById(clientValue)
        clientName = None

        if client is not None:
            clientName = client["name"]

        FEET.createSelectMap(deviceClient, parent.clientManager.getIdNameMap(), clientName) # It now uses name for the ID. Perhaps we should use the real ID?

        return json.dumps(tmp)

    def validate(parent, request, reject):
        pass

    def handleSubmit(parent, request, response):
        pass