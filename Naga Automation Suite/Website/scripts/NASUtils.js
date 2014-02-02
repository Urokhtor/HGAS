/*
 * Constants and global variables.
 *
 */
 
var PAGE_FETCH = 403;
var TABLE_FETCH = 404;
var FORM_SUBMIT = 405;
var PRESERVE_COOKIE = 5; // For how many days to store the cookie.
var currentPage = ""; // Keep track of the current page. Needs to be supplied to server in cases like fetching sensor data from server. BUT IS THIS SECURE?
var defaultFadeout = 5000;

/*
 * Utility functions
 * 
 */
function postHTTPRequest(data, callback) {
    jQuery.post("frontpage_test.html", JSON.stringify(data), function(result) {callback(result)});
}

function getHTTPRequest(data, callback) {
    jQuery.get("frontpage_test.html", JSON.stringify(data), function(result) {callback(result)});
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
        addParameter(newElem, "type", child);
        addParameter(newElem, "value", child);
        addParameter(newElem, "action", child);
        addParameter(newElem, "innerHTML", child);
        addParameter(newElem, "src", child);
        addParameter(newElem, "href", child);
        addParameter(newElem, "selected", child);
        addParameter(newElem, "disabled", child);
        addParameter(newElem, "width", child);
        addParameter(newElem, "height", child);
        addParameter(newElem, "method", child);
        addParameter(newElem, "checked", child);
        
        // Register the event functions which can accept arguments in list format like:
        // ["functionName", "arg1", "arg2", ...]
        if (child["onclick"]) {
            var params = child["onclick"].split(",");
            newElem.onclick = (function(event) {
                var currParams = params;
                return function(event) {
                    window[currParams[0]](currParams);
                }
            })();
        }
        
        if (child["onload"]) {
            var params = child["onload"].split(",");
            newElem.onload = (function(event) {
                var currParams = params;
                return function(event) {
                    window[currParams[0]](currParams);
                }
            })();
        }
        
        if (child["onchange"]) {
            var params = child["onchange"].split(",");
            newElem.onchange = (function(event) {
                var currParams = params;
                return function(event) {
                    window[currParams[0]](currParams);
                }
            })();
        }
        
        element.appendChild(newElem);
        
        // Our current object has child elements to recursively add its children.
        if (object["childcount"]) recursiveGenerator(newElem, child);
    }
}

function doSubmit(params) {
    var formId = params[1];
    var mode = params[2];
    
    var form = document.getElementById(formId);
    var formData = {};
    
    for (var i = 0; i < form.elements.length; i++) {
        if (form.elements[i].type == "checkbox")
            formData[form.elements[i].id] = form.elements[i].checked;
        
        else
            formData[form.elements[i].id] = form.elements[i].value;
    }
    
    data = {};
    data["name"] = currentPage;
    data["params"] = {};
    data["params"]["id"] = formId;
    data["params"]["mode"] = mode;
    data["params"]["form"] = formData;
    data["action"] = FORM_SUBMIT;
    
    postHTTPRequest(data, formResponse);
}

function formResponse(_response) {
    console.log(_response);
    var tmp = _response.replace(/\\"/g, "'").replace(/"/g, "").replace(/'/g, "\"");
    response = JSON.parse(tmp);
    console.log(response);
    
    // This is here before we finish these changes.
    if (response["response"]) {
        response["success"] = response["response"];
    }
    
    var delay = defaultFadeout;
    var notificationType = "";
    var notificationElements;
    
    if (response["fadeout"]) {
        delay = response["fadeout"]*1000;
    }
    
    if (response["success"]) {
        notificationType = "success";
        notificationElements = response["success"];
    } else if (response["error"]) {
        notificationElements = response["error"];
        notificationType = "error";
    }
    
    // In future we want to create a new container for each message.
    for (var i = 0; i < notificationElements.length; i++) {
        // This currently handles one notificationContainer. Should we support multiple?
        if (notificationElements[i]["id"] === "notificationContainer") {
            $("#notificationContainer").html(notificationElements[i]["text"]);
            $("#notificationContainer").addClass(notificationType);
            setTimeout(function() {
                $("#notificationContainer").removeClass(notificationType);
                $("#notificationContainer").html("");
            }, delay);
        } else {
            // Put errors to elements.
        }
    }
    
    if (response["redirect"]) {
        var params = response["redirect"].split(",");
        window[params[0]](params);
    }
}

String.prototype.startsWith = function(prefix) {
    return this.indexOf(prefix) == 0;
};

String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};
