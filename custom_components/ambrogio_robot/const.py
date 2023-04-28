"""Constants for Ambrogio Robot."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Ambrogio Robot"
DOMAIN = "ambrogio_robot"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

API_TOKEN = "DJMYYngGNEit40vA"

CONF_CONFIRM = "confirm"
CONF_MOWERS = "mowers"
CONF_ROBOT_NAME = "robot_name"
CONF_ROBOT_IMEI = "robot_imei"
CONF_SELECTED_ROBOT = "selected_robot"
