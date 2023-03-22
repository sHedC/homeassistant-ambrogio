"""Test Ambrogio Robot Setup process."""

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ambrogio_robot.const import DOMAIN


async def test_setup(hass: HomeAssistant, mock_configdata: dict):
    """Test we can setup the integration."""
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)
