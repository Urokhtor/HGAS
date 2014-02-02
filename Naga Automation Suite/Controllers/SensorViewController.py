from Controllers.ViewController import ViewController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.FrontEndElementTool import FrontEndElementTool as FEET
from Tools.TypeMapper import TypeMapper
from Constants import TABLE_FETCH, CLIENT_TYPE_TELLDUS

import json
from datetime import datetime

class SensorViewController(ViewController):

    def handleRequest(parent, request, response):
        """
        
        """

        container = None

        f = open("Conf/Website/sensorview.json", "r")
        tmp = json.load(f)
        f.close()

        sensorUL = JFET.findElementById(tmp["source"], "sensorUL")
        mainContainer = JFET.findElementById(tmp["source"], "mainContainer")

        sensors = parent.sensorManager.getAll()

        if sensors is None: return tmp

        if request["action"] != TABLE_FETCH:
            container = tmp["source"]
            for sensor in sensors:
                childLi = JFET.addChild(sensorUL, "li")
                childDiv = JFET.addChild(childLi, "div")
                JFET.addParameter(childDiv, "className", "leftcolumndiv")
                childInput = JFET.addChild(childDiv, "input")
                JFET.addParameter(childInput, "className", "leftcolumnbutton")
                JFET.addParameter(childInput, "type", "button")
                JFET.addParameter(childInput, "value", sensor["name"])
                JFET.addParameter(childInput, "id", sensor["id"])

        elif request["action"] == TABLE_FETCH:
            container = JFET.findElementById(tmp["source"], "rightDataColumn")

        sensor = None

        if "params" in request and "id" in request["params"]:
            sensor = parent.sensorManager.getById(int(request["params"]["id"]))
            
        if not sensor:
            sensor = sensors[0]

        # Add the chosen sensor's data to the sensor info table.
        JFET.addParameter(JFET.findElementById(container, "sensorInfoName"), "innerHTML", sensor["name"])
        JFET.addParameter(JFET.findElementById(container, "sensorInfoType"), "innerHTML", TypeMapper.mapSensorTypeToString(sensor["type"]))
        JFET.addParameter(JFET.findElementById(container, "sensorInfoClient"), "innerHTML", parent.clientManager.getById(sensor["clientid"])["name"])
        JFET.addParameter(JFET.findElementById(container, "sensorInfoIndex"), "innerHTML", sensor["index"])
        JFET.addParameter(JFET.findElementById(container, "sensorInfoLastReading"), "innerHTML", str(round(sensor["lastreading"], 1)) + " " + TypeMapper.mapSensorTypeToUnit(sensor["type"]))
        JFET.addParameter(JFET.findElementById(container, "sensorInfoLastUpdate"), "innerHTML", datetime.fromtimestamp(sensor["lastupdated"]).strftime("%d.%m.%Y %H:%M"))

        modifyButton = JFET.findElementById(container, "modifySensor")
        if parent.clientManager.getById(sensor["clientid"]) != CLIENT_TYPE_TELLDUS:
            JFET.addParameter(modifyButton, "onclick", "jumpToPage,submenu_sensor,sensorButton,sensormanagementSelectbutton,id:" + str(sensor["id"]))

        else:
            JFET.addParameter(modifyButton, "disabled", "true")

        # Add links to the sensor plots.
        ##### TODO: Make a check if the plots actually exist. If not, generate them on the fly?
        ##### TODO: Also make a setting for dynamic plot generation, i.e. call the plot generation function here.

        if parent.settingsManager.equals("plottype", "matplotlib"):
            # Add here plot generation for the sensor if setting automaticplots is true.
            sensorPlotsHolder = JFET.findElementById(container, "sensorPlotsHolder")
            sensorImg = JFET.addChild(sensorPlotsHolder, "img")
            JFET.addParameter(sensorImg, "className", "sensorimage")
            JFET.addParameter(sensorImg, "src", "../day-" + str(sensor["id"]) + "_" + str(sensor["type"]) + ".png")

            JFET.addChild(sensorPlotsHolder, "hr")

            sensorImg = JFET.addChild(sensorPlotsHolder, "img")
            JFET.addParameter(sensorImg, "className", "sensorimage")
            JFET.addParameter(sensorImg, "src", "../week-" + str(sensor["id"]) + "_" + str(sensor["type"]) + ".png")

        if request["action"] != TABLE_FETCH: return tmp
        else: return container