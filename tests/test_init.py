"""Test Ambrogio Robot Setup process."""
from unittest.mock import patch
import pytest

from homeassistant.core import HomeAssistant

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ambrogio_robot import async_setup_entry
from custom_components.ambrogio_robot.const import DOMAIN


@pytest.fixture(autouse=True)
def override_entity():
    """Override the PLATFORMS."""
    with patch(
        "custom_components.ambrogio_robot.PLATFORMS",
        {},
    ):
        yield


async def test_setup(hass: HomeAssistant, mock_configdata: dict, mock_configopts: dict):
    """Test we can setup the integration."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=mock_configdata[DOMAIN], options=mock_configopts
    )
    entry.add_to_hass(hass)

    with patch(
        (
            "custom_components.ambrogio_robot.coordinator."
            "AmbrogioDataUpdateCoordinator._async_update_data"
        ),
        return_value={
            "robots": {
                "12233444": {
                    "name": "robot_name",
                    "imei": "robot_imei",
                    "state": "charging",
                }
            }
        },
    ) as mock_sync:
        assert await async_setup_entry(hass, entry)
        await hass.async_block_till_done()

    assert len(mock_sync.mock_calls) > 0
