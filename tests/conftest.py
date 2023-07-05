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
    CONF_EMAIL,
    CONF_PASSWORD,
)

from custom_components.ambrogio_robot import DOMAIN

ClientSessionGenerator = Callable[..., Coroutine[any, any, TestClient]]

FIREBASE_TEST_VER = "5"
TEST_CONFIGDATA = {
    DOMAIN: {CONF_EMAIL: "user@email.com", CONF_PASSWORD: "successpassword"}
}
TEST_CONFIGOPTIONS = {DOMAIN: {}}


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
    with patch(
        "custom_components.ambrogio_robot.api_firebase.GOOGLEAPIS_URL", ""
    ), patch("custom_components.ambrogio_robot.api_firebase.FIREBASE_URL", ""):
        yield


async def googleapis_auth(request: Request):
    """Respond with the google apis authentication."""
    data = await request.json()
    if (
        data[CONF_EMAIL] == TEST_CONFIGDATA[DOMAIN][CONF_EMAIL]
        and data[CONF_PASSWORD] == TEST_CONFIGDATA[DOMAIN][CONF_PASSWORD]
    ):
        response_txt = load_fixture("api_firebase", "googleapi_auth_success.json")
    else:
        if data[CONF_EMAIL] != TEST_CONFIGDATA[DOMAIN][CONF_EMAIL]:
            response_txt = load_fixture("api_firebase", "googleapi_invalid_email.json")
        else:
            response_txt = load_fixture(
                "api_firebase", "googleapi_invalid_password.json"
            )

    return web.Response(
        text=response_txt,
        content_type="application/json",
    )


async def firebase_handler(request: Request):
    """Websocket handler for firebase reqeusts."""
    ws_response = web.WebSocketResponse()

    if not ws_response.can_prepare(request):
        return web.HTTPUpgradeRequired()

    # Check connection details, Firebase Version & Database
    await ws_response.prepare(request)
    query = request.rel_url.query
    if query["v"] != FIREBASE_TEST_VER:
        msg = json.loads(load_fixture("api_firebase", "ws_firebase_version_error.json"))
        await ws_response.send_json(msg)
        await ws_response.close()
        return ws_response
    else:
        msg = json.loads(load_fixture("api_firebase", "ws_setup_response.json"))
        await ws_response.send_json(msg)

    # Get Authorization Request, respond with correct message.
    msg = await ws_response.receive_json()
    token = msg["d"]["b"]["cred"]
    if token != "google-access-token":
        msg = json.loads(load_fixture("api_firebase", "ws_auth_invalid.json"))
    else:
        msg = json.loads(load_fixture("api_firebase", "ws_auth_response.json"))
    await ws_response.send_json(msg)

    # Get Request for Robots and Respond.
    msg = await ws_response.receive_json()
    robot: str = msg["d"]["b"]["p"]
    access_token = robot.split("/")
    msg = load_fixture("api_firebase", f"ws_getrobots_{access_token[2]}.json")

    # If Access Token is invalid.
    if msg is None:
        msg = json.loads(load_fixture("api_firebase", "ws_getrobots_invalid.json"))
    else:
        msg = json.loads(msg)

    await ws_response.send_json(msg)

    await ws_response.close()
    return ws_response


@pytest.fixture
def google_api(hass):
    """Fixture setup a web application."""
    app = web.Application()
    app["hass"] = hass
    app.router.add_route(
        "POST", "/identitytoolkit/v3/relyingparty/verifyPassword", googleapis_auth
    )
    app.router.add_route("GET", "/.ws", firebase_handler)
    async_setup_forwarded(app, True, [])
    return app
