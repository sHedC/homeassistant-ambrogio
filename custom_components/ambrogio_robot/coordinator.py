"""DataUpdateCoordinator for Ambrogio Robot."""
from __future__ import annotations

import asyncio

from datetime import (
    timedelta,
    datetime,
)
from pytz import timezone

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    ATTR_LOCATION,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_STATE,
    ATTR_SW_VERSION,
)
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import (
    AmbrogioRobotApiClient,
    AmbrogioRobotApiClientAuthenticationError,
    AmbrogioRobotApiClientError,
)
from .const import (
    DOMAIN,
    LOGGER,
    API_DATETIME_FORMAT_DEFAULT,
    API_DATETIME_FORMAT_FALLBACK,
    API_ACK_TIMEOUT,
    CONF_MOWERS,
    CONF_ROBOT_NAME,
    CONF_ROBOT_IMEI,
    ATTR_SERIAL,
    ATTR_ERROR,
    ATTR_CONNECTED,
    ATTR_LAST_COMM,
    ATTR_LAST_SEEN,
)


class AmbrogioDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        robots: dict[str, str],
        client: AmbrogioRobotApiClient,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )
        self.robots = robots
        self.client = client

        self.robot_data = {}

        self._loop = asyncio.get_event_loop()

    def _convert_datetime_from_api(
        self,
        date_string: str,
    ) -> datetime:
        """Convert datetime string from API data into datetime object."""
        try:
            return datetime.strptime(date_string, API_DATETIME_FORMAT_DEFAULT)
        except ValueError:
            return datetime.strptime(date_string, API_DATETIME_FORMAT_FALLBACK)

    def _get_datetime_from_duration(
        self,
        duration: int,
    ) -> datetime:
        """Get datetime object by adding a duration to the current time."""
        locale_timezone = timezone(str(self.hass.config.time_zone))
        datetime_now = datetime.utcnow().astimezone(locale_timezone)
        return datetime_now + timedelta(minutes=duration)

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.client._session.close()

    async def _async_update_data(self):
        """Update data via library."""
        try:
            robot_data = {}
            robot_imeis = []
            for robot_imei, robot_name in self.robots.items():
                robot_imeis.append(robot_imei)
                robot_data[robot_imei] = {
                    CONF_ROBOT_NAME: robot_name,
                    CONF_ROBOT_IMEI: robot_imei,
                    ATTR_SERIAL: None,
                    ATTR_SW_VERSION: None,
                    ATTR_STATE: 0,
                    ATTR_ERROR: 0,
                    ATTR_LOCATION: None,
                    ATTR_CONNECTED: False,
                    ATTR_LAST_COMM: None,
                    ATTR_LAST_SEEN: None,
                }
            if len(robot_imeis) == 0:
                return robot_data

            await self.client.execute(
                "thing.list",
                {
                    "show": [
                        "id",
                        "key",
                        "name",
                        "connected",
                        "lastSeen",
                        "lastCommunication",
                        "loc",
                        "properties",
                        "alarms",
                        "attrs",
                        "createdOn",
                        "storage",
                        "varBillingPlanCode",
                    ],
                    "hideFields": True,
                    "keys": robot_imeis,
                },
            )
            response = await self.client.get_response()
            if "result" in response:
                result_list = response["result"]
                for robot in (
                    robot
                    for robot in result_list
                    if "key" in robot and robot["key"] in robot_data
                ):
                    if "alarms" in robot and "robot_state" in robot["alarms"]:
                        robot_state = robot["alarms"]["robot_state"]
                        robot_data[robot["key"]][ATTR_STATE] = robot_state[
                            "state"
                        ]
                        if "msg" in robot_state:
                            robot_data[robot["key"]][ATTR_ERROR] = int(robot_state[
                                "msg"
                            ])
                        # latitude and longitude, not always available
                        if "lat" in robot_state and "lng" in robot_state:
                            robot_data[robot["key"]][ATTR_LOCATION] = {
                                ATTR_LATITUDE: robot_state["lat"],
                                ATTR_LONGITUDE: robot_state["lng"],
                            }
                    if "attrs" in robot:
                        if "robot_serial" in robot["attrs"]:
                            robot_data[robot["key"]][ATTR_SERIAL] = robot["attrs"]["robot_serial"][
                                "value"
                            ]
                        if "program_version" in robot["attrs"]:
                            robot_data[robot["key"]][ATTR_SW_VERSION] = robot["attrs"]["program_version"][
                                "value"
                            ]
                    if "connected" in robot:
                        robot_data[robot["key"]][ATTR_CONNECTED] = robot["connected"]
                    if "lastCommunication" in robot:
                        robot_data[robot["key"]][ATTR_LAST_COMM] = self._convert_datetime_from_api(robot["lastCommunication"])
                    if "lastSeen" in robot:
                        robot_data[robot["key"]][ATTR_LAST_SEEN] = self._convert_datetime_from_api(robot["lastSeen"])

            # TODO
            LOGGER.debug("_async_update_data")
            LOGGER.debug(robot_data)

            self.robot_data = robot_data

            return {
                CONF_MOWERS: self.robot_data,
            }
        except AmbrogioRobotApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except AmbrogioRobotApiClientError as exception:
            raise UpdateFailed(exception) from exception

    async def async_prepare_for_command(
        self,
        imei: str,
    ) -> bool:
        """Prepare lawn mower for incomming command."""
        try:
            await self.client.execute(
                "thing.find",
                {
                    "imei": imei,
                },
            )
            response = await self.client.get_response()
            connected = response.get("connected", False)
            if connected is True:
                return True
            await self.async_wake_up(imei)
            await asyncio.sleep(5)

            attempt = 0
            while connected is False and attempt < 31:
                await self.client.execute(
                    "thing.find",
                    {
                        "imei": imei,
                    },
                )
                response = await self.client.get_response()
                connected = response.get("connected", False)
                if connected is True:
                    return True
                attempt = attempt + 1
                await asyncio.sleep(5)
            raise asyncio.TimeoutError(
                f"The lawn mower with IMEI {imei} was not available after a long wait"
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_wake_up(
        self,
        imei: str,
    ) -> bool:
        """Send command wake_up to lawn nower."""
        LOGGER.debug(f"wake_up: {imei}")
        try:
            return await self.client.execute(
                "sms.send",
                {
                    "coding": "SEVEN_BIT",
                    "imei": imei,
                    "message": "UP",
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)
        return False

    async def async_set_profile(
        self,
        imei: str,
        profile: int,
    ) -> bool:
        """Send command set_profile to lawn nower."""
        LOGGER.debug(f"set_profile: {imei}")
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "set_profile",
                    "imei": imei,
                    "params": {
                        "profile": (profile - 1),
                    },
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_work_now(
        self,
        imei: str,
        area: int | None = None,
    ) -> bool:
        """Send command work_now to lawn nower."""
        LOGGER.debug(f"work_now: {imei}")
        _params = {}
        if isinstance(area, int) and area in range(1, 10):
            _params["area"] = area - 1
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "work_now",
                    "imei": imei,
                    "params": _params,
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_work_for(
        self,
        imei: str,
        duration: int,
        area: int | None = None,
    ) -> bool:
        """Prepare command work_for."""
        LOGGER.debug(f"work_for: {imei}")
        _target = self._get_datetime_from_duration(duration)
        await self.async_work_until(
            imei=imei,
            hours=_target.hour,
            minutes=_target.minute,
            area=area,
        )

    async def async_work_until(
        self,
        imei: str,
        hours: int,
        minutes: int,
        area: int | None = None,
    ) -> bool:
        """Send command work_until to lawn nower."""
        LOGGER.debug(f"work_until: {imei}")
        _params = {
            "hh": hours,
            "mm": minutes,
        }
        if isinstance(area, int) and area in range(1, 10):
            _params["area"] = area - 1
        else:
            _params["area"] = 255
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "work_until",
                    "imei": imei,
                    "params": _params,
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_border_cut(
        self,
        imei: str,
    ) -> bool:
        """Send command border_cut to lawn nower."""
        LOGGER.debug(f"border_cut: {imei}")
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "border_cut",
                    "imei": imei,
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_charge_now(
        self,
        imei: str,
    ) -> bool:
        """Send command charge_now to lawn nower."""
        LOGGER.debug(f"charge_now: {imei}")
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "charge_now",
                    "imei": imei,
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_charge_for(
        self,
        imei: str,
        duration: int,
    ) -> bool:
        """Prepare command charge_until."""
        _target = self._get_datetime_from_duration(duration)
        await self.async_charge_until(
            imei=imei,
            hours=_target.hour,
            minutes=_target.minute,
            weekday=_target.isoweekday(),
        )

    async def async_charge_until(
        self,
        imei: str,
        hours: int,
        minutes: int,
        weekday: int,
    ) -> bool:
        """Send command charge_until to lawn nower."""
        LOGGER.debug(f"charge_until: {imei}")
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "charge_until",
                    "imei": imei,
                    "params": {
                        "hh": hours,
                        "mm": minutes,
                        "weekday": (weekday - 1),
                    },
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_trace_position(
        self,
        imei: str,
    ) -> bool:
        """Send command trace_position to lawn nower."""
        LOGGER.debug(f"trace_position: {imei}")
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "trace_position",
                    "imei": imei,
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_keep_out(
        self,
        imei: str,
        latitude: float,
        longitude: float,
        radius: int,
        hours: int | None = None,
        minutes: int | None = None,
        index: int | None = None,
    ) -> bool:
        """Send command keep_out to lawn nower."""
        LOGGER.debug(f"keep_out: {imei}")
        _params = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
        }
        if isinstance(hours, int) and hours in range(0, 23):
            _params["hh"] = hours
        if isinstance(minutes, int) and minutes in range(0, 59):
            _params["mm"] = minutes
        if isinstance(index, int):
            _params["index"] = index
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": "keep_out",
                    "imei": imei,
                    "params": _params,
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)

    async def async_custom_command(
        self,
        imei: str,
        command: str,
        params: dict[str, any] | list[any] | None = None,
    ) -> bool:
        """Send custom command to lawn nower."""
        try:
            await self.async_prepare_for_command(imei)
            return await self.client.execute(
                "method.exec",
                {
                    "method": command,
                    "imei": imei,
                    "params": params,
                    "ackTimeout": API_ACK_TIMEOUT,
                    "singleton": True,
                },
            )
        except Exception as exception:
            LOGGER.exception(exception)
