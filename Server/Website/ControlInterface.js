var sensorHolder;
var deviceHolder;
var taskHolder;
var sensorControlHolder;
var eventLogHolder;
var intervalHolder;

// Messaging protocol constants
var ON = "e";
var OFF = "d";
var FAIL = "f";
var WRITE = "_w";

function postHTTPRequest(url, data, callback)
{
    var request = false;
    
    try
    {
        // Firefox, Opera 8.0+, Safari
        request = new XMLHttpRequest();
    }
    
    catch (e)
    {
        // Internet Explorer
        try
        {
            request = new ActiveXObject("Msxml2.XMLHTTP");
        }
        
        catch (e)
        {
            try
            {
                request = new ActiveXObject("Microsoft.XMLHTTP");
            }
            
            catch (e)
            {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }
    }
    
    request.open("POST", url, true);
    request.onreadystatechange = function()
    {
        if (request.readyState == 4)
            callback(request);
    }
    request.send(data);
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

function addItemToList(text, listName)
{
    // Create an Option object
    var opt = document.createElement("option");
    
    // Add an Option object to Drop Down/List Box
    document.getElementById(listName).options.add(opt);
    
    // Assign text and value to Option object
    opt.text = text;
}

function clearList(listName)
{
    document.getElementById(listName).options.length = 0;
}

function getSensors()
{
    // Command sent to the server.
    var data = "getSensors";

    // The HTTP request sent to server.
    postHTTPRequest("frontpage.html", data, sensorHandle);
}

function sensorHandle(response)
{
    sensorHolder = eval(response.responseText);
    var ul = document.getElementById("sensorUL");
    
    while (ul.firstChild)
        ul.removeChild(ul.firstChild);
    
    for (var i = 0; i < sensorHolder.length; i++)
    {
        addItemToList(sensorHolder[i].name, "sensorControlSensorList");
        
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
        
    var elem = document.getElementById("sensorDataLabel");
    elem.innerHTML = "";
    
    for (var i = 0; i < sensorHolder.length; i++)
    {
        if (sensorHolder[i].name == sensorItem)
        {
            elem.innerHTML += "Name: " + sensorHolder[i].name + "<br>";
            elem.innerHTML += "Client: " + sensorHolder[i].clientname + "<br>";
            elem.innerHTML += "Index: " + sensorHolder[i].index + "<br>";
            elem.innerHTML += "Type: " + sensorHolder[i].type + "<br>";
            elem.innerHTML += "Last reading: " + sensorHolder[i].lastreading;
            
            if (sensorHolder[i].type == "temp")
                elem.innerHTML += " C";
            
            else if (sensorHolder[i].type == "humidity")
                elem.innerHTML += " %";
            
            else if (sensorHolder[i].type == "ultrasound")
                elem.innerHTML += " cm";
            
            elem.innerHTML += "<br>";
            elem.innerHTML += "Last update: " + sensorHolder[i].lastupdated + "<br>";
            elem.innerHTML += "Lowthreshold: " + sensorHolder[i].lowthreshold + "<br>";
            elem.innerHTML += "Highthreshold: " + sensorHolder[i].highthreshold + "<br>";
            
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
        
    var imageLocation = sensor.name.replace(" ", "") + "-" + sensor.index + "-" + sensor.type + ".png";
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
    createCookie("chosensensor", sensorItem, 1);
    getSensors();
}

function getDevices()
{
    // Command sent to the server.
    var data = "getDevices";

    // The HTTP request sent to server.
    postHTTPRequest("frontpage.html", data, deviceHandle);
}

function deviceHandle(response)
{
    clearList("taskDeviceList");
    clearList("sensorControlDeviceList");
    deviceHolder = eval(response.responseText);
    var ul = document.getElementById("deviceUL");
    ul.innerHTML = "";

    for (var i = 0; i < deviceHolder.length; i++)
    {
        addItemToList(deviceHolder[i].name, "taskDeviceList");
        addItemToList(deviceHolder[i].name, "sensorControlDeviceList");
        
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
        
        if (deviceHolder[i].isrunning) newDeviceStateDiv.innerHTML = "On";
        else newDeviceStateDiv.innerHTML = "Off";
        
        newDeviceNameDiv.innerHTML = deviceHolder[i].name;
        
        var newOffButton= document.createElement("INPUT");
        newDeviceContainerDiv.appendChild(newOffButton);
        newOffButton.className += "devicebutton";
        newOffButton.type = "button";
        newOffButton.value = "Off";
        newOffButton.name = OFF;
        newOffButton.id = deviceHolder[i].index;
        newOffButton.onclick = function(e) {toggleDevice(e.target.name, e.target.id);};
        
        var newOnButton = document.createElement("INPUT");
        newDeviceContainerDiv.appendChild(newOnButton);
        newOnButton.className += "devicebutton";
        newOnButton.type = "button";
        newOnButton.value = "On";
        newOnButton.name = ON;
        newOnButton.id = deviceHolder[i].index;
        newOnButton.onclick = function(e) {toggleDevice(e.target.name, e.target.id);};
    }
}

function toggleDevice(action, index)
{
    data = "controlDevice;" + index + ";" + action;
    postHTTPRequest("frontpage.html", data, toggleHandle);
}

function toggleHandle(response)
{
    receivedResponse = response.responseText;
    getEventLog();
    getDevices();
}

function getTasks()
{
    // Command sent to the server.
    var data = "getTasks";

    // The HTTP request sent to server.
    postHTTPRequest("frontpage.html", data, taskHandle);
}

function taskHandle(response)
{
    clearList("taskNameList");
    taskHolder = eval(response.responseText);
    var ul = document.getElementById("taskUL");
    ul.innerHTML = "";

    for (var i = 0; i < taskHolder.length; i++)
    {
        addItemToList(taskHolder[i].name, "taskNameList");
        
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

    var elem = document.getElementById("taskLabel");
    elem.innerHTML = "";
    
    for (var i = 0; i < taskHolder.length; i++)
    {
        if (taskHolder[i].name == taskItem)
        {
            elem.innerHTML += "Name: " + taskHolder[i].name + "<br>";
            elem.innerHTML += "Device: " + taskHolder[i].device + "<br>";
            elem.innerHTML += "Action: ";
            
            if (taskHolder[i].actiontype == ON)
                elem.innerHTML += "On";
            
            else if (taskHolder[i].actiontype == OFF)
                elem.innerHTML += "Off";
                
            else if (taskHolder[i].actiontype == WRITE)
                elem.innerHTML += "Toggle";
            
            elem.innerHTML += "<br>";
            elem.innerHTML += "Is permanent: " + taskHolder[i].ispermanent + "<br>";
            elem.innerHTML += "Events: " + taskHolder[i].schedules;
        }
    }
    
    createCookie("chosentask", taskItem, 1);
    pickTaskAction();
}

function fillTaskActionList()
{
    addItemToList("Add", "taskActionList");
    addItemToList("Modify", "taskActionList");
    addItemToList("Delete", "taskActionList");
    
    document.getElementById("taskActionList").selectedIndex = 0;
    //pickTaskAction();
}

function pickTaskAction()
{
    var taskActionList = document.getElementById("taskActionList");
    var taskItem = taskActionList.options[taskActionList.selectedIndex].text;
    
    if (taskItem == "Add")
    {
        document.getElementById("taskDel").style.display = "none";
        document.getElementById("taskAdd").style.display = "block";
    }
    
    else if (taskItem == "Modify")
    {
        document.getElementById("taskDel").style.display = "none";
        document.getElementById("taskAdd").style.display = "block";
        var taskName = readCookie("chosentask");
        
        for (var i = 0; i < taskHolder.length; i++)
        {
            if (taskHolder[i].name == taskName)
            {
                document.getElementById("taskName").value = taskName;
                var taskDeviceList = document.getElementById("taskDeviceList")
                
                for (var j = 0; j < taskDeviceList.length; j++)
                    if (taskDeviceList[j].value == taskHolder[i].device)
                        taskDeviceList[j].selected = true;
                        
                if (taskHolder[i].actiontype == ON)
                    document.getElementById("taskExecuteActionList").selectedIndex = 0;
                
                else if (taskHolder[i].actiontype == OFF)
                    document.getElementById("taskExecuteActionList").selectedIndex = 1;
                
                else if (taskHolder[i].actiontype == WRITE)
                    document.getElementById("taskExecuteActionList").selectedIndex = 2;
                
                if (!taskHolder[i].ispermanent)
                {
                    document.getElementById("taskIsTemporaryCheckbox").checked = true;
                    document.getElementById("taskSchedules").value = taskHolder[i].schedules.join(", ");
                }
                
                else
                {
                    document.getElementById("taskIsTemporaryCheckbox").checked = false;
                    document.getElementById("taskSchedules").value = taskHolder[i].schedules.join(", ");
                }
            }
        }
    }
    
    else if (taskItem == "Delete")
    {
        document.getElementById("taskDel").style.display = "block";
        document.getElementById("taskAdd").style.display = "none";
    }
}

function fillTaskExecuteActionList()
{
    addItemToList("On", "taskExecuteActionList");
    addItemToList("Off", "taskExecuteActionList");
    addItemToList("Toggle", "taskExecuteActionList");
    
    document.getElementById("taskExecuteActionList").selectedIndex = 0;
}

function executeTaskAction()
{
    var taskActionList = document.getElementById("taskActionList");
    
    // Put the sensorLists selected item as chosenSensor's text value.
    chosenAction = taskActionList.options[taskActionList.selectedIndex].text;
    var elem = document.getElementById("taskResponseLabel");

    var taskName = document.getElementById("taskName");
    
    if (chosenAction == "Add" || chosenAction == "Modify")
    {
        var taskDeviceList = document.getElementById("taskDeviceList");
        var chosenDevice = taskDeviceList.options[taskDeviceList.selectedIndex].text;
        var taskSchedules = document.getElementById("taskSchedules").value.replace(/[,]/g, "").split(" ");
        var isPermanent = true;
            
        if (document.getElementById("taskIsTemporaryCheckbox").checked)
            isPermanent = false;

        var tmpSchedules = "";
        var taskAction = "";
        
        if (chosenAction == "Add") taskAction = "task add ";
        else if (chosenAction == "Modify") taskAction = "task modify ";
        
        var data = "";
            
        for (var i = 0; i < taskSchedules.length; i++)
            tmpSchedules += taskSchedules[i] + ",";
            
        if (document.getElementById("taskExecuteActionList").selectedIndex == 0)
            data = taskAction + taskName.value + ";" + chosenDevice + ";" + ON + ";" + isPermanent + ";" + tmpSchedules;
            
        else if (document.getElementById("taskExecuteActionList").selectedIndex == 1)
            data = taskAction + taskName.value + ";" + chosenDevice + ";" + OFF + ";" + isPermanent + ";" + tmpSchedules;

        else if (document.getElementById("taskExecuteActionList").selectedIndex == 2)
            data = taskAction + taskName.value + ";" + chosenDevice + ";" + WRITE + ";" + isPermanent + ";" + tmpSchedules;

        postHTTPRequest("frontpage.html", data, executeTaskActionHandle);
    }
    
    else if (chosenAction == "Delete")
    {
        var taskNameList = document.getElementById("taskNameList");
        var taskItem = taskNameList.options[taskNameList.selectedIndex].text;
        data = "task del " + taskItem;
        postHTTPRequest("frontpage.html", data, executeTaskActionHandle);
    }
    
    getTasks();
}

function executeTaskActionHandle(response)
{
    receivedResponse = response.responseText;
    var elem = document.getElementById("taskResponseLabel");
    elem.innerHTML = receivedResponse;
}

function getSensorControl()
{
    // Command sent to the server.
    var data = "getSensorControl";

    // The HTTP request sent to server.
    postHTTPRequest("frontpage.html", data, sensorControlHandle);
}

function sensorControlHandle(response)
{
    clearList("sensorControlNameList");
    sensorControlHolder = eval(response.responseText);
    var ul = document.getElementById("sensorcontrolUL");
    ul.innerHTML = "";
    
    if (sensorControlHolder.length == 0)
    {
        pickSensorControlAction();
        return;
    }
    

    for (var i = 0; i < sensorControlHolder.length; i++)
    {
        addItemToList(sensorControlHolder[i].name, "sensorControlNameList");
        
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
    
    var elem = document.getElementById("sensorControlDataLabel");
    elem.innerHTML = "";
    var nameFound = false;
    
    for (var i = 0; i < sensorControlHolder.length; i++)
    {
        if (i == sensorControlItem)
        {
            nameFound = true;
            elem.innerHTML += "Name: " + sensorControlHolder[i].name + "<br>";
            elem.innerHTML += "Device: " + sensorControlHolder[i].devicename + "<br>";
            elem.innerHTML += "Sensor: " + sensorControlHolder[i].sensorname + "<br>";
            elem.innerHTML += "Last reading: " + sensorControlHolder[i].lastreading + "<br>";
            //var date = new Date(sensorControlHolder[i].lastupdated*1000).toString();
            elem.innerHTML += "Last update: " + sensorControlHolder[i].lastupdated + "<br>";
            elem.innerHTML += "Is running: " + sensorControlHolder[i].isrunning + "<br>";
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
            
        }
    }
    
    if (!nameFound && sensorControlHolder.length > 0)
        pickSensorControl(0);
    
    pickSensorControlAction();
}

function pickSensorControlButton(sensorcontrolItem)
{
    createCookie("chosensensorcontrol", sensorcontrolItem, 1);
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
    var sensorControlItem = sensorControlActionList.options[sensorControlActionList.selectedIndex].text;

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
    }
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
        postHTTPRequest("frontpage.html", data, executeSensorControlActionHandle);
    }

    else if (chosenAction == "Delete")
    {
        var sensorControlNameList = document.getElementById("sensorControlNameList");
        var sensorControlItem = sensorControlNameList.options[sensorControlNameList.selectedIndex].text;
        data = "sensorControl del " + sensorControlItem + ";0";
        postHTTPRequest("frontpage.html", data, executeSensorControlActionHandle);
    }
    getSensorControl();
}

function executeSensorControlActionHandle(response)
{
    receivedResponse = response.responseText;
    document.getElementById("sensorControlResponseLabel").innerHTML = receivedResponse;
}

function getEventLog()
{
    // Command sent to the server.
    var data = "getEvents";

    // The HTTP request sent to server.
    postHTTPRequest("frontpage.html", data, eventLogHandle);
}

function eventLogHandle(response)
{
    eventLogHolder = eval(response.responseText);
    var elem = document.getElementById("eventLogDataLabel");
    elem.innerHTML = "";
    
    for (var i = 0; i < eventLogHolder.length; i++)
        elem.innerHTML += eventLogHolder[i] + "<br>";
}

function getIntervals()
{
    // Command sent to the server.
    var data = "getIntervals";

    // The HTTP request sent to server.
    postHTTPRequest("frontpage.html", data, intervalHandle);
}

function intervalHandle(response)
{
    intervalHolder = eval(response.responseText);
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
    
    postHTTPRequest("frontpage.html", data, changeIntervalResponse);
}

function changeIntervalResponse(response)
{
    document.getElementById("settingsResponseLabel").innerHTML = response.responseText;
    getIntervals();
    getEventLog();
    
}

function showSensors()
{
    document.getElementById("sensorDeviceForm").style.display = "block";
    document.getElementById("deviceForm").style.display = "none";
    document.getElementById("taskForm").style.display = "none";
    document.getElementById("sensorControlForm").style.display = "none";
    document.getElementById("eventLogForm").style.display = "none";
    document.getElementById("settingsForm").style.display = "none";
    
    createCookie("currentpage", "sensor", 1);
}

function showTasks()
{
    document.getElementById("sensorDeviceForm").style.display = "none";
    document.getElementById("deviceForm").style.display = "none";
    document.getElementById("taskForm").style.display = "block";
    document.getElementById("sensorControlForm").style.display = "none";
    document.getElementById("eventLogForm").style.display = "none";
    document.getElementById("settingsForm").style.display = "none";
    
    createCookie("currentpage", "task", 1);
}

function showDevices()
{
    document.getElementById("sensorDeviceForm").style.display = "none";
    document.getElementById("deviceForm").style.display = "block";
    document.getElementById("taskForm").style.display = "none";
    document.getElementById("sensorControlForm").style.display = "none";
    document.getElementById("eventLogForm").style.display = "none";
    document.getElementById("settingsForm").style.display = "none";
    
    createCookie("currentpage", "device", 1);
}

function showSensorControl()
{
    getSensorControl();
    document.getElementById("sensorDeviceForm").style.display = "none";
    document.getElementById("deviceForm").style.display = "none";
    document.getElementById("taskForm").style.display = "none";
    document.getElementById("sensorControlForm").style.display = "block";
    document.getElementById("eventLogForm").style.display = "none";
    document.getElementById("settingsForm").style.display = "none";
    
    createCookie("currentpage", "sensorcontrol", 1);
}

function showEventLog()
{
    getEventLog();
    document.getElementById("sensorDeviceForm").style.display = "none";
    document.getElementById("deviceForm").style.display = "none";
    document.getElementById("taskForm").style.display = "none";
    document.getElementById("sensorControlForm").style.display = "none";
    document.getElementById("eventLogForm").style.display = "block";
    document.getElementById("settingsForm").style.display = "none";
    
    createCookie("currentpage", "eventlog", 1);
}

function showSettings()
{
    document.getElementById("sensorDeviceForm").style.display = "none";
    document.getElementById("deviceForm").style.display = "none";
    document.getElementById("taskForm").style.display = "none";
    document.getElementById("sensorControlForm").style.display = "none";
    document.getElementById("eventLogForm").style.display = "none";
    document.getElementById("settingsForm").style.display = "block";
    
    createCookie("currentpage", "settings", 1);
}

function getPage()
{
    page = readCookie("currentpage");
    
    if (page == null) showSensors();
    
    else if (page == "sensor") showSensors();
    else if (page == "device") showDevices();
    else if (page == "task") showTasks();
    else if (page == "sensorcontrol") showSensorControl();
    else if (page == "eventlog") showEventLog();
    else if (page == "settings") showSettings();
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
addLoadEvent(getIntervals);
addLoadEvent(fillTaskActionList);
addLoadEvent(fillTaskExecuteActionList);
addLoadEvent(fillSensorControlLists);
addLoadEvent(getPage);