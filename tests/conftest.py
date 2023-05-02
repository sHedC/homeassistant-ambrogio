"""Global fixtures for Ambrogio Robot Integration."""
from unittest.mock import patch
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
        CONF_MOWERS: {"1223344": "Some Mower"},
    }
}
TEST_CONFIGOPTIONS = {
    CONF_MOWERS: {"1223344": "Some Mower"},
}


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
