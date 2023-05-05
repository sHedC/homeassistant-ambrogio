"""Sensor platform for Ambrogio Robot."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.vacuum import (
    ATTR_STATUS,
    STATE_CLEANING,
    STATE_DOCKED,
    STATE_PAUSED,
    STATE_IDLE,
    STATE_RETURNING,
    STATE_ERROR,
    StateVacuumEntity,
    VacuumEntityDescription,
    VacuumEntityFeature,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    LOGGER,
    DOMAIN,
    ROBOT_STATES,
    ROBOT_ERRORS,
)
from .coordinator import AmbrogioDataUpdateCoordinator
from .entity import AmbrogioRobotEntity

ROBOT_SUPPORTED_FEATURES = (
    VacuumEntityFeature.STOP
    | VacuumEntityFeature.RETURN_HOME
    | VacuumEntityFeature.SEND_COMMAND
    | VacuumEntityFeature.LOCATE
    | VacuumEntityFeature.STATE
    | VacuumEntityFeature.STATUS
    | VacuumEntityFeature.START
)
ENTITY_DESCRIPTIONS = (
    VacuumEntityDescription(
        key="",
        icon="mdi:robot-mower",
        translation_key="mower",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_devices: AddEntitiesCallback
):
    """Set up the sensor platform."""
    coordinator: AmbrogioDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            AmbrogioRobotVacuum(
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


class AmbrogioRobotVacuum(AmbrogioRobotEntity, StateVacuumEntity):
    """Ambrogio Robot Vacuum class."""

    def __init__(
        self,
        coordinator: AmbrogioDataUpdateCoordinator,
        entity_description: VacuumEntityDescription,
        robot_imei: str,
        robot_name: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator=coordinator,
            robot_imei=robot_imei,
            robot_name=robot_name,
            entity_type="vacuum",
            entity_key=entity_description.key,
        )
        self.entity_description = entity_description
        self._attr_supported_features = ROBOT_SUPPORTED_FEATURES

    def update_extra_state_attributes(self) -> None:
        """Update extra attributes."""
        if self._state == 4:
            _attr_status = ROBOT_ERRORS.get(self._error, "unknown")
        else:
            _attr_status = ROBOT_STATES[self._state]["name"]
        # TODO: Currently no way to map this status, but it would be the best way to
        #       present detailed error messages.
        self._additional_extra_state_attributes = {
            ATTR_STATUS: _attr_status,
        }

    @property
    def state(self) -> str:
        """Return the state of the lawn mower."""
        if self._state in (2, 7, 8):
            return STATE_CLEANING
        if self._state == 1:
            return STATE_DOCKED
        if self._state == 3:
            return STATE_PAUSED
        if self._state == 6:
            return STATE_RETURNING
        if self._state == 11:
            return STATE_IDLE
        return STATE_ERROR

    @property
    def error(self) -> str:
        """Define an error message if the vacuum is in STATE_ERROR."""
        if self._state == 4:
            return ROBOT_ERRORS.get(self._error, "unknown")
        return None

    async def async_start(self) -> None:
        """Start or resume the mowing task."""
        await self.coordinator.async_work_now(
            imei=self._robot_imei,
        )

    async def async_pause(self) -> None:
        """Not supported."""
        LOGGER.warning("Method %s.pause is not supported.", DOMAIN)

    async def async_stop(self, **kwargs) -> None:
        """Command the lawn mower return to station until next schedule."""
        await self.async_return_to_base(**kwargs)

    async def async_return_to_base(self, **kwargs) -> None:
        """Command the lawn mower return to station until next schedule."""
        await self.coordinator.async_charge_now(
            imei=self._robot_imei,
        )

    async def async_clean_spot(self, **kwargs: any) -> None:
        """Not supported."""
        LOGGER.warning("Method %s.clean_spot is not supported.", DOMAIN)

    async def async_locate(self, **kwargs: any) -> None:
        """Locate the lawn mower."""
        await self.coordinator.async_trace_position(
            imei=self._robot_imei,
        )

    async def async_set_fan_speed(self, fan_speed: str, **kwargs: any) -> None:
        """Not supported."""
        LOGGER.warning("Method %s.set_fan_speed is not supported.", DOMAIN)

    async def async_send_command(
        self,
        command: str,
        params: dict[str, any] | list[any] | None = None,
        **kwargs: any
    ) -> None:
        """Send a command to lawn mower."""
        await self.coordinator.async_custom_command(
            imei=self._robot_imei,
            command=command,
            params=params,
        )
