"""Sensor platform for Ambrogio Robot."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    ROBOT_ERRORS,
)
from .coordinator import AmbrogioDataUpdateCoordinator
from .entity import AmbrogioRobotEntity

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="error",
        translation_key="error",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Set up the sensor platform."""
    coordinator: AmbrogioDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            AmbrogioRobotBinarySensor(
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


class AmbrogioRobotBinarySensor(AmbrogioRobotEntity, BinarySensorEntity):
    """Ambrogio Robot Sensor class."""

    def __init__(
        self,
        coordinator: AmbrogioDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
        robot_imei: str,
        robot_name: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator=coordinator,
            robot_imei=robot_imei,
            robot_name=robot_name,
            entity_type="binary_sensor",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description

    def update_extra_state_attributes(self) -> None:
        """Update extra attributes."""
        if self._state == 4:
            self._additional_extra_state_attributes = {
                "reason": ROBOT_ERRORS.get(self._error, "unknown"),
            }

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self._state == 4
