
class FormController:

    def handleRequest(parent, request, response):
        raise NotImplementedError("HandleRequest was not implemented by a class inheriting from FormController")

    def handleSubmit(parent, request, response):
        raise NotImplementedError("HandleSubmit was not implemented by a class inheriting from FormController")
    
    def verify(parent, request, reject):
        raise NotImplementedError("Verify was not implemented by a class inheriting from FormController")

    def successView(parent, messages, redirect, response):
        fadeout = parent.settingsManager.getByName("notificationfadeout")

        data = {}
        data["fadeout"] = fadeout["value"]
        if redirect: data["redirect"] = redirect
        data["success"] = []

        for message in messages:
            data["success"].append(message)
        print(data)
        return data

    def errorView(parent, messages, redirect, response):
        pass