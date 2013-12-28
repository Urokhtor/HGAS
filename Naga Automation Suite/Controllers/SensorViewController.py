from Controllers.ViewController import ViewController
from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET
from Tools.TypeMapper import TypeMapper

import json
from datetime import datetime

class SensorViewController(ViewController):

    def handleRequest(parent, request, response):
        """
        
        """
        
        f = open("Conf/Website/sensorview_test.json", "r")
        tmp = json.load(f)
        f.close()
        
        sensorUL = JFET.findElementById(tmp["source"], "sensorUL")
        
        sensors = parent.deviceManager.getSensors()
        
        for sensor in sensors:
            childLi = JFET.addChild(sensorUL, "li")
            childDiv = JFET.addChild(childLi, "div")
            JFET.addParameter(childDiv, "className", "leftcolumndiv")
            childInput = JFET.addChild(childDiv, "input")
            JFET.addParameter(childInput, "className", "leftcolumnbutton")
            JFET.addParameter(childInput, "type", "button")
            JFET.addParameter(childInput, "value", sensor["name"])
            JFET.addParameter(childInput, "id", sensor["id"])
        
        sensor = None
        if "sensorId" in request:
            sensor = parent.deviceManager.getSensorById(request["sensorId"])
            
        if not sensor:
            sensor = sensors[0]
        
        # Add the chosen sensor's data to the sensor info table.
        JFET.addParameter(JFET.findElementById(tmp["source"], "sensorInfoName"), "innerHTML", sensor["name"])
        JFET.addParameter(JFET.findElementById(tmp["source"], "sensorInfoType"), "innerHTML", TypeMapper.mapSensorTypeToString(sensor["type"]))
        JFET.addParameter(JFET.findElementById(tmp["source"], "sensorInfoClient"), "innerHTML", sensor["clientname"])
        JFET.addParameter(JFET.findElementById(tmp["source"], "sensorInfoIndex"), "innerHTML", sensor["index"])
        JFET.addParameter(JFET.findElementById(tmp["source"], "sensorInfoLastReading"), "innerHTML", str(round(sensor["lastreading"], 1)) + " " + TypeMapper.mapSensorTypeToUnit(sensor["type"]))
        JFET.addParameter(JFET.findElementById(tmp["source"], "sensorInfoLastUpdate"), "innerHTML", datetime.fromtimestamp(sensor["lastupdated"]).strftime("%d.%m.%Y %H:%M"))
        
        # Add links to the sensor plots.
        ##### TODO: Make a check if the plots actually exist. If not, generate them on the fly?
        ##### TODO: Also make a setting for dynamic plot generation, i.e. call the plot generation function here.

        sensorPlotsHolder = JFET.findElementById(tmp["source"], "sensorPlotsHolder")
        sensorImg = JFET.addChild(sensorPlotsHolder, "img")
        JFET.addParameter(sensorImg, "className", "sensorimage")
        JFET.addParameter(sensorImg, "src", "../day-" + str(sensor["id"]) + "_" + str(sensor["type"]) + ".png")

        JFET.addChild(sensorPlotsHolder, "hr")

        sensorImg = JFET.addChild(sensorPlotsHolder, "img")
        JFET.addParameter(sensorImg, "className", "sensorimage")
        JFET.addParameter(sensorImg, "src", "../week-" + str(sensor["id"]) + "_" + str(sensor["type"]) + ".png")
        
        return json.dumps(tmp)
        