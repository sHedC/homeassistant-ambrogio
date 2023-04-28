"""BlueprintEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
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

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )
