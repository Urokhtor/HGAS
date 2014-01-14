from Constants import CONFIG_SETTINGS, CONFIG_CORE

class BaseManager:
    
    def __init__(self, parent):
        self.parent = parent
    
    def getNextId(self):
        currentId = self.parent.configManager.getConf(CONFIG_SETTINGS).getItem("idsequence", None)
        nextId = currentId + 1
        self.parent.configManager.getConf(CONFIG_SETTINGS).setItem("idsequence", nextId)
        return nextId
    
    def create(self):
        raise NotImplementedError("Create was not implemented by a class inheriting from BaseManager")

    def _getById(self, _item, id):
        """

        """

        items = self.parent.configManager.getConf(CONFIG_CORE).getItem(_item, None)

        if not id is None:
            for item in items:
                if item["id"] == id:
                    return item

        return None

    def _getByName(self, _item, name):
        """

        """

        items = self.parent.configManager.getConf(CONFIG_CORE).getItem(_item, None)

        if not name is None:
            for item in items:
                if item["name"] == name:
                    return item

        return None

    def _getAllFromField(self, _item, field):
        """
            Gets all values from given field.
        """

        items = self.parent.configManager.getConf(CONFIG_CORE).getItem(_item, None)
        list = []

        if not field is None:
            for item in items:
                if field in item:
                    list.append(item[field])

        return list

    def _has(self, _item, id):
        """

        """

        items = self.parent.configManager.getConf(CONFIG_CORE).getItem(_item, None)

        if items is None: return False

        for item in items:
            if item["id"] == id:
                return True

        return False

    def _hasByName(self, _item, name):
        items = self.parent.configManager.getConf(CONFIG_CORE).getItem(_item, None)

        for item in items:
            if item["name"] == name:
                return True

        return False
