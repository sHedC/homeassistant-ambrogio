"""Global fixtures for Ambrogio Robot Integration."""
from collections.abc import Callable, Coroutine

from unittest.mock import patch
import os
import json

from aiohttp import web
from aiohttp.test_utils import TestClient, Request

import pytest

from homeassistant.components.http.forwarded import async_setup_forwarded
from homeassistant.const import (
    CONF_API_TOKEN,
    CONF_ACCESS_TOKEN,
)

from custom_components.ambrogio_robot.const import (
    DOMAIN,
    CONF_MOWERS,
)

TEST_CONFIGDATA = {
    DOMAIN: {
        CONF_API_TOKEN: "apitoken",
        CONF_ACCESS_TOKEN: "access_token",
    }
}
TEST_CONFIGOPTIONS = {
    DOMAIN: {
        CONF_MOWERS: {"1234567890": "Some Mower"},
    }
}

ClientSessionGenerator = Callable[..., Coroutine[any, any, TestClient]]


@pytest.fixture
def aiohttp_client(
    event_loop, aiohttp_client, socket_enabled
):  # pylint: disable=unused-argument, redefined-outer-name
    """Return aiohttp_client and allow opening sockets."""
    return aiohttp_client


def load_fixture(folder: str, filename: str) -> str:
    """Load a JSON fixture for testing."""
    try:
        path = os.path.join(os.path.dirname(__file__), "fixtures", folder, filename)
        with open(path, encoding="utf-8") as fptr:
            return fptr.read()
    except OSError:
        return None


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations,
):  # pylint: disable=unused-argument
    """Auto Enable Custom Integrations."""
    yield


@pytest.fixture
def mock_configdata():
    """Return a default mock configuration."""
    return TEST_CONFIGDATA


@pytest.fixture
def mock_configopts():
    """Return a default mock options."""
    return TEST_CONFIGOPTIONS


@pytest.fixture
def mock_robotdata():
    """Return default mock Robot Data."""
    return json.loads(load_fixture("controller", "default_data.json"))


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


# --------------------------------------------------
# Google Authantication API.
@pytest.fixture(autouse=True)
def api_firebase_url():
    """Patch the URL Base for the firebase api."""
    with patch("custom_components.ambrogio_robot.api_firebase.URL_BASE", ""):
        yield


async def googleapis_auth(request: Request):
    """Respond with the google apis authentication."""
    data = await request.json()
    if data["email"] == "user@email.com" and data["password"] == "successpassword":
        response_txt = load_fixture("api_firebase", "googleapi_auth_success.json")
    else:
        if data["email"] != "user@email.com":
            response_txt = load_fixture("api_firebase", "googleapi_invalid_email.json")
        else:
            response_txt = load_fixture(
                "api_firebase", "googleapi_invalid_password.json"
            )

    return web.Response(
        text=response_txt,
        content_type="application/json",
    )


@pytest.fixture
def google_api(hass):
    """Fixture setup a web application."""
    app = web.Application()
    app["hass"] = hass
    app.router.add_route(
        "POST", "/identitytoolkit/v3/relyingparty/verifyPassword", googleapis_auth
    )
    async_setup_forwarded(app, True, [])
    return app
