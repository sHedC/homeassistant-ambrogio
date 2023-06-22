"""Test the Firebase API, mostly WebSocket."""
from unittest.mock import patch

from aiohttp import web

import pytest

from custom_components.ambrogio_robot.api_firebase import (
    AmbrogioRobotFirebaseAPI,
    AmbrogioRobotException,
)

from .conftest import ClientSessionGenerator


async def test_verify_password(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API sets up correctly."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    result = await api.verify_password("user@email.com", "successpassword")
    assert result != {}
    assert result["SessionToken"] == "google-token-id"
    assert result["AccessToken"] == "access-token"


async def test_invalid_password(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API for invalid password."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    with pytest.raises(AmbrogioRobotException):
        await api.verify_password("user@email.com", "failpassword")


async def test_invalid_email(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API for invalid password."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    with pytest.raises(AmbrogioRobotException):
        await api.verify_password("bad@email.com", "successpassword")


async def test_get_robots(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API to get the robots back."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    robot_list = await api.get_robots("token1", "google-token-id")
    assert robot_list != {}


async def test_invalid_token(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API to get the robots back."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    robot_list = await api.get_robots("no-token", "google-token-id")
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
        await api.get_robots("access-token", "google-token-id")
