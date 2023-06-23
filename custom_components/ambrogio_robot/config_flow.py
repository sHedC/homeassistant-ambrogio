"""Adds config flow for Ambrogio."""
import logging
import voluptuous as vol

from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_NAME,
    CONF_ERROR,
)
from homeassistant.config_entries import (
    CONN_CLASS_CLOUD_POLL,
    ConfigFlow,
    FlowResult,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api_firebase import AmbrogioRobotFirebaseAPI, AmbrogioRobotException
from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__name__)


class AmbrogioFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Ambrogio."""

    # Used to call the migration method if the verison changes.
    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the flow for setup."""
        _errors: dict[str, str] = {}

        if user_input is not None:
            result = await authenticate(
                self.hass, user_input[CONF_EMAIL], user_input[CONF_PASSWORD]
            )
            if CONF_ERROR in result:
                _errors["base"] = result[CONF_ERROR]
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default=(user_input or {}).get(CONF_NAME),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_EMAIL,
                        default=(user_input or {}).get(CONF_EMAIL),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_PASSWORD,
                        default=(user_input or {}).get(CONF_PASSWORD),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            errors=_errors,
            last_step=True,
        )


async def authenticate(
    hass: HomeAssistant, email: str, password: str
) -> dict[str, any]:
    """Authenticate and Setup Robots based on Google Login."""
    api = AmbrogioRobotFirebaseAPI(async_get_clientsession(hass))
    try:
        tokens = await api.verify_password(email, password)
    except AmbrogioRobotException as exp:
        _LOGGER.error("Google APIS Auth Failed: %s", exp)
        return {CONF_ERROR: str(exp.message).lower()}

    return tokens
