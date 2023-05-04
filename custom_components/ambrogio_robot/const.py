"""Constants for Ambrogio Robot."""
from logging import Logger, getLogger

import voluptuous as vol
from homeassistant.const import (
    ATTR_DEVICE_ID,
)
from homeassistant.helpers import config_validation as cv

LOGGER: Logger = getLogger(__package__)

NAME = "Ambrogio Robot"
DOMAIN = "ambrogio_robot"
VERSION = "0.0.0"
MANUFACTURER = "Zucchetti Centro Sistemi"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

API_TOKEN = "DJMYYngGNEit40vA"
API_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
API_ACK_TIMEOUT = 30

CONF_CONFIRM = "confirm"
CONF_MOWERS = "mowers"
CONF_ROBOT_NAME = "robot_name"
CONF_ROBOT_IMEI = "robot_imei"
CONF_SELECTED_ROBOT = "selected_robot"

ATTR_SERIAL = "serial"
ATTR_MESSAGE = "message"
ATTR_CONNECTED = "connected"
ATTR_LAST_COMM = "last_communication"
ATTR_LAST_SEEN = "last_seen"
ATTR_LAST_PULL = "last_pull"

SERVICE_SET_PROFILE = "set_profile"
SERVICE_SET_PROFILE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("profile"): vol.All(vol.Coerce(int), vol.Range(min=1, max=3)),
    }
)
SERVICE_WORK_UNTIL = "work_until"
SERVICE_WORK_UNTIL_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("area"): vol.All(vol.Coerce(int), vol.Range(min=1, max=8)),
        vol.Required("hours"): vol.All(vol.Coerce(int), vol.Range(min=0, max=24)),
        vol.Required("minutes"): vol.All(vol.Coerce(int), vol.Range(min=0, max=60)),
    }
)
SERVICE_BORDER_CUT = "border_cut"
SERVICE_BORDER_CUT_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)
SERVICE_CHARGE_UNTIL = "charge_until"
SERVICE_CHARGE_UNTIL_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("hours"): vol.All(vol.Coerce(int), vol.Range(min=0, max=24)),
        vol.Required("minutes"): vol.All(vol.Coerce(int), vol.Range(min=0, max=60)),
        vol.Required("weekday"): vol.All(vol.Coerce(int), vol.Range(min=0, max=6)),
    }
)
SERVICE_TRACE_POSITION = "trace_position"
SERVICE_TRACE_POSITION_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)

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
