"""Custom integration to integrate Ambrogio Robot with Home Assistant.

For more details about this integration, please refer to
https://github.com/sHedC/homeassistant-ambrogio
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_API_TOKEN,
    CONF_ACCESS_TOKEN,
    CONF_EMAIL,
    CONF_PASSWORD,
    Platform,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api_firebase import AmbrogioRobotFirebaseAPI, AmbrogioRobotException
from .const import (
    API_KEY,
    DOMAIN,
)
from .services import async_setup_services
from .api import AmbrogioRobotApiClient
from .coordinator import AmbrogioDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
    Platform.VACUUM,
]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up  ZCS Lawn Mower Robot component."""
    hass.data.setdefault(DOMAIN, {})

    await async_setup_services(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    # Get or update the list of robots from Firebase
    try:
        api_firebase = AmbrogioRobotFirebaseAPI(async_get_clientsession(hass))
        tokens = await api_firebase.verify_password(
            entry.data[CONF_EMAIL], entry.data[CONF_PASSWORD]
        )
        robots: dict = await api_firebase.get_robots(
            tokens[CONF_ACCESS_TOKEN], tokens[CONF_API_TOKEN]
        )
    except AmbrogioRobotException as exp:
        raise ConfigEntryAuthFailed from exp

    # Build the Robot List to hand over.
    robot_list: dict = {}
    for robot in robots.values():
        robot_list[robot["imei"]] = robot["name"]

    hass.data[DOMAIN][entry.entry_id] = coordinator = AmbrogioDataUpdateCoordinator(
        hass=hass,
        robots=robot_list,
        client=AmbrogioRobotApiClient(
            api_key=API_KEY,
            access_token=tokens[CONF_API_TOKEN],
            session=async_get_clientsession(hass),
        ),
    )
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
