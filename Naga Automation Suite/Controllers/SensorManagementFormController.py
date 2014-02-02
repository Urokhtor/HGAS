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

        sensors = parent.sensorManager.getAll()

        if sensors is None: return tmp

        sensor = None
        selectedIndex = None
        clientValue = None

        if "params" in request and "id" in request["params"]:
            sensor = parent.sensorManager.getById(int(request["params"]["id"]))

        if sensor:
            # Add the chosen sensor's data to the sensor info table.
            JFET.addParameter(JFET.findElementById(tmp["source"], "sensorName"), "value", sensor["name"])
            selectedIndex = sensor["type"]
            clientValue = sensor["clientid"]
            JFET.addParameter(JFET.findElementById(tmp["source"], "sensorIndex"), "value", sensor["index"])
            sensorId = JFET.findElementById(tmp["source"], "sensorId")
            JFET.addParameter(sensorId, "value", str(sensor["id"]))

        else:
            JFET.addParameter(JFET.findElementById(tmp["source"], "removeSendbutton"), "disabled", "true")

        sensorType = JFET.findElementById(tmp["source"], "sensorType")
        map = TypeMapper.getSensorTypeMap()
        FEET.createSelectMap(sensorType, map, selectedIndex)

        sensorClient = JFET.findElementById(tmp["source"], "sensorClient")

        client = parent.clientManager.getById(clientValue)
        clientName = None

        if client is not None:
            clientName = client["name"]

        FEET.createSelectMap(sensorClient, parent.clientManager.getIdNameMap(), clientName)

        return tmp

    def validate(parent, request, reject):
        """
            Validates the form data.
        """

        if "params" not in request:
            reject["errors"].append("") # This should somehow be sent to the notification container.
            return

        form = request["params"]["form"]
        if len(form["sensorId"]) > 0: form["sensorId"] = int(form["sensorId"])
        form["sensorType"] = int(form["sensorType"])
        form["sensorClient"] = int(form["sensorClient"])
        form["sensorIndex"] = int(form["sensorIndex"])

    def handleSubmit(parent, request, response):
        """
            Handle things like adding, modifying and removing sensors.
        """

        # Check ID. If it's empty, create new sensor. If it's not, modify existing sensor.
        form = request["params"]["form"]

        if request["params"]["mode"] == "save":
            if len(form["sensorId"]) > 0:
                pass

            else:
                name = form["sensorName"]
                sensorType = form["sensorType"]
                clientid = form["sensorClient"]
                index = form["sensorIndex"]

                sensor = parent.sensorManager.create(name, sensorType, clientid, index)
                response = parent.sensorManager.insert(sensor)
                print(response)
                if "error" in response:
                    return SensorManagementFormController.errorView()

                elif "response" in response:
                    message = {}
                    message["id"] = "notificationContainer"
                    message["text"] = parent.messageManager.getByName("sensor.added")["value"]
                    messages = []
                    messages.append(message)
                    redirect = "jumpToPage,submenu_sensor,sensorButton,sensorSelectbutton,id:" + str(sensor["id"])

                    return SensorManagementFormController.successView(parent, messages, redirect, response)

        elif request["params"]["mode"] == "remove":
            response = parent.sensorManager.removeById(form["sensorId"])

            if "error" in response:
                return SensorManagementFormController.errorView()

            elif "response" in response:
                message = {}
                message["id"] = "notificationContainer"
                message["text"] = parent.messageManager.getByName("sensor.removed")["value"]
                messages = []
                messages.append(message)
                redirect = "jumpToPage,submenu_sensor,sensorButton,sensorSelectbutton,"

                return SensorManagementFormController.successView(parent, messages, redirect, response)