"""Constants for Ambrogio Robot."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Ambrogio Robot"
DOMAIN = "ambrogio_robot"
VERSION = "0.0.0"
MANUFACTURER = "Zucchetti Centro Sistemi"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

API_TOKEN = "DJMYYngGNEit40vA"

CONF_CONFIRM = "confirm"
CONF_MOWERS = "mowers"
CONF_ROBOT_NAME = "robot_name"
CONF_ROBOT_IMEI = "robot_imei"
CONF_SELECTED_ROBOT = "selected_robot"

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
]
