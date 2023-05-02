"""Adds config flow for Ambrogio."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlow,
    CONN_CLASS_CLOUD_POLL,
)
from homeassistant.const import (
    CONF_NAME,
    CONF_API_TOKEN,
    CONF_ACCESS_TOKEN,
    CONF_SCAN_INTERVAL,
    TIME_HOURS,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    AmbrogioRobotApiClient,
    AmbrogioRobotApiClientAuthenticationError,
    AmbrogioRobotApiClientCommunicationError,
    AmbrogioRobotApiClientError,
)
from .const import (
    DOMAIN,
    LOGGER,
    API_TOKEN,
    CONF_CONFIRM,
    CONF_MOWERS,
    CONF_ROBOT_NAME,
    CONF_ROBOT_IMEI,
    CONF_SELECTED_ROBOT,
)


class AmbrogioFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Ambrogio."""

    # Used to call the migration method if the verison changes.
    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return AmbrogioOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                # Try to login to google and get the API Key.
                api_response = await self._test_setup(
                    api_token=user_input[CONF_API_TOKEN],
                    access_token=user_input[CONF_ACCESS_TOKEN],
                    robot_imei=user_input["robot_imei"],
                )
                if api_response == "":
                    # On Success setup the account and first Mower in the List
                    user_settings = {}
                    user_settings[CONF_NAME] = user_input[CONF_NAME]
                    user_settings[CONF_API_TOKEN] = user_input[CONF_API_TOKEN]
                    user_settings[CONF_ACCESS_TOKEN] = user_input[CONF_ACCESS_TOKEN]

                    user_options = {}
                    user_options[CONF_MOWERS] = {}
                    user_options[CONF_MOWERS][user_input["robot_imei"]] = user_input[
                        "robot_name"
                    ]
                else:
                    _errors["base"] = api_response

            except AmbrogioRobotApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except AmbrogioRobotApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except AmbrogioRobotApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                if not _errors:
                    return self.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_settings,
                        options=user_options,
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
                        CONF_API_TOKEN,
                        default=(user_input or {}).get(CONF_API_TOKEN, API_TOKEN),
                        description="API Token for Connecting.",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_ACCESS_TOKEN,
                        default=(user_input or {}).get(CONF_ACCESS_TOKEN),
                        description="User Access Token from App.",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_ROBOT_NAME,
                        default=(user_input or {}).get(CONF_ROBOT_NAME),
                        description="Everyone names their robot. You know you have one.",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_ROBOT_IMEI,
                        default=(user_input or {}).get(CONF_ROBOT_IMEI),
                        description="The IMEI of the Robot SIM card.",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_setup(
        self, api_token: str, access_token: str, robot_imei: str
    ) -> str:
        """Test the Initial Settings connect and mower exists."""
        session = async_create_clientsession(self.hass)
        return_msg = ""
        client_api = AmbrogioRobotApiClient(api_token, access_token, session)
        if await client_api.async_check_api_connect():
            # Validate Mower Exists.
            if await client_api.async_check_robot(robot_imei=robot_imei):
                return_msg = ""
            else:
                return_msg = "robot_not_found"
        else:
            return_msg = "unknown"

        session.close()
        return return_msg


class AmbrogioOptionsFlowHandler(OptionsFlow):
    """Handle the Ambrogio Robot Options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialise Ambrogio Robot options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict | None = None  # pylint: disable=unused-argument
    ) -> FlowResult:
        """Options Menu for Ambrogio Robots."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["settings", "add", "change", "delete"],
        )

    async def async_step_settings(self, user_input: dict | None = None) -> FlowResult:
        """Manage the Ambrogio Robot settings."""
        _errors: dict[str, str] = {}

        if user_input is not None:
            # If user In put, check what is changed and what needs updating.
            if user_input[CONF_API_TOKEN] != self.config_entry.data.get(
                CONF_API_TOKEN
            ) or user_input[CONF_ACCESS_TOKEN] != self.config_entry.data.get(
                CONF_ACCESS_TOKEN
            ):
                # TODO Validate New Login and update settings
                self.config_entry.data[CONF_API_TOKEN] = user_input[CONF_API_TOKEN]
                self.config_entry.data[CONF_ACCESS_TOKEN] = user_input[
                    CONF_ACCESS_TOKEN
                ]

            if not _errors:
                self.options[CONF_SCAN_INTERVAL] = user_input[CONF_SCAN_INTERVAL]
                return await self._update_options()
        else:
            user_input = {}

        return self.async_show_form(
            step_id="settings",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_TOKEN,
                        default=user_input.get(
                            CONF_API_TOKEN,
                            self.config_entry.data.get(CONF_API_TOKEN, API_TOKEN),
                        ),
                        description="API Token for Connecting",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_ACCESS_TOKEN,
                        default=user_input.get(
                            CONF_ACCESS_TOKEN,
                            self.config_entry.data.get(CONF_ACCESS_TOKEN),
                        ),
                        description="User Access Token from App",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=user_input.get(
                            CONF_SCAN_INTERVAL, self.options.get(CONF_SCAN_INTERVAL, 60)
                        ),
                        description="Scan Interval for polling the over air API",
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=30,
                            max=240,
                            unit_of_measurement=TIME_HOURS,
                            mode=selector.NumberSelectorMode.SLIDER,
                        )
                    ),
                }
            ),
            errors=_errors,
        )

    async def async_step_add(self, user_input: dict | None = None) -> FlowResult:
        """Add a Robot to the Garage."""
        _errors: dict[str, str] = {}

        if user_input is not None:
            # Check for Duplicates
            all_mowers: dict = self.options[CONF_MOWERS]
            robot_imei = user_input[CONF_ROBOT_IMEI]
            robot_name = user_input[CONF_ROBOT_NAME]
            if robot_imei in all_mowers:
                _errors["base"] = "imei_exists"
            elif robot_name in all_mowers.values():
                _errors["base"] = "name_exists"
            else:
                # TODO: Validate Input, check for duplicates.
                all_mowers[robot_imei] = robot_name
                return await self._update_options()

        return self.async_show_form(
            step_id="add",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ROBOT_NAME,
                        description="Everyone names their robot",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_ROBOT_IMEI,
                        description="The IMEI of the Robot SIM card",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                }
            ),
            errors=_errors,
            last_step=True,
        )

    async def async_step_change(self, user_input: dict | None = None) -> FlowResult:
        """Select a Robot to Change."""
        _errors: dict[str, str] = {}
        last_step = False

        # Build the Mower Configurations Up
        mowers: dict = self.options[CONF_MOWERS]
        mower_list = []
        for mower_imei in mowers:
            mower_list.append(
                selector.SelectOptionDict(
                    value=mower_imei, label=f"{mowers[mower_imei]} ({mower_imei})"
                )
            )

        robot_imei = ""
        if user_input is not None:
            robot_imei = user_input[CONF_SELECTED_ROBOT]
            if CONF_ROBOT_NAME not in user_input:
                robot_name = mowers[robot_imei]
            else:
                # TODO: Process Change, Check if New Name exists and if changed.
                robot_name = user_input[CONF_ROBOT_NAME]
                if robot_name != mowers[robot_imei]:
                    if robot_name in mowers.values():
                        _errors["base"] = "name_exists"

                if not _errors:
                    mowers[robot_imei] = robot_name
                    return await self._update_options()

        form_schema = {
            vol.Required(
                CONF_SELECTED_ROBOT,
                default=robot_imei,
                description="Select Robot",
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=mower_list,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_SELECTED_ROBOT,
                )
            )
        }
        if robot_imei != "":
            last_step = True
            form_schema.update(
                {
                    vol.Required(
                        CONF_ROBOT_NAME,
                        default=robot_name,
                        description="Robot Name",
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                }
            )

        # Show the Form.
        return self.async_show_form(
            step_id="change",
            data_schema=vol.Schema(form_schema),
            errors=_errors,
            last_step=last_step,
        )

    async def async_step_delete(self, user_input: dict | None = None) -> FlowResult:
        """Delete a Robot from the Garage"""
        _errors: dict[str, str] = {}

        mowers: dict = self.options[CONF_MOWERS]
        if user_input is not None:
            if len(mowers) == 1:
                return self.async_abort(reason="last_robot")

            robot_imei = user_input[CONF_SELECTED_ROBOT]
            confirm = user_input[CONF_CONFIRM]
            if not confirm:
                _errors["base"] = "del_not_confirmed"
            else:
                # TODO: Remove Entities from HASS
                del mowers[robot_imei]
                return await self._update_options()
        else:
            user_input = {}

        # Build the Mower Configurations Up
        mower_list = []
        for mower_imei in mowers.keys():
            mower_list.append(
                selector.SelectOptionDict(
                    value=mower_imei, label=f"{mowers[mower_imei]} ({mower_imei})"
                )
            )

        return self.async_show_form(
            step_id="delete",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SELECTED_ROBOT,
                        default=user_input.get(CONF_SELECTED_ROBOT),
                        description="Selecting Robot",
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=mower_list,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_SELECTED_ROBOT,
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_CONFIRM, default=False, description="Confirm Deletion"
                    ): selector.BooleanSelector(),
                }
            ),
            errors=_errors,
            last_step=True,
        )

    async def _update_options(self) -> FlowResult:
        """Update config entry options."""
        return self.async_create_entry(title="", data=self.options)
