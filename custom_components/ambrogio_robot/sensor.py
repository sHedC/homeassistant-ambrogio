"""Sensor platform for Ambrogio Robot."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
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
        device_class=SensorDeviceClass.ENUM,
        translation_key="state",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Set up the sensor platform."""
    coordinator: AmbrogioDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            AmbrogioRobotSensor(
                coordinator=coordinator,
                entity_description=entity_description,
                robot_imei=robot_imei,
                robot_name=robot_name,
            )
            for robot_imei, robot_name in coordinator.robots.items()
            for entity_description in ENTITY_DESCRIPTIONS
        ],
        update_before_add=True,
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
    def icon(self) -> str:
        """Return the icon of the entity."""
        return ROBOT_STATES[self._state]["icon"]

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return ROBOT_STATES[self._state]["name"]
