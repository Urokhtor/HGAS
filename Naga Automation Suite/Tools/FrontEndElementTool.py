__author__ = 'Urokhtor'

from Tools.JSONFrontEndTool import JSONFrontEndTool as JFET

class FrontEndElementTool:

    def createSource(renderBrowser = True):
        return {"source": {}, "renderbrowser": renderBrowser}

    def saveFile(data, file):
        import sys, json
        sys.path.append("G:\\Programming\Python\\Naga-Automation-Suite\\Naga Automation Suite")
        f = open("Conf/Website/" + file + ".json", "w")
        json.dump(data, f, indent = 4)
        f.close()

    def createMainContainer(source):
        mainContainer = JFET.addChild(source, "div")
        JFET.addParameter(mainContainer, "id", "mainContainer")
        JFET.addParameter(mainContainer, "className", "container")

        return mainContainer

    def createViewTable(div, header, id = "viewTable"):
        childDivViewTable = JFET.addChild(div, "div")
        JFET.addParameter(childDivViewTable, "className", "viewTable")
        JFET.addParameter(childDivViewTable, "id", id)

        # Thead.
        childTableViewTable = JFET.addChild(childDivViewTable, "table")
        JFET.addParameter(childTableViewTable, "className", "fullWidth")

        childThead = JFET.addChild(childTableViewTable, "thead")
        childTr = JFET.addChild(childThead, "tr")
        childTh = JFET.addChild(childTr, "th")
        JFET.addParameter(childTh, "className", "headCell")
        JFET.addParameter(childTh, "innerHTML", header)

        # Actual table.
        childTableViewTable2 = JFET.addChild(childDivViewTable, "table")
        JFET.addParameter(childTableViewTable2, "className", "fullWidth")
        childTbody = JFET.addChild(childTableViewTable2, "tbody")
        JFET.addParameter(childTbody, "id", "tableRows")

        # Buttonrow.
        childTableViewTable3 = JFET.addChild(childDivViewTable, "table")
        JFET.addParameter(childTableViewTable3, "className", "fullWidth")
        childDivButtonRow = JFET.addChild(childTableViewTable3, "div")
        JFET.addParameter(childDivButtonRow, "className", "buttonRow")
        JFET.addParameter(childDivButtonRow, "id", "buttonRow")

        return childDivViewTable

    def createLeftButtonColumn(mainContainer, header, id):
        childDiv = JFET.addChild(mainContainer, "div")
        JFET.addParameter(childDiv, "id", "leftButtonColumn")
        JFET.addParameter(childDiv, "className", "leftcolumn")

        #childTable = JFET.addChild(childDiv, "table")
        childDivSelect = JFET.addChild(childDiv, "div")
        childH3 = JFET.addChild(childDivSelect, "h3")
        JFET.addParameter(childH3, "innerHTML", header)

        childUl = JFET.addChild(childDiv, "ul")
        JFET.addParameter(childUl, "id", id)
        JFET.addParameter(childUl, "className", "leftcolumnul")

        return childDiv

    def createRightDivContainer(mainContainer):
        childDivRight = JFET.addChild(mainContainer, "div")
        JFET.addParameter(childDivRight, "id", "rightDataColumn")
        JFET.addParameter(childDivRight, "className", "rightcolumn")

        return childDivRight

    def createForm(mainContainer, id):
        form = JFET.addChild(mainContainer, "form")
        JFET.addParameter(form, "id", id)
        JFET.addParameter(form, "method", "post")

        return form

    def createTr(tableRows):
        childTr = JFET.addChild(tableRows, "tr")

        return childTr

    def createTd(tr, index, prefix, tableMapping, inputMapping):
        childTd = JFET.addChild(tr, "td")
        JFET.addParameter(childTd, "className", "labelCell")
        JFET.addParameter(childTd, "innerHTML", tableMapping[index])
        childTd2 = JFET.addChild(tr, "td")
        JFET.addParameter(childTd2, "className", "dataCell")

        mapping = tableMapping[index]

        if mapping.find(" ") != -1:
            parts = mapping.split(" ")
            mapping = ""

            for part in parts:
                mapping += part[:1].upper() + part[1:]


        if inputMapping is not None and len(inputMapping) > index:
            childElem = JFET.addChild(childTd2, inputMapping[index]["element"])

            if "type" in inputMapping[index]: JFET.addParameter(childElem, "type", inputMapping[index]["type"])

            JFET.addParameter(childElem, "name", prefix + mapping)
            JFET.addParameter(childElem, "id", prefix + mapping)

        else:
            JFET.addParameter(childTd2, "id", prefix + mapping)

    def fillViewTable(tableRows, prefix, tableMapping, inputMapping = None):
        j = 0
        for i in range(0, int(len(tableMapping)/2)):
            childTr = FrontEndElementTool.createTr(tableRows)
            FrontEndElementTool.createTd(childTr, j, prefix, tableMapping, inputMapping)
            j += 1
            FrontEndElementTool.createTd(childTr, j, prefix, tableMapping, inputMapping)
            j += 1

    def createButtonRowButtons(buttonRow, values, formId = "", onclick = False, prefix = "Sendbutton"):
        for value in reversed(values):
            tmp = None
            if onclick: tmp = "doSubmit," + formId + "," + value.lower()
            button = FrontEndElementTool.createButton(buttonRow, value.lower() + prefix, value.lower() + prefix, "decoratedButton buttonRowItem", value, tmp)

    def createButton(container, id, name, className, value, onclick = None):
        button = JFET.addChild(container, "input")
        JFET.addParameter(button, "id", id)
        JFET.addParameter(button, "name", name)
        JFET.addParameter(button, "type", "button")
        JFET.addParameter(button,"className", className)
        JFET.addParameter(button, "value", value)

        if onclick is not None: JFET.addParameter(button, "onclick", onclick)

        return button

    def createHiddenInput(container, id, name, value = None):
        hidden = JFET.addChild(container, "input")
        JFET.addParameter(hidden, "id", id)
        JFET.addParameter(hidden, "name", name)
        JFET.addParameter(hidden, "type", "hidden")

        if value:
            JFET.addParameter(hidden, "value", value)

        return hidden

    def createDeviceUl(deviceContainer):
        deviceUl = JFET.addChild(deviceContainer, "ul")
        JFET.addParameter(deviceUl, "id", "deviceUl")
        JFET.addParameter(deviceUl, "className", "deviceul")

        return deviceUl

    def createUl(container, id, className):
        ul = JFET.addChild(container, "ul")
        JFET.addParameter(ul, "id", id)
        JFET.addParameter(ul, "className", className)

        return ul

    def createDeviceRow(deviceUl, deviceState, deviceName):
        li = JFET.addChild(deviceUl, "li")
        deviceContainer = JFET.addChild(li, "div")
        JFET.addParameter(deviceContainer, "className", "liContainer")

        state = JFET.addChild(deviceContainer, "div")
        JFET.addParameter(state, "className", "devicestatediv")
        JFET.addParameter(state, "innerHTML", deviceState)

        name = JFET.addChild(deviceContainer, "div")
        JFET.addParameter(name, "className", "devicenamediv")
        #JFET.addParameter(name, "innerHTML", deviceName)
        nameButton = JFET.addChild(name, "input")
        JFET.addParameter(nameButton, "type", "button")
        JFET.addParameter(nameButton, "id", deviceName)
        JFET.addParameter(nameButton, "className", "decoratedButton")
        JFET.addParameter(nameButton, "value", deviceName)

        action = JFET.addChild(deviceContainer, "div")
        JFET.addParameter(action, "className", "right")

        # CHECK DEVICE TYPE TO SEE WHICH BUTTONS TO ADD!!!
        FrontEndElementTool.createButton(action, "deviceOff", 205, "decoratedButton", "Off")
        FrontEndElementTool.createButton(action, "deviceOn", 204, "decoratedButton", "On")

    def createSettingsRow(settingsUl, name, value, prefix):
        li = JFET.addChild(settingsUl, "li")
        settingsContainer = JFET.addChild(li, "div")
        JFET.addParameter(settingsContainer, "className", "liContainer")

        state = JFET.addChild(settingsContainer, "div")
        JFET.addParameter(state, "className", "devicenamediv")
        JFET.addParameter(state, "innerHTML", name)

        settingValue = JFET.addChild(settingsContainer, "div")
        JFET.addParameter(settingValue, "className", "right")
        JFET.addParameter(settingValue, "innerHTML", str(value) + " " + prefix)

    def addScript(container, file):
        script = JFET.addChild(container, "script")
        JFET.addParameter(script, "src", "../scripts/" + file + ".js")

    def createSelectMap(select, map, selectedIndex):
        for item in map:
            option = JFET.addChild(select, "option")
            JFET.addParameter(option, "value", str(item[0]))
            JFET.addParameter(option, "innerHTML", item[1])

            if item[0] == selectedIndex:
                JFET.addParameter(option, "selected", "selected")