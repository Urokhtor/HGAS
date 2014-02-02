__author__ = 'Urokhtor'

from Managers.BaseManager import BaseManager
from Constants import *
from time import time

class SensorManager(BaseManager):

    def __init__(self, parent):
        BaseManager.__init__(self, parent, CONFIG_CORE, "sensors")

    def getReading(self, id):
        sensor = self.getById(id)

        if sensor is None: return # TODO: LOG THIS

        response = self.parent.connection.send(self.parent.protocol.readSensor(sensor))

        if KEY_ERROR in response:
            # TODO: LOG ERROR
            return

        # TODO: How to handle different protocols?
        reading = None

        # TODO: LOG RESULT

        self.updateSensorReading(id, reading)

    def updateSensorReading(self, id, reading):
        sensor = self.getById(id)

        if sensor is None:
            return False

        sensor["lastreading"] = reading
        sensor["lastupdated"] = int(time()) # Unix time.

        if sensor["alltimemax"] < reading:
            sensor["alltimemax"] = reading

        elif sensor["alltimemin"] > reading:
            sensor["alltimemin"] = reading

        self.set(sensor)
        #sensors = self.parent.configManager.getConf(CONFIG_CORE).getItem("sensors", None)
        #self.parent.configManager.getConf(CONFIG_CORE).setItem("sensors", sensors)
        return True

    def create(self, name, type, clientid, index):
        """
            Creates a new sensor object with the parameters supplied and assigns a new unique ID to it
            and then returns it. Use DeviceManager.insertSensor(sensor) to add the newly created sensor
            to the list.
        """

        sensor = {}
        sensor["name"] = name
        sensor["type"] = type
        sensor["index"] = index
        sensor["clientid"] = clientid
        sensor["telldusid"] = None
        sensor["lastreading"] = 0
        sensor["lastupdated"] = 0
        sensor["alltimemax"] = 0
        sensor["alltimemin"] = 0
        sensor["id"] = self.getNextId()

        return sensor

    def insert(self, sensor, isStartup = False):
        if self.has(sensor["id"] and not isStartup):
            return '{"' + KEY_ERROR + '": ' + str(SENSOR_EXISTS_ERROR) + '}'

        response = self.parent.connection.send(self.parent.protocol.insert(sensor, TYPE_SENSOR, isStartup))

        if KEY_ERROR in response: return response

        if response[KEY_RESPONSE] == INSERT_SENSOR_SUCCESS and not isStartup:
            self.add(sensor)

        return response

    def remove(self, sensor):
        if not self.has(sensor["id"]):
            return '{"' + KEY_ERROR + '": ' + str(SENSOR_DOESNT_EXIST_ERROR) + '}'

        response = self.parent.connection.send(self.parent.protocol.remove(sensor, TYPE_SENSOR))

        if KEY_ERROR in response: return response

        sensors = self.getAll()
        sensors.remove(sensor)
        self.parent.configManager.getConf(CONFIG_CORE).setItem("sensors", sensors)
        return response

    def removeById(self, id):
        return self.remove(self.getById(id))