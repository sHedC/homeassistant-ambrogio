"""Test Ambrogio Robot Setup process."""
from unittest.mock import patch
import pytest

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntryState

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ambrogio_robot import (
    async_setup_entry,
    async_reload_entry,
)
from custom_components.ambrogio_robot.coordinator import AmbrogioDataUpdateCoordinator
from custom_components.ambrogio_robot.const import DOMAIN


@pytest.fixture(autouse=True)
def override_entity():
    """Override the PLATFORMS."""
    with patch(
        "custom_components.ambrogio_robot.PLATFORMS",
        {},
    ):
        yield


async def test_setup_and_reload(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_configopts: dict,
    mock_robotdata: dict,
):
    """Test we can setup the integration."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=mock_configdata[DOMAIN], options=mock_configopts[DOMAIN]
    )
    entry.add_to_hass(hass)

    with patch(
        (
            "custom_components.ambrogio_robot.coordinator."
            "AmbrogioDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_robotdata,
    ) as mock_sync:
        assert await async_setup_entry(hass, entry)
        await hass.async_block_till_done()

        assert (
            len(hass.config_entries.flow.async_progress()) == 0
        ), "Flow is in Progress it should not be."

        assert DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]
        assert isinstance(
            hass.data[DOMAIN][entry.entry_id], AmbrogioDataUpdateCoordinator
        )

        # Reload the entry and assert that the data from above is still there
        assert await async_reload_entry(hass, entry) is None
        assert DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]
        assert isinstance(
            hass.data[DOMAIN][entry.entry_id], AmbrogioDataUpdateCoordinator
        )

    assert len(mock_sync.mock_calls) > 0


async def test_unload_entry(
    hass: HomeAssistant,
    mock_configdata: dict,
    mock_configopts: dict,
    mock_robotdata: dict,
):
    """Test being able to unload an entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=mock_configdata[DOMAIN],
        options=mock_configopts[DOMAIN],
        entry_id="test",
    )
    entry.add_to_hass(hass)

    # Check the Config is initiated
    with patch(
        (
            "custom_components.ambrogio_robot.coordinator."
            "AmbrogioDataUpdateCoordinator._async_update_data"
        ),
        return_value=mock_robotdata,
    ) as mock_updater:
        assert (
            await hass.config_entries.async_setup(entry.entry_id) is True
        ), "Component did not setup correctly."
        await hass.async_block_till_done()

    assert len(mock_updater.mock_calls) >= 1, "Mock Entity was not called."

    # Perform and Check Unload Config
    assert (
        await hass.config_entries.async_unload(entry.entry_id) is True
    ), "Component Config Unload Failed."
    assert entry.state == ConfigEntryState.NOT_LOADED
