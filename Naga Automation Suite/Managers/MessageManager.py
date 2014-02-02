__author__ = 'Urokhtor'

from Managers.BaseManager import BaseManager
from Constants import CONFIG_MESSAGES

class MessageManager(BaseManager):

    def __init__(self, parent):
        BaseManager.__init__(self, parent, CONFIG_MESSAGES, "messages")

    """
    def getAll(self):
        return self.parent.configManager.getConf(CONFIG_MESSAGES).items()

    def getByName(self, name):
        return self.parent.configManager.getConf(CONFIG_MESSAGES).getItem(name, name)

    def has(self, name):
        if not self.getByName(name) is None:
            return True

        return False
    """