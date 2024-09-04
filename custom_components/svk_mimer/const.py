"""Common constants."""

from homeassistant.const import Platform


# Base component constants
NAME = "svk_mimer"
DOMAIN = "svk_mimer"
CURRENCY = "SEK"
INTEGRATION_VERSION = "master"
ISSUE_URL = "https://github.com/robinostlund/homeassistant-svk-mimer/issues"
UPDATE_INTERVAL = 600
URL_SVK_MIMER = "https://mimer.svk.se/PrimaryRegulation/PrimaryRegulationIndex"


# Platforms
PLATFORMS = [
    Platform.SENSOR,
]

# Configuration contants
CONF_KW_AVAILABLE = "kw_available"
CONF_FEE_PERCENT = "fee_percent"
CONF_VAT = "vat"
CONF_MONITOR_FCR_N = "monitor_fcr_n"
CONF_MONITOR_FCR_D = "monitor_fcr_d"
CONF_SUBSCRIBING_FCR_N = "subscribing_fcr_n"
CONF_SUBSCRIBING_FCR_D = "subscribing_fcr_d"

# Default value contants
DEFAULT_KW_AVAILABLE = 1
DEFAULT_FEE_PERCENT = 0
DEFAULT_VAT = False
DEFAULT_MONITOR_FCR_N = False
DEFAULT_MONITOR_FCR_D = True
DEFAULT_SUBSCRIBING_FCR_N = False
DEFAULT_SUBSCRIBING_FCR_D = False

# Message constants
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {INTEGRATION_VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

CURRENT_CONFIG_VER = 1

EVENT_NEW_HOUR = f"{DOMAIN}_update_hour"
EVENT_NEW_DAY = f"{DOMAIN}_update_day"
