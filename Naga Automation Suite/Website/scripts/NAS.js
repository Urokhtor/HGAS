
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
    
    postHTTPRequest(data, generatePage);
}

function setPage(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
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
    
    postHTTPRequest(data, generateMenu);
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
    recursiveGenerator(document.body, body);
    
    var menu = readCookie("currentmenu");
    
    if (menu == null) {
        setMenu(document.getElementById("submenu_sensor"), document.getElementById("sensorButton"));
    }
    
    else {
        menuArr = menu.split(" ");
        var menuButton = readCookie(menuArr[1]);
        var sourceElement;

        if (!menu) sourceElement = "sensorButton";
        else sourceElement = menuArr[1];
        
        setMenu(document.getElementById(menuArr[0]), document.getElementById(sourceElement));
    }
}

function generatePage(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    response = JSON.parse(tmp);
    
    var mainContainer = document.getElementById("mainContainer");
    mainContainer.innerHTML = "";
    
    if (!response["renderbrowser"]) {
        mainContainer.innerHTML = JSON.stringify(response["source"]);
        return;
    }
    
    var container = response["source"]["child1"];
    var element = document.getElementById("mainContainer");
    element.innerHTML = "";
    recursiveGenerator(element, container);
}

function generateViewTable(_response) {
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    response = JSON.parse(tmp);
    var element = document.getElementById(response["id"]);
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
        
        postHTTPRequest(data, generateViewTable);
    }
}
