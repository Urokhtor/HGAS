__author__ = 'Urokhtor'

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET

class FrontEndElementTool:

    def createSource(renderBrowser = True):
        return {"source": {}, "renderbrowser": renderBrowser}

    def createMainContainer(source):
        mainContainer = JFET.addChild(source, "div")
        JFET.addParameter(mainContainer, "id", "mainContainer")
        JFET.addParameter(mainContainer, "className", "container")

        return mainContainer

    def createViewTable(div):
        childDivViewTable = JFET.addChild(div, "div")
        JFET.addParameter(childDivViewTable, "className", "viewTable")

        # Thead.
        childTableViewTable = JFET.addChild(childDivViewTable, "table")
        JFET.addParameter(childTableViewTable, "className", "fullWidth")

        childThead = JFET.addChild(childTableViewTable, "thead")
        childTr = JFET.addChild(childThead, "tr")
        childTh = JFET.addChild(childTr, "th")
        JFET.addParameter(childTh, "className", "headCell")
        JFET.addParameter(childTh, "innerHTML", "Sensor info:")

        # Actual table.
        childTableViewTable2 = JFET.addChild(childDivViewTable, "table")
        JFET.addParameter(childTableViewTable2, "className", "fullWidth")
        childTbody = JFET.addChild(childTableViewTable2, "tbody")
        JFET.addParameter(childTbody, "id", "tableRows")

        return childDivViewTable

    def createLeftButtonColumn(mainContainer):
        childDiv = JFET.addChild(mainContainer, "div")
        JFET.addParameter(childDiv, "id", "leftSensorColumn")
        JFET.addParameter(childDiv, "className", "leftcolumn")

        #childTable = JFET.addChild(childDiv, "table")
        childDivSelect = JFET.addChild(childDiv, "div")
        childH3 = JFET.addChild(childDivSelect, "h3")
        JFET.addParameter(childH3, "innerHTML", "Select sensor:")

        childUl = JFET.addChild(childDiv, "ul")
        JFET.addParameter(childUl, "id", "sensorUL")
        JFET.addParameter(childUl, "className", "leftcolumnul")

        return childDiv

    def createRightDivContainer(mainContainer):
        childDivRight = JFET.addChild(mainContainer, "div")
        JFET.addParameter(childDivRight, "id", "rightSensorColumn")
        JFET.addParameter(childDivRight, "className", "rightcolumn")

        return childDivRight