__author__ = 'Urokhtor'

from Controllers.FormController import FormController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper

import json

class TaskManagementFormController(FormController):

    def handleRequest(parent, request, response):
        """

        """

        f = open("Conf/Website/taskmanagementform.json", "r")
        tmp = json.load(f)
        f.close()

        tasks = parent.taskManager.getAll()

        if tasks is None: return json.dumps(tmp)

        task = None
        deviceId = None
        actionType = None

        if "params" in request and "id" in request["params"]:
            task = parent.taskManager.getById(int(request["params"]["id"]))

        if task:
            # Add the chosen sensor's data to the sensor info table.
            JFET.addParameter(JFET.findElementById(tmp["source"], "taskName"), "value", task["name"])
            deviceId = task["deviceid"]
            actionType = task["action"]
            JFET.addParameter(JFET.findElementById(tmp["source"], "taskEvents"), "value", " ".join(task["schedules"]))
            JFET.addParameter(JFET.findElementById(tmp["source"], "taskIsPermanent"), "checked", task["ispermanent"])
            taskId = JFET.findElementById(tmp["source"], "taskId")
            JFET.addParameter(taskId, "value", str(task["id"]))

        else:
            JFET.addParameter(JFET.findElementById(tmp["source"], "taskIsPermanent"), "checked", True)
            JFET.addParameter(JFET.findElementById(tmp["source"], "removeSendbutton"), "disabled", "true")

        taskDevice = JFET.findElementById(tmp["source"], "taskDevice")
        FEET.createSelectMap(taskDevice, parent.deviceManager.getIdNameMap(), deviceId)

        taskAction = JFET.findElementById(tmp["source"], "taskAction")
        FEET.createSelectMap(taskAction, TypeMapper.getTaskActionMap(), actionType)

        return json.dumps(tmp)

    def validate(parent, request, reject):
        form = request["params"]["form"]
        form["taskAction"] = int(form["taskAction"])
        form["taskDevice"] = int(form["taskDevice"])
        if len(form["taskId"]) > 0: form["taskId"] = int(form["taskId"])

    def handleSubmit(parent, request, response):
        form = request["params"]["form"]

        if request["params"]["mode"] == "save":
            name = form["taskName"]
            taskType = "write"
            action = form["taskAction"]
            device = form["taskDevice"]
            isTemporary = form["taskIsPermanent"]
            schedules = form["taskEvents"]

            task = parent.taskManager.create(name, taskType, action, device, isTemporary, schedules)
            return json.dumps(parent.taskManager.insert(task))

        elif request["params"]["mode"] == "remove":
            return json.dumps(parent.taskManager.remove(parent.taskManager.getById(form["taskId"])))