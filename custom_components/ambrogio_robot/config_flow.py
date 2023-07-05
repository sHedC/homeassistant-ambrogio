"""Adds config flow for Ambrogio."""
import logging
import voluptuous as vol

from homeassistant.const import (
    CONF_EMAIL,
    CONF_ERROR,
    CONF_PASSWORD,
)
from homeassistant.config_entries import (
    CONN_CLASS_CLOUD_POLL,
    ConfigFlow,
    ConfigEntry,
    FlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api_firebase import AmbrogioRobotFirebaseAPI, AmbrogioRobotException
from .const import (
    DOMAIN,
    UPDATE_INTERVAL_DEFAULT,
    UPDATE_INTERVAL_WORKING,
    CONF_SCAN_INTERVAL_DEFAULT,
    CONF_SCAN_INTERVAL_WORKING,
)

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
                # Setup the Unique ID and check if already configured
                await self.async_set_unique_id(user_input[CONF_EMAIL])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_EMAIL], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
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

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return the option flow handler."""
        return AmbrogioOptionsFlowHandler(config_entry)


class AmbrogioOptionsFlowHandler(OptionsFlow):
    """Ambrogio config options flow handler."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self,
        user_input: dict[str, any] | None = None,  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL_DEFAULT,
                        default=self.options.get(
                            CONF_SCAN_INTERVAL_DEFAULT, UPDATE_INTERVAL_DEFAULT
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=120, max=600)),
                    vol.Required(
                        CONF_SCAN_INTERVAL_WORKING,
                        default=self.options.get(
                            CONF_SCAN_INTERVAL_WORKING, UPDATE_INTERVAL_WORKING
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=120)),
                }
            ),
        )

    async def _update_options(self) -> FlowResult:
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_EMAIL), data=self.options
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
