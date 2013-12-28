var sensorHolder;
var deviceHolder;
var taskHolder;
var sensorControlHolder;
var eventLogHolder;
var intervalHolder;

// Messaging protocol constants
var SEND_WRITE = 201;
var SEND_ENABLE = 204;
var SEND_DISABLE = 205;

var SENSOR_TYPE_DEFAULT = 0;
var SENSOR_TYPE_TEMPERATURE = 1;
var SENSOR_TYPE_DHT11 = 2;
var SENSOR_TYPE_SR04 = 3;
var SENSOR_BMP085_TEMPERATURE = 4;
var SENSOR_BMP085_PRESSURE = 5;
var SENSOR_BMP085_ALTITUDE = 6;

var DEVICE_TYPE_LIGHTS = 0;
var DEVICE_TYPE_PUMP = 1;

function postHTTPRequest(message, callback)
{
    $.post("frontpage.html", message, function(result) {callback(result)});
}

function getHTTPRequest(message, callback)
{
    $.get("frontpage.html", message, function(result) {callback(result)});
}

function createCookie(name,value,days)
{
	if (days)
    {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
    
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name)
{
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
    
	for(var i=0;i < ca.length;i++)
    {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function sleep(milliseconds)
{
    var start = new Date().getTime();
  
    for (var i = 0; i < 1e7; i++)
    {
        if ((new Date().getTime() - start) > milliseconds)
        {
            break;
        }
    }
}

function addItemToList(text, listName, value)
{
    // Create an Option object
    var opt = document.createElement("option");
    
    // Add an Option object to Drop Down/List Box
    document.getElementById(listName).options.add(opt);
    
    // Assign text and value to Option object
    opt.text = text;
    opt.value = value;
}

function clearList(listName)
{
    document.getElementById(listName).options.length = 0;
}

function submitForm(form, action) {
    var formElem = document.getElementById(form);
    var tmp = {};
    var object = {};
    tmp["type"] = "form";
    tmp["name"] = formElem.getAttribute("action");
    tmp["action"] = action;
    
    for (var i = 0; i < formElem.elements.length; i++) {
        if (formElem.elements[i].type == "checkbox")
            object[formElem.elements[i].id] = formElem.elements[i].checked;
        
        else
            object[formElem.elements[i].id] = formElem.elements[i].value;
    }
    
    tmp["object"] = object;
    console.log(JSON.stringify(tmp));
    postHTTPRequest(JSON.stringify(tmp), formHandle);
}

function formHandle(response) {
    console.log(response);
}

function modifyView(id, page) {    
    setSubMenu(document.getElementById("submenu_" + page), document.getElementById(page + "managementPage"), document.getElementById(page + "managementContainer"));

    if (page == "sensor")
        fillSensorManagement(id);
    
    else if (page == "device")
        fillDeviceManagement(id);
    
    else if (page == "task")
        fillTaskManagement(id);
}

function onLoadFillSensorManagement() {
    addItemToList("temp", "sensorType", SENSOR_TYPE_TEMPERATURE);
    addItemToList("hygrometer", "sensorType", SENSOR_TYPE_DEFAULT);
    addItemToList("humidity", "sensorType", SENSOR_TYPE_DHT11);
    addItemToList("ultrasound", "sensorType", SENSOR_TYPE_SR04);
    addItemToList("BMP085 temp", "sensorType", SENSOR_BMP085_TEMPERATURE);
    addItemToList("BMP085 pressure", "sensorType", SENSOR_BMP085_PRESSURE);
    addItemToList("BMP085 altitude", "sensorType", SENSOR_BMP085_ALTITUDE);
    
    addItemToList("Garden", "sensorClient", "Garden");
}

function onLoadFillDeviceManagement() {
    addItemToList("Lights", "deviceManagementType", DEVICE_TYPE_LIGHTS);
    addItemToList("Pump", "deviceManagementType", DEVICE_TYPE_PUMP);
    
    addItemToList("Garden", "deviceManagementClient", "Garden");
}

function onLoadFillTaskManagement() {
    /*for (var i = 0; i < deviceHolder.length; i++) {
        addItemToList(deviceHolder[i].name, "taskManagementDeviceList", deviceHolder[i].name);
    }*/
    
    addItemToList("On", "taskManagementExecuteActionList", SEND_ENABLE);
    addItemToList("Off", "taskManagementExecuteActionList", SEND_DISABLE);
    addItemToList("Toggle", "taskManagementExecuteActionList", SEND_WRITE);
    
    document.getElementById("taskManagementExecuteActionList").selectedIndex = 0;
}

function fillSensorManagement(id) {
    var sensor;
    
    for (var i = 0; i < sensorHolder.length; i++) {
        if (sensorHolder[i].id == id) {
            sensor = sensorHolder[i];
            break;
        }
    }
    
    if (sensor == undefined) return;
    
    document.getElementById("sensorName").value = sensor.name;
    document.getElementById("sensorType").value = sensor.type;
    document.getElementById("sensorClient").value = sensor.clientname;
    document.getElementById("sensorIndex").value = sensor.index;
    document.getElementById("sensorId").value = sensor.id;
    document.getElementById("addSensor").disabled = true;
}

function fillDeviceManagement(id) {
    var device;
    
    for (var i = 0; i < deviceHolder.length; i++) {
        if (deviceHolder[i].id == id) {
            device = deviceHolder[i];
            break;
        }
    }
    if (device == undefined) return;
    
    document.getElementById("deviceManagementName").value = device.name;
    document.getElementById("deviceManagementType").value = device.type;
    document.getElementById("deviceManagementClient").value = device.clientname;
    document.getElementById("deviceManagementIndex").value = device.index;
    document.getElementById("deviceId").value = device.id;
    document.getElementById("addDevice").disabled = true;
}

function fillTaskManagement(id) {
    var task;
    
    for (var i = 0; i < taskHolder.length; i++) {
        if (taskHolder[i].id == id) {
            task = taskHolder[i];
            break;
        }
    }
    
    if (task == undefined) return;
    
    //clearList("taskManagementDeviceList");
    
    for (var i = 0; i < deviceHolder.length; i++) {
        addItemToList(deviceHolder[i].name, "taskManagementDeviceList", deviceHolder[i].name);
    }
    
    document.getElementById("taskManagementName").value = task.name;
    //document.getElementById("taskManagementDeviceList").value = task.device;
    document.getElementById("taskManagementName").value = task.name;
    document.getElementById("taskManagementIsTemporaryCheckbox").value = task.ispermanent;
    document.getElementById("taskManagementSchedules").value = task.schedules;
    document.getElementById("taskId").value = task.id;
    document.getElementById("addTask").disabled = true;

}

function getSensors()
{
    // Command sent to the server.
    var data = "getSensors";

    // The HTTP request sent to server.
    getHTTPRequest(data, sensorHandle);
}

function sensorHandle(response)
{
    sensorHolder = JSON.parse(response);
    var ul = document.getElementById("sensorUL");
    clearList("sensorcontrolManagementSensor");
    
    while (ul.firstChild)
        ul.removeChild(ul.firstChild);
    
    for (var i = 0; i < sensorHolder.length; i++)
    {
        addItemToList(sensorHolder[i].name, "sensorcontrolManagementSensor");
        
        var newLI = document.createElement("LI");
        var newDiv = document.createElement("DIV");
        var newButton = document.createElement("INPUT");
        newDiv.appendChild(newButton);
        newLI.appendChild(newDiv);
        ul.appendChild(newLI);
        
        newDiv.className += "leftcolumndiv";

        newButton.className += "leftcolumnbutton";
        newButton.type = "button";
        newButton.value = sensorHolder[i].name;
        newButton.id = sensorHolder[i].name;
        newButton.onclick = function(e) {pickSensorButton(e.target.id);};
    }
    
    pickSensor(readCookie("chosensensor"));
    getSensorGraphs(readCookie("chosensensor"));
}

// Pick one sensor from the sensorList and display its name on chosenSensor text field.
function pickSensor(sensorItem)
{
    if (sensorItem == null)
        sensorItem = sensorHolder[0].name;
    
    for (var i = 0; i < sensorHolder.length; i++)
    {
        if (sensorHolder[i].name == sensorItem)
        {
            document.getElementById("sensorInfoName").innerHTML = "<a href='#' title='Click to access modify page' onClick='javascript:modifyView(\"" + sensorHolder[i].id + "\", \"sensor\")'>" + sensorHolder[i].name + "</a>";
            
            var type = "";
            var suffix = "";
            if (sensorHolder[i].type == SENSOR_TYPE_DEFAULT) {
                type = "hygrometer";
            }
            
            else if (sensorHolder[i].type == SENSOR_TYPE_TEMPERATURE) {
                type = "temp";
                suffix = " C";
            }
            
            else if (sensorHolder[i].type == SENSOR_TYPE_DHT11) {
                type = "humidity";
                suffix = " %";
            }
            
            else if (sensorHolder[i].type == SENSOR_TYPE_SR04) {
                type = "ultrasound";
                suffix = " cm";
            }
            
            document.getElementById("sensorInfoType").innerHTML = type;
            document.getElementById("sensorInfoClient").innerHTML = sensorHolder[i].clientname;
            document.getElementById("sensorInfoIndex").innerHTML = sensorHolder[i].index;
            document.getElementById("sensorInfoReading").innerHTML = (sensorHolder[i].lastreading).toFixed(1) + suffix;
            var date = new Date(sensorHolder[i].lastupdated*1000);
            document.getElementById("sensorInfoUpdate").innerHTML = date.toLocaleDateString("fi-FI") + " " + date.toLocaleTimeString("fi-FI").replace(/\./g, ":");
        }
    }
}

function getSensorGraphs(sensorItem)
{
    var imgHolder = document.getElementById("sensorPlotsHolder");
    
    while(imgHolder.firstChild)
        imgHolder.removeChild(imgHolder.firstChild);
            
    var sensor = null;
    
    for (var i = 0; i < sensorHolder.length; i++)
    {
        if (sensorHolder[i].name == sensorItem)
        {
            sensor = sensorHolder[i];
            break;
        }
    }
    
    if (sensor == null)
        return;
        
    var imageLocation = sensor.id + "_" + sensor.type + ".png";
    var sensorDailyPlot = document.createElement("img");
    var sensorWeeklyPlot = document.createElement("img");
    var hr = document.createElement("hr");
    
    sensorDailyPlot.className += "sensorimage";
    sensorWeeklyPlot.className += "sensorimage";
    
    sensorDailyPlot.setAttribute("src", "day-" + imageLocation);
    sensorWeeklyPlot.setAttribute("src", "week-" + imageLocation);
                
    imgHolder.appendChild(sensorDailyPlot);
    imgHolder.appendChild(hr);
    imgHolder.appendChild(sensorWeeklyPlot);
}

function pickSensorButton(sensorItem)
{
    createCookie("chosensensor", sensorItem, 5);
    getSensors();
}

function getDevices()
{
    // Command sent to the server.
    var data = "getDevices";

    // The HTTP request sent to server.
    getHTTPRequest(data, deviceHandle);
}

function deviceHandle(response)
{
    clearList("taskManagementDeviceList");
    clearList("sensorcontrolManagementDevice");
    deviceHolder = JSON.parse(response);
    var ul = document.getElementById("deviceUL");
    ul.innerHTML = "";

    for (var i = 0; i < deviceHolder.length; i++)
    {
        addItemToList(deviceHolder[i].name, "taskManagementDeviceList", deviceHolder[i].name);
        addItemToList(deviceHolder[i].name, "sensorcontrolManagementDevice");
        
        var newLI = document.createElement("LI");
        var newDiv = document.createElement("DIV");
        var newDeviceStateDiv = document.createElement("DIV");
        var newDeviceNameDiv = document.createElement("DIV");
        var newDeviceContainerDiv = document.createElement("DIV");
        
        newDiv.appendChild(newDeviceStateDiv);
        newDiv.appendChild(newDeviceNameDiv);
        newDiv.appendChild(newDeviceContainerDiv);
        
        newLI.appendChild(newDiv);
        ul.appendChild(newLI);

        newDiv.className += "devicecontainerdiv";

        newDeviceStateDiv.className += "devicestatediv";
        newDeviceNameDiv.className += "devicenamediv";
        newDeviceContainerDiv.className += "deviceactioncontaineriv";
        
        if (deviceHolder[i].state) newDeviceStateDiv.innerHTML = "On";
        else newDeviceStateDiv.innerHTML = "Off";
        
        newDeviceNameDiv.innerHTML = "<a href='#' title='Click to access modify page' onClick='javascript:modifyView(\"" + deviceHolder[i].id + "\", \"device\")'>" + deviceHolder[i].name + "</a>";
        
        var newOffButton= document.createElement("INPUT");
        newDeviceContainerDiv.appendChild(newOffButton);
        newOffButton.className += "devicebutton";
        newOffButton.type = "button";
        newOffButton.value = "Off";
        newOffButton.name = SEND_DISABLE;
        newOffButton.id = deviceHolder[i].index;
        newOffButton.onclick = function(e) {toggleDevice(e.target.name, e.target.id);};
        
        var newOnButton = document.createElement("INPUT");
        newDeviceContainerDiv.appendChild(newOnButton);
        newOnButton.className += "devicebutton";
        newOnButton.type = "button";
        newOnButton.value = "On";
        newOnButton.name = SEND_ENABLE;
        newOnButton.id = deviceHolder[i].index;
        newOnButton.onclick = function(e) {toggleDevice(e.target.name, e.target.id);};
    }
}

function toggleDevice(action, index)
{
    data = "controlDevice;" + index + ";" + action;
    postHTTPRequest(data, toggleHandle);
}

function toggleHandle(response)
{
    receivedResponse = response;
    getEventLog();
    getDevices();
}

function getTasks()
{
    // Command sent to the server.
    var data = "getTasks";

    // The HTTP request sent to server.
    getHTTPRequest(data, taskHandle);
}

function taskHandle(response)
{
    taskHolder = JSON.parse(response);
    var ul = document.getElementById("taskUL");
    ul.innerHTML = "";

    for (var i = 0; i < taskHolder.length; i++)
    {
        var newLI = document.createElement("LI");
        var newDiv = document.createElement("DIV");
        var newButton = document.createElement("INPUT");
        newDiv.appendChild(newButton);
        newLI.appendChild(newDiv);
        ul.appendChild(newLI);
        
        newDiv.className += "leftcolumndiv";

        newButton.className += "leftcolumnbutton";
        newButton.type = "button";
        newButton.value = taskHolder[i].name;
        newButton.id = taskHolder[i].name;
        newButton.onclick = function(e) {pickTask(e.target.id);};
    }
    
    pickTask(readCookie("chosentask"));
    getEventLog();
}

function pickTask(taskItem)
{
    if (taskItem == null)
        taskItem = taskHolder[0].name;
    
    for (var i = 0; i < taskHolder.length; i++)
    {
        if (taskHolder[i].name == taskItem)
        {
            document.getElementById("taskInfoName").innerHTML = "<a href='#' title='Click to access modify page' onClick='javascript:modifyView(\"" + taskHolder[i].id + "\", \"task\")'>" + taskHolder[i].name + "</a>";
            document.getElementById("taskInfoDevice").innerHTML = taskHolder[i].device;
            
            var action = "";            
            if (taskHolder[i].action == SEND_ENABLE)
                action += "On";
            
            else if (taskHolder[i].action == SEND_DISABLE)
                action += "Off";
                
            else if (taskHolder[i].action == SEND_WRITE)
                action += "Toggle";
            
            
            document.getElementById("taskInfoAction").innerHTML = action;
            document.getElementById("taskInfoEvents").innerHTML = taskHolder[i].schedules;
            document.getElementById("taskInfoIsPermanent").innerHTML = taskHolder[i].ispermanent;
        }
    }
    
    createCookie("chosentask", taskItem, 5);
}

function getSensorControl()
{
    // Command sent to the server.
    var data = "getSensorControl";

    // The HTTP request sent to server.
    getHTTPRequest(data, sensorControlHandle);
}

function sensorControlHandle(response)
{
    //clearList("sensorControlNameList");
    sensorControlHolder = JSON.parse(response);
    var ul = document.getElementById("sensorcontrolUL");
    ul.innerHTML = "";
    
    if (sensorControlHolder.length == 0)
    {
        pickSensorControlAction();
        return;
    }
    

    for (var i = 0; i < sensorControlHolder.length; i++)
    {
        //addItemToList(sensorControlHolder[i].name, "sensorControlNameList");
        
        var newLI = document.createElement("LI");
        var newDiv = document.createElement("DIV");
        var newButton = document.createElement("INPUT");
        newDiv.appendChild(newButton);
        newLI.appendChild(newDiv);
        ul.appendChild(newLI);
        
        newDiv.className += "leftcolumndiv";

        newButton.className += "leftcolumnbutton";
        newButton.type = "button";
        newButton.value = sensorControlHolder[i].name;
        newButton.id = i;
        newButton.onclick = function(e) {pickSensorControlButton(e.target.id);};
    }

    pickSensorControl(readCookie("chosensensorcontrol"));
    getEventLog();
}

function pickSensorControl(sensorControlItem)
{
    if (sensorControlHolder.length == 0)
        return;
    
    if (sensorControlItem == null)
        sensorControlItem = sensorControlHolder[0].name;

    var nameFound = false;
    
    for (var i = 0; i < sensorControlHolder.length; i++)
    {
        if (i == sensorControlItem)
        {
            document.getElementById("sensorcontrolInfoName").innerHTML = "<a href='#' title='Click to access modify page' onClick='javascript:modifyView(\"" + sensorControlHolder[i].name + "\", \"sensorcontrol\")'>" + sensorControlHolder[i].name + "</a>";
            document.getElementById("sensorcontrolInfoDevice").innerHTML = sensorControlHolder[i].device;
            document.getElementById("sensorcontrolInfoSensor").innerHTML = sensorControlHolder[i].sensor;
            document.getElementById("sensorcontrolInfoSensorType").innerHTML = sensorControlHolder[i].sensortype;
            document.getElementById("sensorcontrolInfoReading").innerHTML = sensorControlHolder[i].lastreading;
            document.getElementById("sensorcontrolInfoUpdate").innerHTML = sensorControlHolder[i].lastupdated;
            document.getElementById("sensorcontrolInfoHighThreshold").innerHTML = sensorControlHolder[i].firstthreshold;
            document.getElementById("sensorcontrolInfoHighThresholdAction").innerHTML = sensorControlHolder[i].firstcallback;
            document.getElementById("sensorcontrolInfoLowThreshold").innerHTML = sensorControlHolder[i].secondthreshold;
            document.getElementById("sensorcontrolInfoLowThresholdAction").innerHTML = sensorControlHolder[i].secondcallback;
            document.getElementById("sensorcontrolInfoIsRunning").innerHTML = sensorControlHolder[i].isrunning;
            /*
            var action = "";            
            if (taskHolder[i].action == SEND_ENABLE)
                action += "On";
            
            else if (taskHolder[i].action == SEND_DISABLE)
                action += "Off";
                
            else if (taskHolder[i].action == SEND_WRITE)
                action += "Toggle";
            
            
            document.getElementById("taskAction").innerHTML = action;
            document.getElementById("taskEvents").innerHTML = taskHolder[i].schedules;
            document.getElementById("taskIsPermanent").innerHTML = taskHolder[i].ispermanent;
            
            nameFound = true;
            elem.innerHTML += "Name: " + sensorControlHolder[i].name + "<br>";
            elem.innerHTML += "Device: " + sensorControlHolder[i].devicename + "<br>";
            elem.innerHTML += "Sensor: " + sensorControlHolder[i].sensorname + "<br>";
            elem.innerHTML += "Last reading: " + sensorControlHolder[i].lastreading + "<br>";
            var date = new Date(sensorControlHolder[i].lastupdated*1000).toString();
            elem.innerHTML += "Last update: " + date + "<br>";
            elem.innerHTML += "Is running: " + sensorControlHolder[i].state + "<br>";
            elem.innerHTML += "Sensortype: " + sensorControlHolder[i].sensortype + "<br>";
            elem.innerHTML += "High threshold: " + sensorControlHolder[i].highthreshold + "<br>";
            elem.innerHTML += "High threshold action: ";
            
            if (sensorControlHolder[i].highcallback == ON)
                elem.innerHTML += "on <br>";
            
            else
                elem.innerHTML += "off <br>";
            
            elem.innerHTML += "Low threshold: " + sensorControlHolder[i].lowthreshold + "<br>";
            elem.innerHTML += "Low threshold order: ";
            
            if (sensorControlHolder[i].lowcallback == OFF)
                elem.innerHTML += "off <br>";
            
            else
                elem.innerHTML += "on <br";
            */
        }
    }
    
    if (!nameFound && sensorControlHolder.length > 0)
        pickSensorControl(0);
    
    pickSensorControlAction();
}

function pickSensorControlButton(sensorcontrolItem)
{
    createCookie("chosensensorcontrol", sensorcontrolItem, 5);
    getSensorControl();
}

function fillSensorControlActionList()
{
    addItemToList("Add", "sensorControlActionList");
    addItemToList("Modify", "sensorControlActionList");
    addItemToList("Delete", "sensorControlActionList");
    
    document.getElementById("sensorControlActionList").selectedIndex = 0;
}

function fillSensorControlActionLists()
{
    addItemToList("Turn on", "sensorControlFirstActionList");
    addItemToList("Turn off", "sensorControlFirstActionList");
    
    document.getElementById("sensorControlFirstActionList").selectedIndex = 0;
    
    addItemToList("Turn on", "sensorControlSecondActionList");
    addItemToList("Turn off", "sensorControlSecondActionList");
    
    document.getElementById("sensorControlSecondActionList").selectedIndex = 1;
}

function fillSensorControlLists()
{
    fillSensorControlActionList();
    fillSensorControlActionLists();
    pickSensorControlToggleAction(1);
}

function pickSensorControlToggleAction(index)
{
    if (index == 1)
    {
        if (document.getElementById("sensorControlFirstActionList").selectedIndex == 0)
            document.getElementById("sensorControlSecondActionList").selectedIndex = 1;
        
        else if (document.getElementById("sensorControlFirstActionList").selectedIndex == 1)
            document.getElementById("sensorControlSecondActionList").selectedIndex = 0;
    }
    
    else if (index == 2)
    {
        if (document.getElementById("sensorControlSecondActionList").selectedIndex == 0)
            document.getElementById("sensorControlFirstActionList").selectedIndex = 1;
        
        else if (document.getElementById("sensorControlSecondActionList").selectedIndex == 1)
            document.getElementById("sensorControlFirstActionList").selectedIndex = 0;
    }
}

function pickSensorControlAction()
{
    var sensorControlActionList = document.getElementById("sensorControlActionList");
    /*var sensorControlItem = sensorControlActionList.options[sensorControlActionList.selectedIndex].text;

    if (sensorControlItem == "Add")
    {
        document.getElementById("sensorControlDelForm").style.display = "none";
        document.getElementById("sensorControlAddForm").style.display = "block";
    }
    
    else if (sensorControlItem == "Modify")
    {
        document.getElementById("sensorControlDelForm").style.display = "none";
        document.getElementById("sensorControlAddForm").style.display = "block";
        var sensorControlName = sensorControlHolder[readCookie("chosensensorcontrol")].name;
        
        for (var i = 0; i < sensorControlHolder.length; i++)
        {
            if (sensorControlHolder[i].name == sensorControlName)
            {
                document.getElementById("sensorControlName").value = sensorControlName;
                var sensorControlDeviceList = document.getElementById("sensorControlDeviceList");
                
                for (var j = 0; j < sensorControlDeviceList.length; j++)
                    if (sensorControlDeviceList[j].value == sensorControlHolder[i].devicename)
                        sensorControlDeviceList[j].selected = true;
                        
                var sensorControlSensorList = document.getElementById("sensorControlSensorList");
                
                for (var j = 0; j < sensorControlSensorList.length; j++)
                    if (sensorControlSensorList[j].value == sensorControlHolder[i].sensorname)
                        sensorControlSensorList[j].selected = true;

                if (sensorControlHolder[i].firstcallback == ON)
                    pickSensorControlToggleAction(1);
                    
                else if (sensorControlHolder[i].firstcallback == OFF)
                    pickSensorControlToggleAction(2);
                    
                document.getElementById("sensorControlHighThreshold").value = sensorControlHolder[i].highthreshold;
                document.getElementById("sensorControlLowThreshold").value = sensorControlHolder[i].lowthreshold;
            }
        }
    }
    
    else if (sensorControlItem == "Delete")
    {
        document.getElementById("sensorControlDelForm").style.display = "block";
        document.getElementById("sensorControlAddForm").style.display = "none";
    }*/
}

function executeSensorControlAction()
{
    var sensorControlActionList = document.getElementById("sensorControlActionList");
    var chosenAction = sensorControlActionList.options[sensorControlActionList.selectedIndex].text;
    var sensorControlName = document.getElementById("sensorControlName").value;

    if (chosenAction == "Add" || chosenAction == "Modify")
    {
        var sensorControlDeviceList = document.getElementById("sensorControlDeviceList");
        var chosenDevice = sensorControlDeviceList.options[sensorControlDeviceList.selectedIndex].text;
        var sensorControlSensorList = document.getElementById("sensorControlSensorList");
        var chosenSensor = sensorControlSensorList.options[sensorControlSensorList.selectedIndex].text;
        var highThreshold = document.getElementById("sensorControlHighThreshold").value;
        var lowThreshold = document.getElementById("sensorControlLowThreshold").value;
        var sensorType = "";
            
        for (var i = 0; i < sensorHolder.length; i++)
            if (sensorHolder[i].name == chosenSensor)
                sensorType = sensorHolder[i].type;

        var isInverted = 0;
        
        if (document.getElementById("sensorControlFirstActionList").selectedIndex == 1)
            isInverted = 1;
        
        if (chosenAction == "Add") sensorControlAction = "sensorControl add ";
        else if (chosenAction == "Modify") sensorControlAction = "sensorControl modify ";
        
        var data = sensorControlAction + sensorControlName + ";" + chosenDevice + ";" + chosenSensor + ";" + sensorType + ";" + highThreshold + ";" + lowThreshold + ";" + isInverted;
        postHTTPRequest(data, executeSensorControlActionHandle);
    }

    else if (chosenAction == "Delete")
    {
        var sensorControlNameList = document.getElementById("sensorControlNameList");
        var sensorControlItem = sensorControlNameList.options[sensorControlNameList.selectedIndex].text;
        data = "sensorControl del " + sensorControlItem + ";0";
        postHTTPRequest(data, executeSensorControlActionHandle);
    }
    getSensorControl();
}

function executeSensorControlActionHandle(response)
{
    receivedResponse = response;
    document.getElementById("sensorControlResponseLabel").innerHTML = receivedResponse;
}

function getEventLog()
{
    // Command sent to the server.
    var data = "getEvents";

    // The HTTP request sent to server.
    getHTTPRequest(data, eventLogHandle);
}

function eventLogHandle(response)
{
    eventLogHolder = JSON.parse(response);
    var elem = document.getElementById("eventLogDataLabel");
    elem.innerHTML = "";
    
    for (var i = 0; i < eventLogHolder.length; i++)
        elem.innerHTML += eventLogHolder[i] + "<br>";
}

function getSettings()
{
    // Command sent to the server.
    var data = "getIntervals";

    // The HTTP request sent to server.
    getHTTPRequest(data, intervalHandle);
}

function intervalHandle(response)
{
    intervalHolder = JSON.parse(response);
    document.getElementById("loggingIntervalReadingLabel").innerHTML = "Current value " + intervalHolder[0].logginginterval + " minutes";
    document.getElementById("dailyplotsIntervalReadingLabel").innerHTML = "Current value " + intervalHolder[0].dailyplotinterval + " minutes";
    document.getElementById("weeklyplotsIntervalReadingLabel").innerHTML = "Current value " + intervalHolder[0].weeklyplotinterval + " minutes";
    document.getElementById("sensorcontrolIntervalReadingLabel").innerHTML = "Current value " + intervalHolder[0].sensorcontrolinterval + " minutes";
    document.getElementById("eventLogLengthReadingLabel").innerHTML = "Current value " + intervalHolder[0].eventloglength + " lines";
}

function changeInterval(index)
{
    var data = "";
    
    if (index == 0)
        data = "settings;logginginterval;" + document.getElementById("loggingIntervalValue").value;
        
    else if (index == 1)
        data = "settings;dailyplotinterval;" + document.getElementById("dailyplotsIntervalValue").value;
        
    else if (index == 2)
        data = "settings;weeklyplotinterval;" + document.getElementById("weeklyplotsIntervalValue").value;
        
    else if (index == 3)
        data = "settings;sensorcontrolinterval;" + document.getElementById("sensorcontrolIntervalValue").value;
    
    else if (index == 4)
    {
        document.getElementById("settingsResponseLabel").innerHTML = "Shutting down";
        data = "settings;shutdown;0";
    }
    
    else if (index == 5)
        data = "settings;eventloglength;" + document.getElementById("eventLogLengthValue").value;
    
    postHTTPRequest(data, changeIntervalResponse);
}

function changeIntervalResponse(response)
{
    document.getElementById("settingsResponseLabel").innerHTML = response;
    getSettings();
    getEventLog();
    
}

function setMenu(menu, activeButton) {
    var submenu = document.getElementById("submenu");
    var submenuArr = submenu.getElementsByClassName("submenu");
    
    for (var i = 0; i < submenuArr.length; i++) {
        if (submenuArr[i].id == menu.id) {
            submenuArr[i].style.display = "block";
            createCookie("currentsubmenu", menu.id + " " + activeButton.id, 5);
        }
        
        else if (submenuArr[i].style.display != "none")
            submenuArr[i].style.display = "none";
    }
    
    var menuDiv = document.getElementById("menu");
    var inputArr = menuDiv.getElementsByTagName("input");
    
    for (var i = 0; i < inputArr.length; i++) {
        if (inputArr[i].id == activeButton.id)
            inputArr[i].className = "chosenmenubutton";
        
        else if (inputArr[i].className != "menubutton")
            inputArr[i].className = "menubutton";
    }
    
    var page = readCookie(menu.id);
    
    if (page != null) {
        page = page.split(" ");
        setSubMenu(document.getElementById(page[0]), document.getElementById(page[1]), document.getElementById(page[2]));
    }
    
    else {
        var prefix = menu.id.split("_")[1];
        setSubMenu(document.getElementById(menu.id), document.getElementById(prefix + "Page"), document.getElementById(prefix + "Container"));
    }
}

function setSubMenu(menu, activeButton, container) {
    var body = document.getElementById("body");
    var containerArr = body.getElementsByClassName("container");
    
    for (var i = 0; i < containerArr.length; i++) {
        if (containerArr[i].id == container.id) {
            reloadPage(container.id.split("Container")[0]);
            
            if (containerArr[i].id.indexOf("management") != -1) {
                var originalString = containerArr[i].id.split("management")[0];
                var tmp = originalString.charAt(0).toUpperCase() + originalString.substring(1);
                document.getElementById(originalString + "Id").value = "";
                document.getElementById("add" + tmp).disabled = false;
                
                //var form = containerArr[i].id.split("Container")[0] + "Form";
                //var elem = document.getElementById(form);
                
                /*for (var j = 0; j < elem.elements.length; j++) {
                    //console.log(elem.elements[i].id);
                    //elem.elements[i].value = undefined;
                }*/
            }
            
            containerArr[i].style.display = "block";
            createCookie(menu.id, menu.id + " " + activeButton.id + " " + container.id, 5);
        }
        
        else if (containerArr[i].style.display != "none")
            containerArr[i].style.display = "none";
    }
    
    var inputArr = menu.getElementsByTagName("input");
    
    for (var i = 0; i < inputArr.length; i++) {
        if (inputArr[i].id == activeButton.id)
            inputArr[i].className = "chosensubmenubutton";
        
        else if (inputArr[i].className != "submenubutton")
            inputArr[i].className = "submenubutton";
    }
}

function getPage()
{
    var submenu = readCookie("currentsubmenu");
    
    if (submenu == null) {
        setMenu(document.getElementById("submenu_sensor"), document.getElementById("sensorsButton"));
        submenu = readCookie("currentsubmenu");
        submenu = submenu.split(" ");
    }
    
    else {
        submenu = submenu.split(" ");
        setMenu(document.getElementById(submenu[0]), document.getElementById(submenu[1]));
    }
    
    var page = readCookie(submenu[0]);
    
    if (page == null)
        setSubMenu(document.getElementById("submenu_sensor"), document.getElementById("sensorPage"), document.getElementById("sensorForm"));
    
    else {
        page = page.split(" ");
        setSubMenu(document.getElementById(page[0]), document.getElementById(page[1]), document.getElementById(page[2]));
    }
}

function reloadPage(page) {
    if (page == "sensor") getSensors();
    else if (page == "device") getDevices();
    else if (page == "task") getTasks();
    else if (page == "sensorcontrol") getSensorControl();
    else if (page == "eventlog") getEventLog();
    else if (page == "settings") getSettings();
}

// Adds a function that needs to be executed on page load.
function addLoadEvent(func)
{
    var onLoad = window.onload;
    
    if (typeof window.onload != "function")
        window.onload = func;
    
    else
    {
        window.onload = function()
        {
            if (onLoad)
                onLoad();
            
            func();
        }
    }
}

addLoadEvent(getSensors);
//addLoadEvent(onLoadPickSensor);
addLoadEvent(getDevices);
addLoadEvent(getTasks);
addLoadEvent(getSensorControl);
addLoadEvent(getEventLog);
addLoadEvent(getSettings);
addLoadEvent(onLoadFillSensorManagement);
addLoadEvent(onLoadFillDeviceManagement);
addLoadEvent(onLoadFillTaskManagement);
//addLoadEvent(fillTaskExecuteActionList);
//addLoadEvent(fillSensorControlLists);
addLoadEvent(getPage);