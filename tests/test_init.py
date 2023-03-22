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


async def test_setup(hass: HomeAssistant, mock_configdata: dict):
    """Test we can setup the integration."""
    entry = MockConfigEntry(domain=DOMAIN, data=mock_configdata[DOMAIN])
    entry.add_to_hass(hass)

    with patch(
        (
            "custom_components.ambrogio_robot.coordinator."
            "BlueprintDataUpdateCoordinator._async_update_data"
        ),
        return_value={
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": (
                "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit "
                "molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
            ),
        },
    ) as mock_sync:
        assert await async_setup_entry(hass, entry)
        await hass.async_block_till_done()

    assert len(mock_sync.mock_calls) > 0
