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

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            model=VERSION,
            manufacturer=MANUFACTURER,
        )

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
            self._location = robot["location"]
