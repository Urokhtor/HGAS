__author__ = 'Urokhtor'

from Controllers.ViewController import ViewController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper

import json

class SettingsManagementFormController(ViewController):

    def handleRequest(parent, request, response):
        """

        """

        f = open("Conf/Website/settingsmanagementform.json", "r")
        tmp = json.load(f)
        f.close()
        settingsContainer = JFET.findElementById(tmp["source"], "settingsContainer")

        settingsUl = FEET.createUl(settingsContainer, "settingsUl", "deviceul")

        settings = parent.settingsManager.getAll()

        if settings is None: return json.dumps(tmp)

        for setting in settings:
            # Perhaps create a mapping to human readable strings for settings keys and sort them alphabetically.
            message = parent.messageManager.getByName("setting." + setting["name"])

            if message is not None:
                description = message["value"]

            else:
                description = setting["name"]

            value = None

            if setting["type"] == "bool": value = TypeMapper.mapBoolean(setting["value"])
            else: value = setting["value"]

            FEET.createSettingsRow(settingsUl, description, value, setting["prefix"])

        return json.dumps(tmp)