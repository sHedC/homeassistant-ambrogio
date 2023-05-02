"""BlueprintEntity class."""
from __future__ import annotations

from datetime import datetime
from homeassistant.const import (
    ATTR_NAME,
    ATTR_IDENTIFIERS,
    ATTR_LOCATION,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_STATE,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import (
    ATTRIBUTION,
    LOGGER,
    DOMAIN,
    MANUFACTURER,
    CONF_MOWERS,
    CONF_ROBOT_IMEI,
    ATTR_SERIAL,
    ATTR_CONNECTED,
    ATTR_LAST_COMM,
    ATTR_LAST_SEEN,
    ATTR_LAST_PULL,
    ROBOT_STATES,
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

        self._state = 0
        self._available = True
        self._location = {
            ATTR_LATITUDE: None,
            ATTR_LONGITUDE: None,
        }
        self._connected = False
        self._last_communication = None
        self._last_seen = None
        self._last_pull = None
        
        self.entity_id = f"{entity_type}.{self._attr_unique_id}"

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
            ATTR_IDENTIFIERS: {(DOMAIN, self._robot_imei)},
            ATTR_NAME: self._robot_name,
            ATTR_MODEL: self._robot_model,
            ATTR_MANUFACTURER: MANUFACTURER,
        }

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return Extra Attributes."""
        return {
            CONF_ROBOT_IMEI: self._robot_imei,
            ATTR_CONNECTED: self._connected,
            ATTR_LAST_COMM: self._last_communication,
            ATTR_LAST_SEEN: self._last_seen,
            ATTR_LAST_PULL: self._last_pull,
        }

    async def async_update(self) -> None:
        """Peform async_update."""
        self._update_handler()

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_handler()
        self.async_write_ha_state()

    def _update_handler(self):
        if self._robot_imei in self.coordinator.data[CONF_MOWERS]:
            robot = self.coordinator.data[CONF_MOWERS][self._robot_imei]
            self._state = robot[ATTR_STATE] if robot[ATTR_STATE] < len(ROBOT_STATES) else 0
            self._available = self._state > 0
            if robot[ATTR_LOCATION] is not None:
                    self._location = robot[ATTR_LOCATION]
            self._robot_serial = robot[ATTR_SERIAL]
            if (
                self._robot_serial is not None
                and len(self._robot_serial) > 4
            ):
                self._robot_model = self._robot_serial[0:5]

            self._connected = robot[ATTR_CONNECTED]
            self._last_communication = robot[ATTR_LAST_COMM]
            self._last_seen = robot[ATTR_LAST_SEEN]
            self._last_pull = datetime.now()
