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

PLOT_DAY = 86400
PLOT_WEEK = 604800

MAX_MESSAGE_LENGTH = 255

# Arduino response codes.
NO_COMMAND_ERROR = 1
NO_INDEX_ERROR = 2
NO_DEVICE_ERROR = 3
NO_TYPE_ERROR = 4
WRONG_TYPE_ERROR = 5
UNRECOGNISED_COMMAND_ERROR = 6
MESSAGE_TOO_LONG_ERROR = 7
COULD_NOT_ADD_SENSOR_ERROR = 8
COULD_NOT_ADD_DEVICE_ERROR = 9
COULD_NOT_REMOVE_SENSOR_ERROR = 10
COULD_NOT_REMOVE_DEVICE_ERROR = 11

SENSOR_EXISTS_ERROR = 50
PUMP_EXISTS_ERROR = 51
SENSOR_DOESNT_EXIST_ERROR = 52
PUMP_DOESNT_EXIST_ERROR = 53

NO_ARDUINO_RESPONSE = 6

INSERT_SENSOR_SUCCESS = 100
INSERT_PUMP_SUCCESS = 101
READ_SENSOR_SUCCESS = 102
RUN_DEVICE_SUCCESS = 103
REMOVE_SENSOR_SUCCESS = 104
REMOVE_PUMP_SUCCESS = 105
NO_ACTION_NEEDED = 106
READ_FREEMEMORY_SUCCESS = 107
TOGGLED_DEVICE_ON = 108
TOGGLED_DEVICE_OFF = 109

SEND_READ = 200
SEND_WRITE = 201
SEND_INSERT = 202
SEND_MODIFY = 203
SEND_ENABLE = 204
SEND_DISABLE = 205
SEND_REMOVE = 206
SEND_FREEMEMORY = 207

TYPE_SENSOR = 300
TYPE_PUMP = 301

FORM_ADD = 400
FORM_MODIFY = 401
FORM_REMOVE = 402

# Sensor types
SENSOR_TYPE_DEFAULT = 0
SENSOR_TYPE_TEMPERATURE = 1
SENSOR_TYPE_DHT11 = 2
SENSOR_TYPE_SR04 = 3
BMP085_TEMPERATURE = 4
BMP085_PRESSURE = 5
BMP085_ALTITUDE = 6

# Device types
DEVICE_TYPE_LIGHTS = 0
DEVICE_TYPE_PUMP = 1

# Device states
DEVICE_STATE_ON = 1
DEVICE_STATE_OFF = 0

KEY_COMMAND = "command"
KEY_DEVICE = "unit"
KEY_DEVICE_TYPE = "typedevice"
KEY_IS_STARTUP = "startup"
KEY_INDEX = "index"
KEY_HIGH_THRESHOLD = "high"
KEY_LOW_THRESHOLD = "low"
KEY_TYPE = "type"
KEY_MAX_ON_TIME = "max"
KEY_HYGROMETER_INDEX = "hygrometer"
KEY_USES_HYGROMETER = "uses"
KEY_ERROR = "error"
KEY_READING = "reading"
KEY_RESPONSE = "response"
KEY_STATE = "state"
KEY_ID = "id"
KEY_REJECT = "reject"

TYPE_FORM = "form"
TYPE_GET = "get"

CONFIG_SETTINGS = "settings"
CONFIG_FORMS = "forms"
CONFIG_CORE = "core"
CONFIG_ROOT = "Conf/"
