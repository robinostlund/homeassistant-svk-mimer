"""Platform for Husqvarna Automower basic entity."""

import logging
from datetime import datetime, date

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo, DeviceEntryType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import SVKMimerDataUpdateCoordinator
from .const import DOMAIN, URL_SVK_MIMER

_LOGGER = logging.getLogger(__name__)


class SVKMimerEntity(CoordinatorEntity[SVKMimerDataUpdateCoordinator]):
    """Defining the SVKMimer Basic Entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator) -> None:
        """Initialize SVKMimerEntity."""
        super().__init__(coordinator)

        #self.coordinator = coordinator

    # @callback
    # def _handle_coordinator_update(self) -> None:
    #     """Handle updated data from the coordinator."""
    #     #self._attr_is_on = self.coordinator.data
    #     self.async_write_ha_state()

    def get_data(self, key: str) -> dict:
        """Get data from coordinator."""
        return self.coordinator.data.get(key)

    @property
    def device_info(self) -> DeviceInfo:
        """Define the DeviceInfo of the sensor."""
        return DeviceInfo(
            identifiers={(DOMAIN, 'svk_mimer')},
            name='SVK Mimer',
            manufacturer='SVK',
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=URL_SVK_MIMER,
            model='Mimer',
        )

    @property
    def add_state_attributes(self):
        """Return the state attributes."""
        return {
            "update_success": self.coordinator.last_update_success,
            "last_updated": self.coordinator.last_updated.strftime("%Y-%m-%d %H:%M:%S") if self.coordinator.last_updated else None
        }

    @property
    def should_poll(self) -> bool:
        """Return True if the device is available."""
        return False