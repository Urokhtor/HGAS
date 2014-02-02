__author__ = 'Urokhtor'

from Managers.BaseManager import BaseManager
from Constants import *

class ClientManager(BaseManager):

    def __init__(self, parent):
        BaseManager.__init__(self, parent, CONFIG_CORE, "clients")

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
        self.add(client)
        return '{"' + KEY_RESPONSE + '": ' + str(INSERT_CLIENT_SUCCESS) + '}'

    def remove(self, client):
        if not self.has(client["id"]):
            return '{"' + KEY_ERROR + '": ' + str(CLIENT_DOESNT_EXIST_ERROR) + '}'

        clients = self.getAll()
        clients.remove(client)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("clients", clients)

        return '{"' + KEY_RESPONSE + '": ' + str(REMOVE_CLIENT_SUCCESS) + '}'