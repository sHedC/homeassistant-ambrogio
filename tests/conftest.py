"""Global fixtures for Ambrogio Robot Integration."""
from unittest.mock import patch
import pytest

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from custom_components.ambrogio_robot.const import DOMAIN

TEST_CONFIGDATA = {DOMAIN: {CONF_USERNAME: "user.name", CONF_PASSWORD: "hash"}}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Auto Enable Custom Integrations."""
    yield


@pytest.fixture
def mock_configdata():
    """Return a default mock configuration."""
    return TEST_CONFIGDATA
