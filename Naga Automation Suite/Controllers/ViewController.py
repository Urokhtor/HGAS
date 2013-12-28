import json
from Constants import KEY_ERROR

class ViewController:

    def handleRequest(parent, request, response):
        raise NotImplementedError("HandleRequest was not implemented by a class inheriting from ViewController")

    def fetchResources(parent, request, response):
        """
            Reload the JSON page description and preprocess it.
        """

        if request["name"] is None:
            return '{"' + KEY_ERROR + '": "No controller was defined"}'

        #  This is not really THAT safe, perhas it needs to be changed in the future. For time being it's OK.
        f = open("Conf/Website/" + request["name"].split("Controller")[0].lower() + ".json", "r")
        tmp = json.load(f)
        f.close()

        # Now check for licences and stuff.
        ViewController.recursivelyCheckLicences(parent, tmp)
        response["file"] = tmp

    def recursivelyCheckLicences(parent, file):
        for object in file:
            # See if object contains some licences we need to check.
            # After that if the object contains childs, call them recursively.
            continue
