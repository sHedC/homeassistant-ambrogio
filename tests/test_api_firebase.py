"""Test the Firebase API, mostly WebSocket."""
from unittest.mock import patch

from aiohttp import web

import pytest

from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_API_TOKEN,
    CONF_EMAIL,
    CONF_PASSWORD,
)

from custom_components.ambrogio_robot import DOMAIN
from custom_components.ambrogio_robot.api_firebase import (
    AmbrogioRobotFirebaseAPI,
    AmbrogioRobotException,
)

from .conftest import ClientSessionGenerator, TEST_CONFIGDATA


async def test_verify_password(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API sets up correctly."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    result = await api.verify_password(
        TEST_CONFIGDATA[DOMAIN][CONF_EMAIL], TEST_CONFIGDATA[DOMAIN][CONF_PASSWORD]
    )
    assert result != {}
    assert result[CONF_API_TOKEN] == "robot-api-token"
    assert result[CONF_ACCESS_TOKEN] == "google-access-token"


async def test_invalid_password(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API for invalid password."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    with pytest.raises(AmbrogioRobotException):
        await api.verify_password(TEST_CONFIGDATA[DOMAIN][CONF_EMAIL], "failpassword")


async def test_invalid_email(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API for invalid password."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    with pytest.raises(AmbrogioRobotException):
        await api.verify_password(
            "bad@email.com", TEST_CONFIGDATA[DOMAIN][CONF_PASSWORD]
        )


async def test_get_robots(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API to get the robots back."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    robot_list = await api.get_robots("google-access-token", "token1")
    assert robot_list != {}


async def test_invalid_token(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API to get the robots back."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    robot_list = await api.get_robots("google-access-token", "no-token")
    assert robot_list == {}


@patch("custom_components.ambrogio_robot.api_firebase.FIREBASE_VER", "1")
async def test_wrong_firebase_version(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API to get the robots back."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    with pytest.raises(AmbrogioRobotException):
        await api.get_robots("agoogle-access-token", "token1")
