/*
 * Constants and global variables.
 *
 */
 
var PAGE_FETCH = 403;
var TABLE_FETCH = 404;
var PRESERVE_COOKIE = 5; // For how many days to store the cookie.
var currentPage = ""; // Keep track of the current page. Needs to be supplied to server in cases like fetching sensor data from server. BUT IS THIS SECURE?

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
        addParameter(newElem, "method", child);
        addParameter(newElem, "action", child);
        addParameter(newElem, "innerHTML", child);
        addParameter(newElem, "href", child);
        addParameter(newElem, "selected", child);
        
        // This implementation below needs to be changed so that we can pass parameters. Currently
        // no parameters can be passed.
        if (child["onclick"]) {
            var params = child["onclick"].split(",");
            newElem.onclick = function() {window[params[0]](params);}
        }
        
        // onload
        if (child["onload"]) {
            var params = child["onload"];
            newElem.onload = function() {window[params[0]](params);}
        }
        
        // onchange
        if (child["onchange"]) {
            var params = child["onchange"];
            newElem.onchange = function() {window[params[0]](params);}
        }
        
        element.appendChild(newElem);
        
        // Our current object has child elements to recursively add its children.
        if (object["childcount"]) recursiveGenerator(newElem, child);
    }
}

String.prototype.startsWith = function(prefix) {
    return this.indexOf(prefix) == 0;
};

String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

/* ==================== End of utility functions ==================== */

function jumpToPage(params) {
    var menuId = params[1];
    var menuButtonId = params[2];
    var subMenuButtonId = params[3];
    var queryParams = {};
    
    for (var i = 4; i < params.length; i++) {
        var tmp = params[i].split(":");
        queryParams[tmp[0]] = tmp[1];
    }
    
    var menu = document.getElementById(menuId);
    var menuButton = document.getElementById(menuButtonId);
    var subMenuButton = document.getElementById(subMenuButtonId);
    
    createCookie(menu.id, menu.id + " " + subMenuButton.id, PRESERVE_COOKIE);
    setMenu(menu, menuButton, queryParams);
}

function setMenu(menu, activeButton, params) {
    if (typeof menu === "string") {
        menu = document.getElementById(menu);
    }
    
    if (typeof activeButton === "string") {
        activeButton = document.getElementById(activeButton);
    }
    
    createCookie("currentmenu", menu.id + " " + activeButton.id, PRESERVE_COOKIE);

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
        setSubMenu(document.getElementById(page[0]), document.getElementById(page[1]), params);
    }
    
    else {
        var prefix = menu.id.split("_")[1];
        setSubMenu(menu, document.getElementById(prefix + "Selectbutton"), params);
    }
}

function setSubMenu(menu, activeButton, params) {
    if (typeof menu === "string") {
        menu = document.getElementById(menu);
    }
    
    if (typeof activeButton === "string") {
        activeButton = document.getElementById(activeButton);
    }
    
    console.log(menu);
    console.log(activeButton);
    
    var container = document.getElementById("submenu");
    var children = container.getElementsByTagName("div");
    
    for (var i = 0; i < children.length; i++) {
        if (activeButton.id.startsWith(children[i].id.split("_")[1])) {
            children[i].style.display = "block";
            createCookie(menu.id, menu.id + " " + activeButton.id, PRESERVE_COOKIE);
        }
        
        else
            children[i].style.display = "none";
    }

    var inputArr = menu.getElementsByTagName("input");
    
    for (var i = 0; i < inputArr.length; i++) {
        if (inputArr[i].id == activeButton.id)
            inputArr[i].className = "chosensubmenubutton";
        
        else if (inputArr[i].className != "submenubutton")
            inputArr[i].className = "submenubutton";
    }
    
    data = {};
    data["name"] = activeButton.id;
    currentPage = activeButton.id;
    data["action"] = PAGE_FETCH;
    
    if (typeof params !== "undefined") {
        data["params"] = params;
    }
    
    postHTTPRequest(JSON.stringify(data), generatePage);
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
    data["name"] = "NASMenuViewController";
    data["action"] = PAGE_FETCH;
    
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
    
    var menu = readCookie("currentmenu");
    
    if (menu == null) {
        console.log("menu == null");
        setMenu(document.getElementById("submenu_sensor"), document.getElementById("sensorButton"));
    }
    
    else {
        console.log("menu != null");
        menuArr = menu.split(" ");
        var menuButton = readCookie(menuArr[1]);
        var sourceElement;

        if (!menu) {
            console.log("!menu");
            sourceElement = "sensorButton";
        }
        
        else {
            console.log("menu");
            sourceElement = menuArr[1];
        }
        
        setMenu(document.getElementById(menuArr[0]), document.getElementById(sourceElement));
    }
    
    var end2 = new Date().getMilliseconds();
    console.log("Total time spent in generateMenu(): " + (end2-start) + " ms");
}

function generatePage(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    response = JSON.parse(tmp);
    
    var mainContainer = document.getElementById("mainContainer");
    mainContainer.innerHTML = "";
    console.log(response);
    if (!response["renderbrowser"]) {
        mainContainer.innerHTML = JSON.stringify(response["source"]);
        return;
    }
    
    var container = response["source"]["child1"];
    var element = document.getElementById("mainContainer");
    element.innerHTML = "";
    var start = new Date().getMilliseconds();
    recursiveGenerator(element, container);
    var end = new Date().getMilliseconds();
    console.log("Page generation took " + (end-start) + " ms");
}

function generateViewTable(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    response = JSON.parse(tmp);
    console.log(response);
    var element = document.getElementById(response["id"]);
    console.log(element);
    element.innerHTML = "";
    recursiveGenerator(element, response);

}

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
    /* 
        We want to sniff button clicks here and distinguish between menu buttons and things like selecting
        sensors.
    */
  
    var id = e.srcElement.id;
    var className = e.srcElement.className;
    
    if (id.endsWith("Button")) {
        var submenuId = id.split("Button")[0];
        var submenu = document.getElementById("submenu_" + submenuId);
        setMenu(submenu, e.srcElement);
    }
    
    else if (id.endsWith("Selectbutton")) {
        var container = document.getElementById("submenu");
        var children = container.getElementsByTagName("div");
        
        for (var i = 0; i < children.length; i++) {
            console.log(children[i]);
            if (id.startsWith(children[i].id.split("_")[1])) {
                setSubMenu(children[i], e.srcElement);
                break;
            }
        }
    }
    
    else if (className === "leftcolumnbutton") {
        data = {};
        data["name"] = currentPage;
        data["params"] = {}
        data["params"]["id"] = id;
        data["action"] = TABLE_FETCH;
        
        postHTTPRequest(JSON.stringify(data), generateViewTable);
    }
  
    /*e = e || window.event;
    var from = findParent('a',e.target || e.srcElement);
    if (from) {
        console.log(from);
        console.log(e);
        e.preventDefault();

        var data = {};
        data["type"] = "view";
        data["name"] = "HerpViewController";
        data["action"] = PAGE_FETCH;

        postHTTPRequest(JSON.stringify(data), durp);
    }*/
}

//find first parent with tagName [tagname]
/*function findParent(tagname,el){
  if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
    return el;
  }
  while (el = el.parentNode){
    if ((el.nodeName || el.tagName).toLowerCase()===tagname.toLowerCase()){
      return el;
    }
  }
  return null;
}*/