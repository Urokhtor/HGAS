__author__ = 'Urokhtor'

from Controllers.ViewController import ViewController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper
from Constants import TABLE_FETCH

import json

class ClientViewController(ViewController):

    def handleRequest(parent, request, response):
        """

        """

        container = None

        f = open("Conf/Website/clientview.json", "r")
        tmp = json.load(f)
        f.close()

        clientUL = JFET.findElementById(tmp["source"], "clientUL")
        clients = parent.clientManager.getAll()

        if clients is None: return json.dumps(tmp)

        if request["action"] != TABLE_FETCH:
            container = tmp["source"]
            for client in clients:
                childLi = JFET.addChild(clientUL, "li")
                childDiv = JFET.addChild(childLi, "div")
                JFET.addParameter(childDiv, "className", "leftcolumndiv")
                childInput = JFET.addChild(childDiv, "input")
                JFET.addParameter(childInput, "className", "leftcolumnbutton")
                JFET.addParameter(childInput, "type", "button")
                JFET.addParameter(childInput, "value", client["name"])
                JFET.addParameter(childInput, "id", client["id"])

        elif request["action"] == TABLE_FETCH:
            container = JFET.findElementById(tmp["source"], "rightDataColumn")

        client = None

        if "params" in request and "id" in request["params"]:
            client = parent.clientManager.getById(int(request["params"]["id"]))

        if not client:
            client = clients[0]

        # Add the chosen sensor's data to the sensor info table.
        JFET.addParameter(JFET.findElementById(container, "clientName"), "innerHTML", client["name"])
        JFET.addParameter(JFET.findElementById(container, "clientType"), "innerHTML", TypeMapper.mapClientType(client["type"]))
        JFET.addParameter(JFET.findElementById(container, "clientAddress"), "innerHTML", client["ip"])

        modifyButton = JFET.findElementById(container, "modifyClient")
        JFET.addParameter(modifyButton, "onclick", "jumpToPage,submenu_client,clientButton,clientmanagementSelectbutton,id:" + str(client["id"]))

        if request["action"] != TABLE_FETCH: return json.dumps(tmp)
        else: return json.dumps(container)