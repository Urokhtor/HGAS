from Constants import CONFIG_SETTINGS, CONFIG_CORE

class BaseManager:
    
    def __init__(self, parent, conf, item):
        self.parent = parent
        self.conf = conf
        self.item = item
    
    def getNextId(self):
        currentId = self.parent.settingsManager.getByName("idsequence")
        nextId = currentId["value"] + 1
        currentId["value"] = nextId
        self.parent.settingsManager.setByName("idsequence", nextId)
        return nextId
    
    def create(self, *args):
        raise NotImplementedError("Create was not implemented by a class inheriting from BaseManager")

    def getAll(self):
        """

        """

        return self.parent.configManager.getConf(self.conf).getItem(self.item, None)

    def getById(self, id):
        """

        """

        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)

        if not id is None:
            for item in items:
                if item["id"] == id:
                    return item

        return None

    def getByName(self, name):
        """

        """

        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)

        if not name is None:
            for item in items:
                if item["name"] == name:
                    return item

        return None

    def getAllFromField(self, field):
        """
            Gets all values from given field.
        """

        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)
        list = []

        if not field is None:
            for item in items:
                if field in item:
                    list.append(item[field])

        return list

    def getIdNameMap(self):
        """
            Returns a tuple mapping of id and name.
        """

        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)
        list = []

        for item in items:
            if "name" in item and "id" in item:
                list.append((item["id"], item["name"]))

        return list

    def add(self, item):
        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)

        if items is None: return False

        items.append(item)
        self.parent.configManager.getConf(self.conf).setItem(self.item, items)
        return True

    def set(self, item):
        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)

        if items is None: return False

        for _item in items:
            if _item["id"] == item["id"]:
                _item = item
                self.parent.configManager.getConf(self.conf).setItem(self.item, items)
                return True

        return False

    def has(self, id):
        """

        """

        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)

        if items is None: return False

        for item in items:
            if item["id"] == id:
                return True

        return False

    def hasByName(self, name):
        items = self.parent.configManager.getConf(self.conf).getItem(self.item, None)

        for item in items:
            if item["name"] == name:
                return True

        return False

    def equals(self, name, value):
        """
            Takes name of the item and the wanted value and checks if the item's current value matches with the
            wanted value.
        """

        if self.hasByName(name):
            if self.getByName(name) == value:
                return True

        return False

    def remove(self, item):
        raise NotImplementedError("Remove was not implemented by a class inheriting from BaseManager")

    def removeById(self, id):
        return self.remove(self.getById(id))