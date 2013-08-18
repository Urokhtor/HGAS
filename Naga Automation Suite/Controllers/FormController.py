
class FormController:
    
    def handleSubmit(parent, request, response):
        raise NotImplementedError("HandleSubmit was not implemented by a class inheriting from FormController")
    
    def verify(parent, request, reject):
        raise NotImplementedError("Verify was not implemented by a class inheriting from FormController")
    