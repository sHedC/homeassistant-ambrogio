"""Test Ambrogio config flow."""
from unittest.mock import patch

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_API_TOKEN,
    CONF_ACCESS_TOKEN,
    CONF_NAME,
)

from custom_components.ambrogio_robot.const import (
    DOMAIN,
    CONF_ROBOT_NAME,
    CONF_ROBOT_IMEI,
)


async def test_form_success(hass: HomeAssistant):
    """Test setting up the form and configuring."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {}

    # TODO: This failes with Lingering Timer, need to figure that out.
    # with patch(
    #    "custom_components.ambrogio_robot.config_flow.AmbrogioFlowHandler._test_setup",
    #    return_value="",
    # ) as mock_authenticate:
    #    setup_result = await hass.config_entries.flow.async_configure(
    #        result["flow_id"],
    #        {
    #            CONF_API_TOKEN: "api_token",
    #            CONF_ACCESS_TOKEN: "access_token",
    #            CONF_NAME: "Garage",
    #            CONF_ROBOT_NAME: "robot_name",
    #            CONF_ROBOT_IMEI: "robot_imei",
    #        },
    #    )
    #    await hass.async_block_till_done()

    # assert setup_result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    # assert setup_result["title"] == "Garage"

    # assert len(mock_authenticate.mock_calls) == 1
