__author__ = 'Urokhtor'

from Controllers.FormController import FormController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper

import json

class ClientManagementFormController(FormController):

    def handleRequest(parent, request, response):
        """

        """

        f = open("Conf/Website/clientmanagementform.json", "r")
        tmp = json.load(f)
        f.close()

        clients = parent.clientManager.getAll()

        if clients is None: return tmp

        client = None
        selectedIndex = None

        if "params" in request and "id" in request["params"]:
            client = parent.clientManager.getById(int(request["params"]["id"]))

        if client:
            # Add the chosen sensor's data to the sensor info table.
            JFET.addParameter(JFET.findElementById(tmp["source"], "clientName"), "value", client["name"])
            JFET.addParameter(JFET.findElementById(tmp["source"], "clientAddress"), "value", client["ip"])
            selectedIndex = client["type"]
            clientId = JFET.findElementById(tmp["source"], "clientId")
            JFET.addParameter(clientId, "value", str(client["id"]))

        else:
            JFET.addParameter(JFET.findElementById(tmp["source"], "removeSendbutton"), "disabled", "true")

        clientType = JFET.findElementById(tmp["source"], "clientType")
        map = TypeMapper.getClientTypeMap()
        FEET.createSelectMap(clientType, map, selectedIndex)

        return tmp

    def validate(parent, request, reject):
        form = request["params"]["form"]
        if len(form["clientId"]) > 0: form["clientId"] = int(form["clientId"])
        form["clientType"] = int(form["clientType"])


    def handleSubmit(parent, request, response):
        form = request["params"]["form"]

        if request["params"]["mode"] == "save":
            if len(form["clientId"]) > 0:
                pass

            else:
                name = form["clientName"]
                clientType = form["clientType"]
                ip = form["clientAddress"]

                client = parent.clientManager.create(name, clientType, ip)
                return parent.clientManager.insert(client)

        elif request["params"]["mode"] == "remove":
            return parent.clientManager.removeById(form["clientId"])