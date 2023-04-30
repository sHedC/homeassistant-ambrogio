"""Sensor platform for Ambrogio Robot."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    LOGGER,
    DOMAIN,
    ROBOT_STATES,
)
from .coordinator import AmbrogioDataUpdateCoordinator
from .entity import AmbrogioRobotEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="state",
        name="Robot State",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Set up the sensor platform."""
    coordinator: AmbrogioDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        AmbrogioRobotSensor(
            coordinator=coordinator,
            entity_description=entity_description,
            robot_imei=robot_imei,
            robot_name=robot_name,
        )
        for robot_imei, robot_name in coordinator.robots.items()
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AmbrogioRobotSensor(AmbrogioRobotEntity, SensorEntity):
    """Ambrogio Robot Sensor class."""

    def __init__(
        self,
        coordinator: AmbrogioDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
        robot_imei: str,
        robot_name: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator, robot_imei, robot_name, "sensor", entity_description.key
        )
        self.entity_description = entity_description

    @property
    def state(self) -> str | None:
        return ROBOT_STATES[self._state]["name"]
    
    @property
    def icon(self) -> str:
        """Return the icon of the entity."""
        return ROBOT_STATES[self._state]["icon"]
    
    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return ROBOT_STATES[0]["name"]
