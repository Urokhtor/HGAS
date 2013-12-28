/*
 * Constants
 *
 */
 
var PAGE_FETCH = 403;

/*
 * Utility functions
 * 
 */
function postHTTPRequest(message, callback) {
    jQuery.post("frontpage_test.html", message, function(result) {callback(result)});
}

function getHTTPRequest(message, callback) {
    jQuery.get("frontpage_test.html", message, function(result) {callback(result)});
}

function createCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
    
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
    
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
    
	return null;
}

function addParameter(element, parameter, source) {
    if (source[parameter]) element[parameter] = source[parameter];
}

function recursiveGenerator(element, object) {
    for (var i = 1; i <= object["childcount"]; i++) {
        var child = object["child"+i];
        //console.log(child);
        
        var newElem =  document.createElement(child["element"]);
        addParameter(newElem, "id", child);
        addParameter(newElem, "name", child);
        addParameter(newElem, "className", child);
        addParameter(newElem, "style", child);
        addParameter(newElem, "width", child);
        addParameter(newElem, "height", child);
        addParameter(newElem, "src", child);
        addParameter(newElem, "type", child);
        addParameter(newElem, "value", child);
        addParameter(newElem, "onclick", child);
        addParameter(newElem, "method", child);
        addParameter(newElem, "action", child);
        addParameter(newElem, "innerHTML", child);
        addParameter(newElem, "href", child);
        
        element.appendChild(newElem);
        //console.log(element.innerHTML);
        
        if (object["childcount"]) recursiveGenerator(newElem, child);
    
    }
}

/* ==================== End of utility functions ==================== */

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
        setSubMenu(document.getElementById(menu.id), document.getElementById(prefix + "Page"));
    }
}

function setSubMenu(menu, activeButton, container) {
    //var body = document.getElementById("body");
    //var containerArr = body.getElementsByClassName("container");
    //var mainContainer = document.getElementById("mainContainer");
    
    //console.log(menu);
    //console.log(activeButton);
    //console.log(container);
    data = {};
    data["type"] = "view";
    data["name"] = "SensorViewController";
    data["action"] = PAGE_FETCH;
    
    postHTTPRequest(JSON.stringify(data), generatePage);
    
    /*for (var i = 0; i < containerArr.length; i++) {
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
        /*    }
            
            containerArr[i].style.display = "block";
            createCookie(menu.id, menu.id + " " + activeButton.id + " " + container.id, 5);
        }
        
        else if (containerArr[i].style.display != "none")
            containerArr[i].style.display = "none";
    }
    */
    var inputArr = menu.getElementsByTagName("input");
    
    for (var i = 0; i < inputArr.length; i++) {
        if (inputArr[i].id == activeButton.id)
            inputArr[i].className = "chosensubmenubutton";
        
        else if (inputArr[i].className != "submenubutton")
            inputArr[i].className = "submenubutton";
    }
}

function setPage(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    //console.log(tmp);
    var response = JSON.parse(tmp);
    var mainContainer = document.getElementById("mainContainer");
    mainContainer.innerHTML = "";
    recursiveGenerator(mainContainer, response["source"]);
    return;
}

function getPage() {
    // First get the menu body and generate it, then check which page to load
    // and finally load the page and generate it.
    
    var data = {};
    data["type"] = "view";
    data["name"] = "NASMenuViewController";
    data["action"] = PAGE_FETCH;
    //console.log(data);
    postHTTPRequest(JSON.stringify(data), generateMenu);
}

function generateMenu(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    var response = JSON.parse(tmp);
    
    // The menu was prerendered at server so glue it in the body.
    if (!response["renderbrowser"]) {
        jQuery("body").html(JSON.stringify(response["source"]));
        return;
    }
    
    var body = response["source"];
    
    var start = new Date().getMilliseconds();
    recursiveGenerator(document.body, body);
    var end = new Date().getMilliseconds();
    console.log("Generating menu took " + (end-start) + " ms");
    
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
    
    /*var page = readCookie(submenu[0]);
    
    if (page == null)
        setSubMenu(document.getElementById("submenu_sensor"), document.getElementById("sensorPage"), document.getElementById("sensorForm"));
    
    else {
        page = page.split(" ");
        setSubMenu(document.getElementById(page[0]), document.getElementById(page[1]), document.getElementById(page[2]));
    }*/
    
    var end2 = new Date().getMilliseconds();
    console.log("Total time spent in generateMenu(): " + (end2-start) + " ms");
}

function generatePage(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    response = JSON.parse(tmp);
    
    var mainContainer = jQuery("mainContainer");
    mainContainer.html("");
    
    if (!response["renderbrowser"]) {
        mainContainer.html(JSON.stringify(response["source"]));
        return;
    }
    
    var container = response["source"];
    var element = document.getElementById("mainContainer");
    element.innerHTML = "";
    var start = new Date().getMilliseconds();
    recursiveGenerator(element, container);
    var end = new Date().getMilliseconds();
    console.log("Page generation took " + (end-start) + " ms");
}

/*window.onclick = function(event) {
    console.log(event);
}*/

// Adds a function that needs to be executed on page load.
function addLoadEvent(func) {
    var onLoad = window.onload;
    
    if (typeof window.onload != "function")
        window.onload = func;
    
    else {
        window.onload = function() {
            if (onLoad)
                onLoad();
            
            func();
        }
    }
}

// On load get the page body from the server and generate it.
addLoadEvent(getPage);

window.onclick = function(e){
  e = e || window.event;
  var from = findParent('a',e.target || e.srcElement);
  if (from){
     /* it's a link, actions here */
     console.log(from);
     console.log(e);
     e.preventDefault();

    var data = {};
    data["type"] = "view";
    data["name"] = "HerpViewController";
    data["action"] = PAGE_FETCH;

     postHTTPRequest(JSON.stringify(data), durp);
  }
}

function durp(response) {
    console.log(response);
}

//find first parent with tagName [tagname]
function findParent(tagname,el){
  if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
    return el;
  }
  while (el = el.parentNode){
    if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
      return el;
    }
  }
  return null;
}