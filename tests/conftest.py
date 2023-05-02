"""Global fixtures for Ambrogio Robot Integration."""
from unittest.mock import patch
import os
import json
import pytest

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
    CONF_MOWERS: {"1234567890": "Some Mower"},
}


def load_fixture(folder: str, filename: str) -> dict:
    """Load a JSON fixture for testing."""
    try:
        path = os.path.join(os.path.dirname(__file__), "fixtures", folder, filename)
        with open(path, encoding="utf-8") as fptr:
            return json.loads(fptr.read())
    except OSError:
        return {}


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
    return load_fixture("controller", "default_data.json")


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
