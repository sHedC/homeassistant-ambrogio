"""Sensor platform for Ambrogio Robot."""
from __future__ import annotations

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.components.sensor import SensorEntityDescription
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
        key="location",
        name="Robot Location",
        icon="mdi:robot-mower",
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
        update_before_add=True
    )


class AmbrogioRobotDeviceTracker(AmbrogioRobotEntity, TrackerEntity):
    """Ambrogio Robot Device Tracker class."""

    def __init__(
        self,
        coordinator: AmbrogioDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
        robot_imei: str,
        robot_name: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator, robot_imei, robot_name, "device_tracker", entity_description.key
        )
        self.entity_description = entity_description

    @property
    def latitude(self) -> Optional[float]:
        """Return latitude value of the device."""
        location = self._location.get("latitude", None)
        return location if location else None

    @property
    def longitude(self) -> Optional[float]:
        """Return longitude value of the device."""
        location = self._location.get("longitude", None)
        return location if location else None

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def device_class(self):
        return None
