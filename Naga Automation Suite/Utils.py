"""
    Naga Automation Suite - an automation system for home gardens
    Copyright (C) 2013  Jere Teittinen
    
    Author: Jere Teittinen <j.teittinen@luukku.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
from Scheduler import Task
from Constants import *

from time import time
from os import path
import traceback

def dispatchRequest(parent, request):
    if not "name" in request:
        return "" # Return some error.

    parent.logging.logDebug("Serving request: " + json.dumps(request))
    module = None

    # Reload the module if needed and then load it for execution.
    try:
        # For debugging purposes reload changes made to the controller. Later on
        # make the front end support reloading modules.
        urlMap = parent.configManager.getConf(CONFIG_URLMAP).items()

        if request["name"] in urlMap:
            moduleName = urlMap[request["name"]]

            if moduleName.find("View") != -1: request["type"] = TYPE_VIEW
            elif moduleName.find("Form") != -1: request["type"] = TYPE_FORM

            reloadIfNeeded(parent, moduleName)
            tmp = time()
            module = parent.moduleManager.getModule("Controllers." + moduleName)
            parent.logging.logDebug("Getting module " + "Controllers." + moduleName + " took: " + str(time()-tmp))

    except Exception as e:
        parent.logging.logDebug("Add error logging here in the dispatchRequest")
        parent.logging.logDebug(str(e))
        traceback.print_exc()
        return '{"' + KEY_ERROR + '": "An error occurred: ' + str(e) + '"}'

    if request["type"] == TYPE_FORM:
        try:
            reject = {}
            reject["errors"] = []
            response = {} # Ugh, this is actually useless.

            if not module is None:
                if request["action"] == PAGE_FETCH:
                    tmp = module.handleRequest(parent, request, response)

                    if isinstance(tmp, str): return tmp
                    else: return json.dumps(tmp)

                #module.fetchResource()

                if request["action"] == FORM_SUBMIT:
                    # Validate the form data and do type conversions.
                    module.validate(parent, request, reject)

                    # Tell the web UI that something went wrong.
                    if "reject" in reject:
                        return reject

                    # If validation was a success, handle the form data.
                    tmp = module.handleSubmit(parent, request, response)

                    if isinstance(tmp, str): return tmp
                    else: return json.dumps(tmp)
            
            else:
                return '{"' + KEY_ERROR + '": "Couldn\'t find module ' + request["name"] + '"}'
        
        except Exception as e:
            parent.logging.logDebug("Add error logging here in the dispatchRequest")
            parent.logging.logDebug(str(e))
            traceback.print_exc()
            return '{"' + KEY_ERROR + '": "An error occurred: ' + str(e) + '"}'
    
    elif request["type"] == TYPE_VIEW:
        try:
            #reject = {}
            response = {}
            
            if not module is None:
                # Load the file and handle licences (show/hide some options on the page) etc.
                #module.fetchResources(parent, request, response)

                # Handle the page request.
                tmp = module.handleRequest(parent, request, response)

                if isinstance(tmp, str): return tmp
                else: return json.dumps(tmp)
            
            else:
                return '{"' + KEY_ERROR + '": "Couldn\'t find module ' + request["name"] + '"}'
            
        except Exception as e:
            parent.logging.logDebug("Add error logging here in the dispatchRequest")
            parent.logging.logDebug(str(e))
            traceback.print_exc()
            return '{"' + KEY_ERROR + '": "An error occurred: ' + str(e) + '"}'
    
    elif request["type"] == TYPE_GET:
        # Some getSensors() etc. stuff here.
        # I don't know if it's really needed. TYPE_VIEW should be able to handle it all.
        print("Derp")
        
    return '{"' + KEY_ERROR + '": "Could not load page"}' # HOW ABOUT MAKING A STANDARD 404 PAGE INSTEAD? PROBABLY NOT SUITABLE FOR STUFF LIKE SENSOR REQUESTS.

def reloadIfNeeded(parent, name):
    tmp = time()
    modifyTime = path.getmtime("Controllers/" + name + ".py")
    modules = parent.configManager.getConf(CONFIG_FORMS).getItem("modules", "")

    for module in modules:
        if module["module"] == "Controllers." + name:
            # We don't know when the file was modified last time so initialize a value.
            if not "lastmodify" in module:
                module["lastmodify"] = 0

            # Dynamically reload the module because the file has been modified and we want the latest version.
            if module["lastmodify"] < modifyTime:
                parent.moduleManager.reloadModule("Controllers." + name)
                module["lastmodify"] = modifyTime
                parent.configManager.getConf(CONFIG_FORMS).setItem("modules", modules)
                parent.logging.logDebug("Reoading module " + "Controllers." + name + " took: " + str(time()-tmp))
                break