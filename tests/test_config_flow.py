"""Test Ambrogio config flow."""
from unittest.mock import patch

import pytest

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant

from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_API_TOKEN,
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_NAME,
    CONF_ERROR,
)

from custom_components.ambrogio_robot.const import DOMAIN


# @pytest.mark.parametrize("expected_lingering_tasks", [True])
# async def test_form_success(hass: HomeAssistant):
#    """Test setting up the form and configuring."""
#    result = await hass.config_entries.flow.async_init(
#        DOMAIN, context={"source": config_entries.SOURCE_USER}
#    )
#    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
#    assert result["errors"] == {}
#
#    with patch(
#        "custom_components.ambrogio_robot.config_flow.AmbrogioFlowHandler._test_setup",
#        return_value="",
#    ) as mock_authenticate:
#        setup_result = await hass.config_entries.flow.async_configure(
#            result["flow_id"],
#            {
#                CONF_API_TOKEN: "api_token",
#                CONF_ACCESS_TOKEN: "access_token",
#                CONF_NAME: "Garage",
#                CONF_ROBOT_NAME: "robot_name",
#                CONF_ROBOT_IMEI: "robot_imei",
#            },
#        )
#        await hass.async_block_till_done()
#
#    assert setup_result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
#    assert setup_result["title"] == "Garage"
#
#    assert len(mock_authenticate.mock_calls) == 1


async def test_form_setup(hass: HomeAssistant):
    """Test initiate form setup."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == config_entries.SOURCE_USER
    assert result["errors"] == {}


async def test_form_login_fail(hass: HomeAssistant):
    """Test setup of robots from google login."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.ambrogio_robot.config_flow.authenticate",
        return_value={CONF_ERROR: "authentication_error"},
    ) as mock_authenticate:
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME: "garage_name",
                CONF_EMAIL: "user@email.com",
                CONF_PASSWORD: "none",
            },
        )
        await hass.async_block_till_done()

    assert len(mock_authenticate.mock_calls) == 1

    assert setup_result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert setup_result["step_id"] == config_entries.SOURCE_USER
    assert setup_result["errors"] == {"base": "authentication_error"}


async def test_form_login_setup(hass: HomeAssistant):
    """Test setup of robots from google login."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.ambrogio_robot.config_flow.authenticate",
        return_value={
            CONF_ACCESS_TOKEN: "google-access-token",
            CONF_API_TOKEN: "robot-api-token",
        },
    ):
        setup_result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME: "garage_name",
                CONF_EMAIL: "some.random@email.com",
                CONF_PASSWORD: "none",
            },
        )

    assert setup_result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert setup_result["title"] == "garage_name"
