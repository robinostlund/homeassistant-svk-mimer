"""Platform for sensor integration."""
from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import date, datetime, timedelta
from dataclasses import dataclass


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

#from homeassistant.helpers.entity import DeviceInfo, DeviceEntryType
#from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CURRENCY,
    DOMAIN,
    URL_SVK_MIMER,
    EVENT_NEW_HOUR,
    EVENT_NEW_DAY,
    CONF_KW_AVAILABLE,
    CONF_FEE_PERCENT,
    CONF_VAT,
    DEFAULT_KW_AVAILABLE,
    DEFAULT_FEE_PERCENT,
    DEFAULT_VAT
)
from .entity import SVKMimerEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class SVKMimerSensorRequiredKeysMixin:
    """Mixin for required keys."""

    value_fn: Callable[[SVKMimerEntity], float]
    #value_multiplier: Callable[[SVKMimerEntity], float]
    # available_fn: Callable[[SVKMimerEntity], bool]


@dataclass
class SVKMimerSensorEntityDescription(
    SensorEntityDescription, SVKMimerSensorRequiredKeysMixin
):
    """Describes a sensor entity description."""

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SVKMimerSensorEntityDescription(
        key = 'fcr_n',
        name = 'FCR-N',
        icon = 'mdi:cash',
        entity_registry_enabled_default=True,
        #entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        #device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=CURRENCY,
        value_fn=lambda data: data.prices_fcr_n,
    ),
    SVKMimerSensorEntityDescription(
        key = 'fcr_n_earnings_today',
        name = 'FCR-N Estimated Earnings Today',
        icon = 'mdi:cash',
        entity_registry_enabled_default=True,
        #entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        #device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=CURRENCY,
        value_fn=lambda data: data.prices_fcr_n,
    ),
    SVKMimerSensorEntityDescription(
        key = 'fcr_d_up',
        name = 'FCR-D Up',
        icon = 'mdi:cash',
        entity_registry_enabled_default=True,
        #entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        #device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=CURRENCY,
        value_fn=lambda data: data.prices_fcr_d_up,
    ),
    SVKMimerSensorEntityDescription(
        key = 'fcr_d_up_earnings_today',
        name = 'FCR-D Up Estimated Earnings Today',
        icon = 'mdi:cash',
        entity_registry_enabled_default=True,
        #entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        #device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=CURRENCY,
        value_fn=lambda data: data.prices_fcr_d_up,
    ),
    SVKMimerSensorEntityDescription(
        key = 'fcr_d_down',
        name = 'FCR-D Down',
        icon = 'mdi:cash',
        entity_registry_enabled_default=True,
        #entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        #device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=CURRENCY,
        value_fn=lambda data: data.prices_fcr_d_down,
    ),
    SVKMimerSensorEntityDescription(
        key = 'fcr_d_down_earnings_today',
        name = 'FCR-D Down Estimated Earnings Today',
        icon = 'mdi:cash',
        entity_registry_enabled_default=True,
        #entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        #device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=CURRENCY,
        value_fn=lambda data: data.prices_fcr_d_down,
    )
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for description in SENSOR_TYPES:
        if "_earnings_today" in description.key:
            sensor = SVKMimerEarningsSensor(
                hass,
                coordinator, 
                description,
                price_multiplier = entry.data.get(CONF_KW_AVAILABLE, DEFAULT_KW_AVAILABLE),
                price_percentage_fee = entry.data.get(CONF_FEE_PERCENT, DEFAULT_FEE_PERCENT),
                price_include_vat = entry.data.get(CONF_VAT, DEFAULT_VAT)
            )
        else:
            sensor = SVKMimerSensor(
                hass,
                coordinator, 
                description,
                price_multiplier = entry.data.get(CONF_KW_AVAILABLE, DEFAULT_KW_AVAILABLE),
                price_percentage_fee = entry.data.get(CONF_FEE_PERCENT, DEFAULT_FEE_PERCENT),
                price_include_vat = entry.data.get(CONF_VAT, DEFAULT_VAT)
            )
        entities.append(sensor)
        
    async_add_entities(entities)


# class SVKMimerSensor(SensorEntity, CoordinatorEntity, RestoreEntity):
class SVKMimerSensor(SensorEntity, SVKMimerEntity):
    """Sensors data"""

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, coordinator, description: SVKMimerSensorEntityDescription, 
        price_multiplier: float = 0, price_percentage_fee: int = 0, price_include_vat: bool = False) -> None:
        """Set up sensor entity."""
        super().__init__(coordinator)
        self.hass = hass

        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self.entity_description = description

        self.price_multiplier = price_multiplier
        self.price_percentage_fee = price_percentage_fee
        self.price_include_vat = price_include_vat

    def _get_prices_with_date(self, prices: dict, date: str) -> dict:
        """Returns only prices with specified date"""
        data = {}
        for key, val in prices.items():
            if date == datetime.strptime(key, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"):
                if self.price_multiplier > 1:
                    val = val * self.price_multiplier
                if self.price_percentage_fee > 0:
                    perc = lambda x : x/100
                    fee = val * perc(self.price_percentage_fee)
                    val -= fee
                if self.price_include_vat:
                    val = val * 0.75
                data[key] = val
        return data

    def _get_prices_raw(self, prices: dict) -> list:
        """Returns prices in raw format"""
        data = []
        for key, val in prices.items():
            item = {
                "start": key,
                "end": (datetime.strptime(key, "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "value": val
            }
            data.append(item)
        return data

    @property
    def _get_prices_today(self) -> dict:
        """Returns only todays prices"""
        return self._get_prices_with_date(
            prices = self.entity_description.value_fn(self.coordinator.data),
            date = date.today().strftime("%Y-%m-%d")
        )

    @property
    def _get_prices_tomorrow(self) -> dict:
        """Returns only tomorrows prices"""
        return self._get_prices_with_date(
            prices = self.entity_description.value_fn(self.coordinator.data),
            date = (date.today() + timedelta(1)).strftime("%Y-%m-%d")
        )

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        hour_now = datetime.now().strftime("%Y-%m-%d %H:00:00")
        return self._get_prices_today.get(hour_now)

    @property
    def available(self):
        """Return the availability of the sensor."""
        prices = self._get_prices_today
        hour_now = datetime.now().strftime("%Y-%m-%d %H:00:00")
        if prices and hour_now in prices:
            return True
        else:
            return False

    @property
    def extra_state_attributes(self) -> dict:
        """Return the attributes of the sensor."""
        # https://github.com/custom-components/nordpool/blob/master/custom_components/nordpool/sensor.py
        prices_today = self._get_prices_today
        prices_tomorrow = self._get_prices_tomorrow

        attributes = {
            "currency": CURRENCY,
            "today": list(prices_today.values()),
            "today_raw": self._get_prices_raw(prices_today),
            "today_sum": sum(prices_today.values()),
            "tomorrow": list(prices_tomorrow.values()),
            "tomorrow_raw": self._get_prices_raw(prices_tomorrow),
            "tomorrow_sum": sum(prices_tomorrow.values()),
            "tomorrow_valid": True if prices_tomorrow else False,
        }
        if hasattr(self, "add_state_attributes"):
            attributes = {**attributes, **self.add_state_attributes}
        return attributes

    async def _handle_new_data(self) -> None:
        #self._attr_native_value = self.entity_description.value_fn(self.coordinator.data).get(self.hour_now)
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        await super().async_added_to_hass()
        _LOGGER.debug(f"called async_added_to_hass {self.name}")

        async_dispatcher_connect(self.hass, EVENT_NEW_DAY, self._handle_new_data)
        #async_dispatcher_connect(self.hass, EVENT_NEW_PRICE, self._handle_new_data)
        async_dispatcher_connect(self.hass, EVENT_NEW_HOUR, self._handle_new_data)
        await self._handle_new_data()


class SVKMimerEarningsSensor(SVKMimerSensor):

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        prices_today = self._get_prices_today
        return sum(prices_today.values())

    @property
    def extra_state_attributes(self) -> dict:
        """Return the attributes of the sensor."""

        attributes = {
            "currency": CURRENCY,
        }
        if hasattr(self, "add_state_attributes"):
            attributes = {**attributes, **self.add_state_attributes}
        return attributes