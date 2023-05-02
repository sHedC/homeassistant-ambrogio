"""Test the Diagnostics."""
from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ambrogio_robot.const import DOMAIN


async def test_diagnostics(
    hass: HomeAssistant, mock_configdata: dict, mock_configopts: dict
):
    """Test Diagnostics work."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=mock_configdata[DOMAIN], options=mock_configopts[DOMAIN]
    )
    entry.add_to_hass(hass)

    # TODO: Build and Test Diagnostics
