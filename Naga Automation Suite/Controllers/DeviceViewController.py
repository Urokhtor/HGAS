from Controllers.ViewController import ViewController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper
from Constants import CLIENT_TYPE_TELLDUS

import json

class DeviceViewController(ViewController):

    def handleRequest(parent, request, response):
        """

        """

        f = open("Conf/Website/deviceview.json", "r")
        tmp = json.load(f)
        f.close()
        deviceContainer = JFET.findElementById(tmp["source"], "deviceContainer")

        deviceUl = FEET.createDeviceUl(deviceContainer)

        devices = parent.deviceManager.getAll()

        if devices is None: return json.dumps(tmp)

        for device in devices:
            FEET.createDeviceRow(deviceUl, TypeMapper.mapDeviceState(device["state"]), device["name"])
            nameButton = JFET.findElementById(deviceUl, device["name"])

            if parent.clientManager.getById(device["clientid"]) != CLIENT_TYPE_TELLDUS:
                JFET.addParameter(nameButton, "onclick", "jumpToPage,submenu_device,deviceButton,devicemanagementSelectbutton,id:" + str(device["id"]))

        return json.dumps(tmp)