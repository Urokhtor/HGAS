__author__ = 'Urokhtor'

from Controllers.ViewController import ViewController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper
from Constants import TABLE_FETCH

import json

class TaskViewController(ViewController):

    def handleRequest(parent, request, response):
        """

        """

        container = None

        f = open("Conf/Website/taskview.json", "r")
        tmp = json.load(f)
        f.close()

        taskUL = JFET.findElementById(tmp["source"], "taskUL")
        tasks = parent.taskManager.getAll()

        if tasks is None: return json.dumps(tmp)

        if request["action"] != TABLE_FETCH:
            container = tmp["source"]
            for task in tasks:
                # We don't want any background tasks to surface.
                if task["type"] != "write": continue

                childLi = JFET.addChild(taskUL, "li")
                childDiv = JFET.addChild(childLi, "div")
                JFET.addParameter(childDiv, "className", "leftcolumndiv")
                childInput = JFET.addChild(childDiv, "input")
                JFET.addParameter(childInput, "className", "leftcolumnbutton")
                JFET.addParameter(childInput, "type", "button")
                JFET.addParameter(childInput, "value", task["name"])
                JFET.addParameter(childInput, "id", task["id"])

        elif request["action"] == TABLE_FETCH:
            container = JFET.findElementById(tmp["source"], "rightDataColumn")

        task = None

        if "params" in request and "id" in request["params"]:
            task = parent.taskManager.getById(int(request["params"]["id"]))

        if not task:
            task = tasks[0]

        # Add the chosen sensor's data to the sensor info table.
        JFET.addParameter(JFET.findElementById(container, "taskName"), "innerHTML", task["name"])
        JFET.addParameter(JFET.findElementById(container, "taskDevice"), "innerHTML", parent.deviceManager.getById(task["deviceid"])["name"])
        JFET.addParameter(JFET.findElementById(container, "taskAction"), "innerHTML", TypeMapper.mapTaskAction(task["action"]))
        JFET.addParameter(JFET.findElementById(container, "taskEvents"), "innerHTML", task["schedules"])
        JFET.addParameter(JFET.findElementById(container, "taskIsPermanent"), "innerHTML", TypeMapper.mapBoolean(task["ispermanent"]))

        modifyButton = JFET.findElementById(container, "modifyTask")
        JFET.addParameter(modifyButton, "onclick", "jumpToPage,submenu_task,taskButton,taskmanagementSelectbutton,id:" + str(task["id"]))

        if request["action"] != TABLE_FETCH: return json.dumps(tmp)
        else: return json.dumps(container)