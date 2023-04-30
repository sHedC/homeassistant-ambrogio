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
            # TODO
            LOGGER.error("_async_update_data")
            
            robot_data = {"robots": {}}
            robot_imeis = []
            for robot_imei, robot_name in self.robots.items():
                robot_imeis.append(robot_imei)
                robot_data["robots"][robot_imei] = {
                    "name": robot_name,
                    "imei": robot_imei,
                    "state": "unknown",
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
            if "params" in response:
                if "result" in response["params"]:
                    result_list = response["params"]["result"]
                    for i in range(len(result_list)):
                        robot = result_list[i]
                        if "key" in robot and "alarms" in robot:
                            if "robot_state" in robot["alarms"] and robot["key"] in robot_data["robots"]:
                                robot_state = robot["alarms"]["robot_state"]
                                
                                # robot_state["since"] -> timestamp since state change (format 2023-04-30T10:24:47.517Z)
                                # robot_state["lat"] -> latitude, not always available
                                # robot_state["lng"] -> longitude, not always available
                                
                                robot_data["robots"][robot["key"]]["state"] = ROBOT_STATES[robot_state["state"]]["name"]
            
            # TODO
            LOGGER.error(robot_data)
            
            return robot_data

        except AmbrogioRobotApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except AmbrogioRobotApiClientError as exception:
            raise UpdateFailed(exception) from exception
