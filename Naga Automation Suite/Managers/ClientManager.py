from Managers.BaseManager import BaseManager
from Constants import CONFIG_CORE

class ClientManager(BaseManager):

    def create(self, name, type, ip):
        """

        """

        client = {}
        client["name"] = name
        client["type"] = type
        client["ip"] = ip
        client["id"] = self.getNextId()

        return client

    def insert(self, client):
        clients = self.parent.configManager.getConf(CONFIG_CORE).getItem("clients", None)
        clients.append(client)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("clients", clients)

        # RETURN RESPONSE

    def getById(self, id):
        """

        """

        return self._getById("clients", id)

    def getByName(self, name):
        """

        """

        return self._getByName("clients", name)

    def has(self, id):
        """

        """

        return self._has("clients", id)

    def hasByName(self, name):
        """

        """

        return self._hasByName("clients", name)
