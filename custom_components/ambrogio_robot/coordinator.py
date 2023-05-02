"""DataUpdateCoordinator for Ambrogio Robot."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    ATTR_LOCATION,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_STATE,
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
    CONF_MOWERS,
    CONF_ROBOT_NAME,
    CONF_ROBOT_IMEI,
    ATTR_SERIAL,
    ATTR_CONNECTED,
    ATTR_LAST_COMM,
    ATTR_LAST_SEEN,
    # ROBOT_STATES,
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
        self.client = client
        self.robots = robots
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def __aenter__(self):
        """Return Self."""
        return self

    async def __aexit__(self, *excinfo):
        """Close Session before class is destroyed."""
        await self.client._session.close()

    async def _async_update_data(self):
        """Update data via library."""
        try:
            robot_data = {CONF_MOWERS: {}}
            robot_imeis = []
            for robot_imei, robot_name in self.robots.items():
                robot_imeis.append(robot_imei)
                robot_data[CONF_MOWERS][robot_imei] = {
                    CONF_ROBOT_NAME: robot_name,
                    CONF_ROBOT_IMEI: robot_imei,
                    ATTR_SERIAL: None,
                    ATTR_STATE: 0,
                    ATTR_LOCATION: None,
                    ATTR_CONNECTED: False,
                    ATTR_LAST_COMM: None,
                    ATTR_LAST_SEEN: None,
                }

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
                    if "key" in robot and robot["key"] in robot_data[CONF_MOWERS]
                ):
                    if "alarms" in robot and "robot_state" in robot["alarms"]:
                        robot_state = robot["alarms"]["robot_state"]
                        robot_data[CONF_MOWERS][robot["key"]][ATTR_STATE] = robot_state[
                            "state"
                        ]
                        # latitude and longitude, not always available
                        if "lat" in robot_state and "lng" in robot_state:
                            robot_data[CONF_MOWERS][robot["key"]][ATTR_LOCATION] = {
                                ATTR_LATITUDE: robot_state["lat"],
                                ATTR_LONGITUDE: robot_state["lng"],
                            }
                        # robot_state["since"] -> timestamp since state change
                        # (format 2023-04-30T10:24:47.517Z)
                    if "attrs" in robot and "robot_serial" in robot["attrs"]:
                        robot_serial = robot["attrs"]["robot_serial"]
                        robot_data[CONF_MOWERS][robot["key"]][ATTR_SERIAL] = robot_serial[
                            "value"
                        ]

            # TODO
            LOGGER.debug("_async_update_data")
            LOGGER.debug(robot_data)

            return robot_data

        except AmbrogioRobotApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except AmbrogioRobotApiClientError as exception:
            raise UpdateFailed(exception) from exception
