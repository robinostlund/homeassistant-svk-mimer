"""SVK Mimer integration."""
import asyncio
import logging
import voluptuous as vol

from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from datetime import datetime, date, timedelta
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_track_time_change


from aiosvkmimer.client import Mimer

from .const import (
    DOMAIN,
    CONF_KW_AVAILABLE,
    CONF_VAT,
    DEFAULT_KW_AVAILABLE,
    DEFAULT_VAT,
    STARTUP_MESSAGE,
    PLATFORMS,
    UPDATE_INTERVAL,
    EVENT_NEW_HOUR,
    EVENT_NEW_DAY,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class SVKMimerDeviceState:
    """Data retrieved from a SVK Mimer."""

    prices_fcr_n: set[dict]
    prices_fcr_d_up: set[dict]
    prices_fcr_d_down: set[dict]


class SVKMimerDataUpdateCoordinator(DataUpdateCoordinator[SVKMimerDeviceState]):
    """Class to manage fetching SVK Mimer data."""

    def __init__(self, hass: HomeAssistant, *, entry: ConfigEntry) -> None:
        """Initialize data updater."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=UPDATE_INTERVAL))

        self.session = Mimer()

    async def _fetch_data(self) -> SVKMimerDeviceState:
        """Fetch data from SVK Mimer"""
        _LOGGER.debug(f"called _fetch_data")

        await self.session.fetch(
            period_from=date.today().strftime("%Y-%m-%d"), period_to=(date.today() + timedelta(1)).strftime("%Y-%m-%d")
        )

        return SVKMimerDeviceState(
            prices_fcr_n=self.session.get_fcr_n_prices(),
            prices_fcr_d_up=self.session.get_fcr_d_up_prices(),
            prices_fcr_d_down=self.session.get_fcr_d_down_prices(),
        )

    async def _async_update_data(self) -> None:
        """Update data from SVK Mimer."""
        _LOGGER.debug(f"called _async_update_data")
        try:
            data = await self._fetch_data()
            self.last_updated = datetime.now()
            return data
        except AsyncioTimeoutError as error:
            _LOGGER.debug("Asyncio timeout: %s", error)
            raise ConfigEntryNotReady from error
        except Exception as error:
            _LOGGER.debug("Exception in async_setup_entry: %s", error)
            raise ConfigEntryNotReady from Exception
        # except ApiError as err:
        #     raise UpdateFailed(f"Error communicating with API: {err}")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""

    async def cb_new_hr(_):
        """Callback to tell the sensors to update on a new hour."""
        _LOGGER.debug("Called new_hr callback")
        async_dispatcher_send(hass, EVENT_NEW_HOUR)

    async def cb_new_day(_):
        """Callback to handle some house keeping when it is a new day."""
        _LOGGER.debug("Called new_day_cb callback")
        async_dispatcher_send(hass, EVENT_NEW_DAY)

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    coordinator = SVKMimerDataUpdateCoordinator(hass, entry=entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # https://github.com/custom-components/nordpool/blob/master/custom_components/nordpool/__init__.py
    event_new_hr = async_track_time_change(hass, cb_new_hr, minute=0, second=0)
    event_new_day = async_track_time_change(hass, cb_new_day, hour=0, minute=0, second=0)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle unload of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    await hass.config_entries.async_reload(entry.entry_id)
