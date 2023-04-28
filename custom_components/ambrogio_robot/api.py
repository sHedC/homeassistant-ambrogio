"""Dummy API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class AmbrogioRobotApiClientError(Exception):
    """Exception to indicate a general API error."""


class AmbrogioRobotApiClientCommunicationError(AmbrogioRobotApiClientError):
    """Exception to indicate a communication error."""


class AmbrogioRobotApiClientAuthenticationError(AmbrogioRobotApiClientError):
    """Exception to indicate an authentication error."""


class AmbrogioRobotApiClient:
    """Sample API Client."""

    def __init__(
        self,
        api_key: str,
        access_token: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._api_key = api_key
        self._access_token = access_token
        self._session = session

    async def async_check_api_connect(self) -> bool:
        """Check the API Connectivity is valid."""
        return True

    async def async_check_robot(self, robot_imei: str) -> bool:
        """Check the Robot Exists."""
        return True

    async def async_get_api_id(self) -> str:
        """Get the API Token Key from Google APIs."""
        return "keythatshouldnotbeshared"

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise AmbrogioRobotApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise AmbrogioRobotApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise AmbrogioRobotApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise AmbrogioRobotApiClientError(
                "Something really wrong happened!"
            ) from exception
