"""Custom integration to integrate Ambrogio Robot with Home Assistant.

For more details about this integration, please refer to
https://github.com/sHedC/homeassistant-ambrogio
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    CONF_API_TOKEN,
    CONF_ACCESS_TOKEN,
    CONF_SCAN_INTERVAL,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AmbrogioRobotApiClient
from .const import CONF_MOWERS, DOMAIN
from .coordinator import AmbrogioDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator = AmbrogioDataUpdateCoordinator(
        hass=hass,
        robots=entry.options[CONF_MOWERS],
        client=AmbrogioRobotApiClient(
            api_key=entry.data[CONF_API_TOKEN],
            access_token=entry.data[CONF_ACCESS_TOKEN],
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
