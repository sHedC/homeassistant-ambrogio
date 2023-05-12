"""Constants for Ambrogio Robot."""
from logging import Logger, getLogger

import voluptuous as vol
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_LOCATION,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS,
)
from homeassistant.helpers import config_validation as cv

LOGGER: Logger = getLogger(__package__)

NAME = "Ambrogio Robot"
DOMAIN = "ambrogio_robot"
VERSION = "0.0.0"
MANUFACTURER = "Zucchetti Centro Sistemi"
ATTRIBUTION = "Data provided gently by Telit IoT Platform"

API_TOKEN = "DJMYYngGNEit40vA"
API_DATETIME_FORMAT_DEFAULT = "%Y-%m-%dT%H:%M:%S.%f%z"
API_DATETIME_FORMAT_FALLBACK = "%Y-%m-%dT%H:%M:%S%z"
API_ACK_TIMEOUT = 30

UPDATE_INTERVAL_DEFAULT = 300
UPDATE_INTERVAL_WORKING = 60

CONF_CONFIRM = "confirm"
CONF_MOWERS = "mowers"
CONF_ROBOT_NAME = "robot_name"
CONF_ROBOT_IMEI = "robot_imei"
CONF_SELECTED_ROBOT = "selected_robot"

ATTR_SERIAL = "serial"
ATTR_WORKING = "working"
ATTR_ERROR = "error"
ATTR_CONNECTED = "connected"
ATTR_LAST_COMM = "last_communication"
ATTR_LAST_SEEN = "last_seen"
ATTR_LAST_PULL = "last_pull"
ATTR_LAST_STATE = "last_state"
ATTR_LAST_WAKE_UP = "last_wake_up"

SERVICE_SET_PROFILE = "set_profile"
SERVICE_SET_PROFILE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("profile"): vol.All(vol.Coerce(int), vol.Range(min=1, max=3)),
    }
)
SERVICE_WORK_NOW = "work_now"
SERVICE_WORK_NOW_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)
SERVICE_WORK_FOR = "work_for"
SERVICE_WORK_FOR_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("duration"): vol.All(vol.Coerce(int), vol.Range(min=1, max=1439)),
        vol.Optional("area"): vol.All(vol.Coerce(int), vol.Range(min=1, max=10)),
    }
)
SERVICE_WORK_UNTIL = "work_until"
SERVICE_WORK_UNTIL_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("hours"): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
        vol.Required("minutes"): vol.All(vol.Coerce(int), vol.Range(min=0, max=59)),
        vol.Optional("area"): vol.All(vol.Coerce(int), vol.Range(min=1, max=10)),
    }
)
SERVICE_BORDER_CUT = "border_cut"
SERVICE_BORDER_CUT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)
SERVICE_CHARGE_NOW = "charge_now"
SERVICE_CHARGE_NOW_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)
SERVICE_CHARGE_FOR = "charge_for"
SERVICE_CHARGE_FOR_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("duration"): vol.All(vol.Coerce(int), vol.Range(min=1, max=1439)),
    }
)
SERVICE_CHARGE_UNTIL = "charge_until"
SERVICE_CHARGE_UNTIL_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required("hours"): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
        vol.Required("minutes"): vol.All(vol.Coerce(int), vol.Range(min=0, max=59)),
        vol.Required("weekday"): vol.All(vol.Coerce(int), vol.Range(min=1, max=7)),
    }
)
SERVICE_TRACE_POSITION = "trace_position"
SERVICE_TRACE_POSITION_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
    }
)
SERVICE_KEEP_OUT = "keep_out"
SERVICE_KEEP_OUT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.entity_ids_or_uuids,
        vol.Required(CONF_LOCATION): vol.Schema(
            {
                vol.Required(CONF_LATITUDE): float,
                vol.Required(CONF_LONGITUDE): float,
                vol.Optional(CONF_RADIUS): int,
            }
        ),
        vol.Optional("hours"): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
        vol.Optional("minutes"): vol.All(vol.Coerce(int), vol.Range(min=0, max=59)),
        vol.Optional("index"): vol.Coerce(int),
    }
)

ROBOT_MODELS = {
    "AM015D": "Fifteen Deluxe", # ?
    "AM020D": "Twenty Deluxe", # ?
    "AM020L": "Twenty Elite",
    "AM020P": "Twenty Elite S+", # ?
    "AM020R": "Twenty ZR", # ?
    "AM025D": "Twenty 25 Deluxe", # ?
    "AM025L": "Twenty 25 Elite", # ?
    "AM029D": "Twenty 29 Deluxe", # ?
    "AM029L": "Twenty 29 Elite", # ?
    "AM032D": "L32 Deluxe", # ?
    "AM035B": "L35 Basic",
    "AM035D": "L35 Deluxe",
    "AM040B": "4.0 Basic", # ???
    "AM040L": "4.0 Elite", # ???
    "AM043L": "4.36 Elite",
    "AM060L": "L60 Elite", # ?
    "AM060P": "L60 Elite S+", # ?
    "AM085L": "L85 Elite", # ?
    "AM095L": "Quad Elite 4WD",
    "AM250D": "L250 Deluxe", # ?
    "AM250L": "L250i Elite",
    "AM250P": "L250i Elite S+",# ?
    "AM350L": "L350i Elite", # ?
    "AM400B": "L400i Basic", # ?
    "AM400D": "L400i Deluxe", # ?
    "AM400L": "L400 Elite", # ?
    #"AM450B": "", # DB:21
    #"AM450D": "", # DB:99
}

ROBOT_STATES = [
    {
        "name" : "unknown",
        "icon" : "mdi:crosshairs-question",
        "color": "#000000",
    },
    {
        "name" : "charge",
        "icon" : "mdi:battery-charging",
        "color": "#CCCC00",
    },
    {
        "name" : "work",
        "icon" : "mdi:state-machine",
        "color": "#007700",
    },
    {
        "name" : "pause",
        "icon" : "mdi:pause",
        "color": "#0000FF",
    },
    {
        "name" : "fail",
        "icon" : "mdi:alert-circle",
        "color": "#FF0000",
    },
    {
        "name" : "nosignal",
        "icon" : "mdi:signal-off",
        "color": "#FF7700",
    },
    {
        "name" : "gotostation",
        "icon" : "mdi:ev-station",
        "color": "#FFFF00",
    },
    {
        "name" : "gotoarea",
        "icon" : "mdi:grass",
        "color": "#00FF00",
    },
    {
        "name" : "bordercut",
        "icon" : "mdi:scissors-cutting",
        "color": "#00CC00",
    },
    {
        "name" : "expired",
        "icon" : "mdi:clock-alert",
        "color": "#000000",
    },
    {
        "name" : "renewed",
        "icon" : "mdi:clock-check",
        "color": "#00B5B5",
    },
    {
        "name" : "work_standby",
        "icon" : "mdi:power-standby",
        "color": "#E61EDC",
    },
]
ROBOT_WORKING_STATES = [2, 6, 7, 8, 11]
ROBOT_WAKE_UP_INTERVAL = 300

ROBOT_ERRORS = {
    0: "bus_error",
    1: "sync_error",
    2: "blackout_sig02",
    3: "blackout_sig03",
    4: "blackout_sig04",
    5: "blocked",
    6: "bump_error",
    7: "bump_error_bump03",
    8: "grass_too_high",
    9: "out_of_border_block",
    10: "out_of_border_bord01",
    11: "out_of_border_bord02",
    12: "out_of_border_bord03",
    13: "out_of_border_bump01",
    14: "out_of_border_bump02",
    15: "out_of_border_out01",
    16: "out_of_border_out02",
    17: "out_of_border_start",
    18: "out_of_border_sync01",
    19: "out_of_border_sync02",
    20: "tilt",
    21: "blade_error",
    22: "blade_error_tmotor",
    23: "blade_error_tdrv",
    24: "blade_error_curr",
    25: "blade_error_rpm",
    26: "blade_error_wdog",
    27: "blade_error_fail",
    28: "wheel_error_left",
    29: "wheel_error_left_tmotor",
    30: "wheel_error_left_tdrv",
    31: "wheel_error_left_curr",
    32: "wheel_error_left_rpm",
    33: "wheel_error_left_wdog",
    34: "wheel_error_left_fail",
    35: "wheel_error_right",
    36: "wheel_error_right_tmotor",
    37: "wheel_error_right_tdrv",
    38: "wheel_error_right_curr",
    39: "wheel_error_right_rpm",
    40: "wheel_error_right_wdog",
    41: "wheel_error_right_fail",
    42: "out_of_border_out03",
    43: "rollover",
    44: "lift",
    45: "lift_lift2",
    46: "lift_lift3",
    47: "lift_lift4",
    48: "tilt_tilt3",
    49: "tilt_tilt4",
    50: "out_of_border_bump04",
    51: "low_battery",
    52: "power_off",
    53: "no_signal",
    54: "out_of_border_out04",
    55: "signal_returned",
    56: "autocheck_start",
    57: "autocheck_stop",
    58: "out_of_border_nosig",
    59: "no_signal_c1",
    60: "no_signal_c2",
    61: "no_signal_c2_1",
    62: "no_signal_c1_1",
    63: "out_of_border_bord04",
    64: "emergency_stop",
    65: "display_required",
    66: "receiver_required",
    67: "gsm_required",
    68: "driver_l_required",
    69: "driver_r_required",
    70: "driver_b_required",
    71: "magnet_required",
    72: "blocked_block1",
    73: "blocked_block3",
    79: "compass_required",
    80: "bump_error_front",
    81: "bump_error_back",
    82: "date_error",
    84: "program_error",
    85: "version_error",
    90: "safety_lift_sensor_damaged_or_dirty",
    91: "recharge_error",
    92: "autocheck_gyro",
    93: "autocheck_fail",
    94: "autocheck_rain",
    95: "autocheck_coils",
    96: "autocheck_motion",
    97: "autocheck_wheels_blocked",
    98: "autocheck_wheels_error",
    99: "autocheck_recharge",
    100: "autocheck_button_wrong",
    101: "autocheck_button_not_released",
    102: "autocheck_not_lifted",
    103: "display_error",
    104: "blade_error_blocked",
    105: "wheel_error_left_blocked",
    106: "wheel_error_right_blocked",
    107: "blade_error_left",
    108: "blade_error_left_tmotor",
    109: "blade_error_left_tdrv",
    110: "blade_error_left_curr",
    111: "blade_error_left_rpm",
    112: "blade_error_left_wdog",
    113: "blade_error_left_fail",
    114: "blade_error_left_blocked",
    115: "blade_error_right",
    116: "blade_error_right_tmotor",
    117: "blade_error_right_tdrv",
    118: "blade_error_right_curr",
    119: "blade_error_right_rpm",
    120: "blade_error_right_wdog",
    121: "blade_error_right_fail",
    122: "blade_error_right_blocked",
    123: "wheel_error_fl",
    124: "wheel_error_fl_tmotor",
    125: "wheel_error_fl_tdrv",
    126: "wheel_error_fl_curr",
    127: "wheel_error_fl_rpm",
    128: "wheel_error_fl_wdog",
    129: "wheel_error_fl_fail",
    130: "wheel_error_fl_blocked",
    131: "wheel_error_fr",
    132: "wheel_error_fr_tmotor",
    133: "wheel_error_fr_tdrv",
    134: "wheel_error_fr_curr",
    135: "wheel_error_fr_rpm",
    136: "wheel_error_fr_wdog",
    137: "wheel_error_fr_fail",
    138: "wheel_error_fr_blocked",
    139: "steer_error_fl",
    140: "steer_error_fl_tmotor",
    141: "steer_error_fl_tdrv",
    142: "steer_error_fl_curr",
    143: "steer_error_fl_rpm",
    144: "steer_error_fl_wdog",
    145: "steer_error_fl_fail",
    146: "steer_error_fl_blocked",
    147: "steer_error_fr",
    148: "steer_error_fr_tmotor",
    149: "steer_error_fr_tdrv",
    150: "steer_error_fr_curr",
    151: "steer_error_fr_rpm",
    152: "steer_error_fr_wdog",
    153: "steer_error_fr_fail",
    154: "steer_error_fr_blocked",
    155: "steer_error_bl",
    156: "steer_error_bl_tmotor",
    157: "steer_error_bl_tdrv",
    158: "steer_error_bl_curr",
    159: "steer_error_bl_rpm",
    160: "steer_error_bl_wdog",
    161: "steer_error_bl_fail",
    162: "steer_error_bl_blocked",
    163: "steer_error_br",
    164: "steer_error_br_tmotor",
    165: "steer_error_br_tdrv",
    166: "steer_error_br_curr",
    167: "steer_error_br_rpm",
    168: "steer_error_br_wdog",
    169: "steer_error_br_fail",
    170: "steer_error_br_blocked",
    171: "radar_error",
    256: "board_error",
    257: "config_error",
    258: "test_b_required",
    259: "test_c_required",
    260: "trapped",
    1000: "sd_card_error",
    1001: "tilt_communication_error",
    1002: "rtc_error",
    1003: "can_0_error",
    1004: "can_1_error",
    1005: "blade_motor_communication_error",
    1006: "wheel_left_communication_error",
    1007: "wheel_right_communication_error",
    1008: "receiver_left_communication_error",
    1009: "connect_error",
    1010: "blade_height_error",
    1011: "bluetooth_error",
    1012: "geofence_error",
    1013: "gps_error",
    1014: "connect_error_1",
    1015: "over_current_error",
    1016: "over_voltage_error",
    1017: "eeprom_error",
    1018: "tilt_left_disconnect",
    1019: "tilt_right_disconnect",
    1020: "receiver_left_disconnect",
    1021: "receiver_right_disconnect",
    1022: "inductive_module_error",
    1023: "inductive_module_error_1",
    1024: "inductive_module_error_2",
    1025: "connect_module_error",
    1026: "middle_blade_driver_disconnected",
    1027: "blade_left_driver_disconnected",
    1028: "blade_right_driver_disconnected",
    1029: "display_communication_error",
    1030: "low_battery_while_charging",
    1031: "blade_height_left",
    1032: "blade_height_right",
    1033: "device_error_devicex_require",
    1042: "long_disconnection_middle_blade",
    1043: "long_disconnection_blade_left",
    1044: "long_disconnection_blade_right",
    1045: "battery_not_detected",
    1046: "zdefender_error",
    1047: "radar_data_save_error",
    1049: "docking_error",
    2000: "invalid_voucher",
    2001: "used_voucher",
    2002: "voucher_zone_error",
    2003: "server_connection_error",
    3001: "mismatch_wheel_motors",
    3002: "mismatch_back_coils",
    3003: "mismatch_left_coils",
    3004: "mismatch_right_coils",
    3005: "mismatch_front_coils",
    3006: "wrong_measurament_back_left_coil",
    3007: "wrong_measurament_back_right_coil",
    3008: "wrong_measurament_left_left_coil",
    3009: "wrong_measurament_left_right_coil",
    3010: "wrong_measurament_right_left_coil",
    3011: "wrong_measurament_right_right_coil",
    3012: "wrong_measurament_front_left_coil",
    3013: "wrong_measurament_front_right_coil",
    3014: "mismatch_bump",
    3015: "bump_sensor_blocked",
    3016: "lift_error",
    3017: "mismatch_lift_sensors",
    3018: "rain_error",
    3019: "stop_button_blocked",
    3020: "no_signal_back_receiver",
    3021: "no_signal_receiver_left",
    3022: "no_signal_receiver_right",
    3023: "no_signal_front_receiver",
    3033: "wrong_or_missing_action",
    4000: "trapped_no_grass",
    4001: "trapped_drop_off",
    4002: "trapped_bump",
    4003: "trapped_tilt",
    5000: "unexpected_shutdown_error",
    5001: "unexpected_shutdown_resume_from_failure",
    5002: "unexpected_shutdown_autocheck",
    5003: "unexpected_shutdown_charge",
    5004: "unexpected_shutdown_work",
    5005: "unexpected_shutdown_work_pause",
    5006: "unexpected_shutdown_done",
    5008: "unexpected_shutdown_error",
}
