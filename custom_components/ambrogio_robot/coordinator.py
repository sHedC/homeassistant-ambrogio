"""DataUpdateCoordinator for Ambrogio Robot."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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
from .const import DOMAIN, LOGGER, ROBOT_STATES


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

    async def _async_update_data(self):
        """Update data via library."""
        try:
            robot_data = {"robots": {}}
            robot_imeis = []
            for robot_imei, robot_name in self.robots.items():
                robot_imeis.append(robot_imei)
                robot_data["robots"][robot_imei] = {
                    "name": robot_name,
                    "imei": robot_imei,
                    "serial": None,
                    "state": 0,
                    "location": {
                        "latitude": None,
                        "longitude": None,
                    },
                }
            
            result = await self.client.execute("thing.list", {
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
                    "varBillingPlanCode"
                ],
                "hideFields": True,
                "keys": robot_imeis
            })
            response = await self.client.get_response()
            if "result" in response:
                result_list = response["result"]
                for robot in ( robot for robot in result_list if "key" in robot and robot["key"] in robot_data["robots"] ):
                    if "alarms" in robot and "robot_state" in robot["alarms"]:
                        robot_state = robot["alarms"]["robot_state"]
                        robot_data["robots"][robot["key"]]["state"] = robot_state["state"]
                        # latitude and longitude, not always available
                        if "lat" in robot_state and "lng" in robot_state:
                            robot_data["robots"][robot["key"]]["location"]["latitude"] = robot_state["lat"]
                            robot_data["robots"][robot["key"]]["location"]["longitude"] = robot_state["lng"]
                        # robot_state["since"] -> timestamp since state change (format 2023-04-30T10:24:47.517Z)
                    if "attrs" in robot and "robot_serial" in robot["attrs"]:
                        robot_serial = robot["attrs"]["robot_serial"]
                        robot_data["robots"][robot["key"]]["serial"] = robot_serial["value"]

            # TODO
            LOGGER.debug("_async_update_data")
            LOGGER.debug(robot_data)
            
            return robot_data

        except AmbrogioRobotApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except AmbrogioRobotApiClientError as exception:
            raise UpdateFailed(exception) from exception
