"""Constants for Ambrogio Robot."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Ambrogio Robot"
DOMAIN = "ambrogio_robot"
VERSION = "0.0.0"
MANUFACTURER = "Zucchetti Centro Sistemi"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

API_TOKEN = "DJMYYngGNEit40vA"
API_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

CONF_CONFIRM = "confirm"
CONF_MOWERS = "mowers"
CONF_ROBOT_NAME = "robot_name"
CONF_ROBOT_IMEI = "robot_imei"
CONF_SELECTED_ROBOT = "selected_robot"

ATTR_SERIAL = "serial"
ATTR_CONNECTED = "connected"
ATTR_LAST_COMM = "last_communication"
ATTR_LAST_SEEN = "last_seen"
ATTR_LAST_PULL = "last_pull"

ROBOT_STATES = [
    {
        "name" : "unknown",
        "icon" : "mdi:crosshairs-question",
    },
    {
        "name" : "charging",
        "icon" : "mdi:battery-charging",
    },
    {
        "name" : "working",
        "icon" : "mdi:state-machine",
    },
    {
        "name" : "stop",
        "icon" : "mdi:stop-circle",
    },
    {
        "name" : "error",
        "icon" : "mdi:alert-circle",
    },
    {
        "name" : "nosignal",
        "icon" : "mdi:signal-off",
    },
    {
        "name" : "gotostation",
        "icon" : "mdi:ev-station",
    },
    {
        "name" : "gotoarea",
        "icon" : "mdi:grass",
    },
    {
        "name" : "bordercut",
        "icon" : "mdi:scissors-cutting",
    },
    # few robots has unknown state 9
    {
        "name" : "unknown",
        "icon" : "mdi:crosshairs-question",
    },
]
