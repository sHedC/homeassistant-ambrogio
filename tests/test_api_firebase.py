"""Test the Firebase API, mostly WebSocket."""
from aiohttp import web

import pytest

from custom_components.ambrogio_robot.api_firebase import (
    AmbrogioRobotFirebaseAPI,
    AmbrogioRobotAuthException,
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

    with pytest.raises(AmbrogioRobotAuthException):
        await api.verify_password("user@email.com", "failpassword")


async def test_invalid_email(
    google_api: web.Application, aiohttp_client: ClientSessionGenerator
):
    """Test the API for invalid password."""
    session = await aiohttp_client(google_api)
    api = AmbrogioRobotFirebaseAPI(session)
    assert api is not None

    with pytest.raises(AmbrogioRobotAuthException):
        await api.verify_password("bad@email.com", "successpassword")
