"""Sensor platform for Ambrogio Robot."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    ATTR_LOCATION,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
)
from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
)
from .coordinator import AmbrogioDataUpdateCoordinator
from .entity import AmbrogioRobotEntity

ENTITY_DESCRIPTIONS = (
    EntityDescription(
        key="location",
        name="Robot Location",
        icon="mdi:robot-mower",
        translation_key="location",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Set up the sensor platform."""
    coordinator: AmbrogioDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            AmbrogioRobotDeviceTracker(
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


class AmbrogioRobotDeviceTracker(AmbrogioRobotEntity, TrackerEntity):
    """Ambrogio Robot Device Tracker class."""

    def __init__(
        self,
        coordinator: AmbrogioDataUpdateCoordinator,
        entity_description: EntityDescription,
        robot_imei: str,
        robot_name: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator=coordinator,
            robot_imei=robot_imei,
            robot_name=robot_name,
            entity_type="device_tracker",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        location = self._get_attribute(ATTR_LOCATION, {}).get(ATTR_LATITUDE, None)
        return location if location else None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        location = self._get_attribute(ATTR_LOCATION, {}).get(ATTR_LONGITUDE, None)
        return location if location else None

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def device_class(self):
        """Return Device Class."""
        return None
