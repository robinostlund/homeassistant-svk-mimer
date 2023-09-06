"""Config flow to add the integration via the UI."""
from __future__ import annotations

import logging

from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow, CONN_CLASS_CLOUD_POLL
from homeassistant.data_entry_flow import FlowResult

from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import (
    DOMAIN,
    CONF_KW_AVAILABLE,
    CONF_MONITOR_FCR_N,
    CONF_MONITOR_FCR_D_DOWN,
    CONF_MONITOR_FCR_D_UP,
    CONF_FEE_PERCENT,
    CONF_VAT,
    DEFAULT_KW_AVAILABLE,
    DEFAULT_MONITOR_FCR_N,
    DEFAULT_MONITOR_FCR_D_DOWN,
    DEFAULT_MONITOR_FCR_D_UP,
    DEFAULT_FEE_PERCENT,
    DEFAULT_VAT,
    CURRENT_CONFIG_VER,
)

_LOGGER = logging.getLogger(__name__)


class SVKMimerConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = CURRENT_CONFIG_VER

    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Init SVKMimerConfigFlowHandler."""
        self._errors: dict[str, Any] = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            # Check if already configured
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=DOMAIN, data=user_input)

        # create configuration schema
        data_schema = {
            vol.Required(CONF_KW_AVAILABLE, default=DEFAULT_KW_AVAILABLE): vol.Coerce(float),
            vol.Optional(CONF_FEE_PERCENT, default=DEFAULT_FEE_PERCENT): vol.Coerce(int),
            vol.Optional(CONF_VAT, default=DEFAULT_VAT): bool,
            vol.Optional(CONF_MONITOR_FCR_N, default=DEFAULT_MONITOR_FCR_N): bool,
            vol.Optional(CONF_MONITOR_FCR_D_DOWN, default=DEFAULT_MONITOR_FCR_D_DOWN): bool,
            vol.Optional(CONF_MONITOR_FCR_D_UP, default=DEFAULT_MONITOR_FCR_D_UP): bool,
        }

        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema), errors=self._errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the SVKMimerOptionsFlowHandler."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle options flow."""

        if user_input is not None:
            # Update config entry with data from user input
            self.hass.config_entries.async_update_entry(self.config_entry, data=user_input)
            return self.async_create_entry(title=self.config_entry, data=user_input)

        # create configuration schema
        data_schema = {
            vol.Required(
                CONF_KW_AVAILABLE, default=self.config_entry.options.get(CONF_KW_AVAILABLE, DEFAULT_KW_AVAILABLE)
            ): vol.Coerce(float),
            vol.Optional(
                CONF_FEE_PERCENT, default=self.config_entry.options.get(CONF_FEE_PERCENT, DEFAULT_FEE_PERCENT)
            ): vol.Coerce(int),
            vol.Optional(CONF_VAT, default=self.config_entry.options.get(CONF_VAT, DEFAULT_VAT)): bool,
            vol.Optional(
                CONF_MONITOR_FCR_N, default=self.config_entry.options.get(CONF_MONITOR_FCR_N, DEFAULT_MONITOR_FCR_N)
            ): bool,
            vol.Optional(
                CONF_MONITOR_FCR_D_DOWN,
                default=self.config_entry.options.get(CONF_MONITOR_FCR_D_DOWN, DEFAULT_MONITOR_FCR_D_DOWN),
            ): bool,
            vol.Optional(
                CONF_MONITOR_FCR_D_UP,
                default=self.config_entry.options.get(CONF_MONITOR_FCR_D_UP, DEFAULT_MONITOR_FCR_D_UP),
            ): bool,
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(data_schema))
