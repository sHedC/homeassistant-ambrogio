"""BlueprintEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import (
    ATTRIBUTION,
    LOGGER,
    DOMAIN,
    NAME,
    VERSION,
    MANUFACTURER,
    CONF_ROBOT_IMEI,
)
from .coordinator import AmbrogioDataUpdateCoordinator


class AmbrogioRobotEntity(CoordinatorEntity):
    """Ambrogio Robot Entity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: AmbrogioDataUpdateCoordinator,
        robot_imei: str,
        robot_name: str,
        entity_type: str,
        entity_key: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._robot_imei = robot_imei
        self._robot_name = robot_name
        self._robot_serial = None
        self._robot_model = None

        self._attr_unique_id = slugify(f"{robot_name}_{entity_key}")
        self.entity_id = f"{entity_type}.{self._attr_unique_id}"
        
        self._state = 0
        self._available = True
        self._location = {
            "latitude": None,
            "longitude": None,
        }
        self.attrs: dict[str, Any] = {
            CONF_ROBOT_IMEI: self._robot_imei,
        }

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._robot_name

    @property
    def icon(self) -> str:
        """Return the icon of the entity."""
        return "mdi:robot-mower"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._attr_unique_id

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def device_info(self):
        """Return the device info."""

        return {
            "identifiers": {
                (DOMAIN, self._robot_imei)
            },
            "name": self._robot_name,
            "model": self._robot_model,
            "manufacturer": MANUFACTURER,
        }

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.attrs

    async def async_update(self) -> None:
        
        # TODO
        LOGGER.debug("async_update")
        LOGGER.debug(self._robot_name)
        
        self._update_handler();
    
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        
        # TODO
        LOGGER.debug("_handle_coordinator_update")
        LOGGER.debug(self._robot_name)
        
        self._update_handler();
        self.async_write_ha_state()
    
    def _update_handler(self):
        if self._robot_imei in self.coordinator.data["robots"]:
            robot = self.coordinator.data["robots"][self._robot_imei]
            self._state = robot["state"]
            self._available = (self._state > 0)
            self._location = robot["location"]
            self._robot_serial = robot["serial"]
            if len(self._robot_serial) > 0:
                self._robot_model = self._robot_serial[0:5]
